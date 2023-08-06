# Copyright 2021 Spotify AB

import abc
import datetime
import hashlib
import json
import logging
import os
import uuid

import docker
import glom
import yaml

from google.cloud import pubsub_v1
from googleapiclient import discovery

from klio_core import dataflow

logger = logging.getLogger("klio")
logger.setLevel(logging.INFO)


class _AbstractBenchmarkPlatformMetadata(abc.ABC):
    def __init__(self, job_config, job_dir):
        self._job_config = job_config
        self._job_dir = job_dir

    @abc.abstractmethod
    def get_metadata(self):
        pass

    @abc.abstractmethod
    def get_vcpu_count(self):
        pass


class _BenchmarkDefaultMetadata(_AbstractBenchmarkPlatformMetadata):
    """Default metadata when not on GKE or Dataflow.

    Will mostly be used in case someone benchmarks their job locally
    with direct runner (for whatever reason). But this is a bit of
    future proofing in case we benchmark on other platforms, too.
    """

    def get_metadata(self):
        return {}

    def get_vcpu_count(self):
        # This assumes we're on DirectRunner locally - and DirectRunner
        # only uses one CPU
        return 1


class _BenchmarkDataflowMetadata(_AbstractBenchmarkPlatformMetadata):
    """Benchmark data utilities specific for Dataflow-based jobs."""

    def _get_dataflow_job_id(self):
        client = dataflow.DataflowClient()
        try:
            job_data = client.find_job_by_name(
                job_name=self._job_config.job_name,
                gcp_project=self._job_config.pipeline_options.project,
                region=self._job_config.pipeline_options.region,
            )
            return job_data["id"]
        except Exception as e:
            logger.warning(
                "Unable to find Dataflow Job ID for "
                f"{self._job_config.job_name}. The benchmark will still be "
                "started, but the job may not have been submitted to Dataflow "
                f"successfully. Error: {e}"
            )
            return "NOT_FOUND"

    def get_metadata(self):
        job_id = self._get_dataflow_job_id()
        opts = self._job_config.pipeline_options

        max_num_workers = opts.max_num_workers
        autoscaling_on = opts.autoscaling_algorithm != "NONE"
        if autoscaling_on is False:
            max_num_workers = None
        harness_threads = opts.as_dict().get(
            "number_of_worker_harness_threads"
        )
        disk_type_url = opts.worker_disk_type
        disk_type = disk_type_url.split("/")[-1]

        return {
            "dataflow_metadata": {
                "dataflow_job_id": job_id,
                "machine_type": opts.worker_machine_type,
                "num_workers": opts.num_workers,
                "max_num_workers": max_num_workers,
                "autoscaling_on": autoscaling_on,
                "disk_type": disk_type,
                "region": opts.region,
                "experiments": opts.experiments,
                "number_of_worker_harness_threads": harness_threads,
            }
        }

    def get_vcpu_count(self):
        opts = self._job_config.pipeline_options
        machine_type = opts.worker_machine_type
        cpu_count = int(machine_type.split("-")[-1])
        num_workers = int(opts.num_workers)
        return cpu_count * num_workers


class _BenchmarkGKEMetadata(_AbstractBenchmarkPlatformMetadata):
    """Benchmark data utilities specific for GKE-based jobs."""

    def __init__(self, job_config, job_dir):
        super().__init__(job_config, job_dir)
        self._job_metadata = {}

    def _set_deployment_info(self):
        path_to_deployment_config = os.path.join(
            self._job_dir, "kubernetes", "deployment.yaml"
        )
        with open(path_to_deployment_config, "r") as f:
            depl_conf = yaml.safe_load(f)

        replicas = glom.glom(depl_conf, "spec.replicas", default=None)
        containers = glom.glom(
            depl_conf, "spec.template.spec.containers", default=[]
        )
        # NOTE: this assumes that the first container is the job's container
        resources = glom.glom(containers[0], "resources", default={})

        res_reqs = glom.glom(resources, "requests", default={})
        cpu_requests = glom.glom(res_reqs, "cpu", default=None)
        mem_requests = glom.glom(res_reqs, "memory", default=None)

        res_lmts = glom.glom(resources, "limits", default={})
        cpu_limits = glom.glom(res_lmts, "cpu", default=None)
        mem_limits = glom.glom(res_lmts, "memory", default=None)

        self._job_metadata["replica_count"] = replicas
        self._job_metadata["cpu"] = {
            "requests": cpu_requests,
            "limits": cpu_limits,
        }
        self._job_metadata["memory"] = {
            "requests": mem_requests,
            "limits": mem_limits,
        }

    def _set_autoscaling_info(self):
        # TODO: abstract away a bit - may not be named "hpa.yaml"
        # TODO: also, not sure if it's safe to assume this is actually
        # applied to the deployment
        hpa_config_path = os.path.join(self._job_dir, "kubernetes", "hpa.yaml")
        autoscaling_on = False
        min_replica_count, max_replica_count = None, None

        if os.path.exists(hpa_config_path):
            with open(hpa_config_path, "r") as f:
                hpa_config = yaml.safe_load(f)
            autoscaling_on = True
            max_replica_count = glom.glom(hpa_config, "spec.maxReplicas")
            min_replica_count = glom.glom(hpa_config, "spec.minReplicas")

        self._job_metadata["autoscaling_on"] = autoscaling_on
        self._job_metadata["min_replica_count"] = min_replica_count
        self._job_metadata["max_replica_count"] = max_replica_count

    def get_metadata(self):
        try:
            from kubernetes import config as k8s_config
        except ImportError as e:
            if "kubernetes" in e.msg:
                logger.error(
                    "Failed to import DirectGKERunner dependencies. "
                    "Did you install `spotify-klio-cli[kubernetes]`?"
                )
                raise SystemExit(1)
            logger.error(e)
            raise SystemExit(1)

        _, active_context = k8s_config.list_kube_config_contexts()
        self._job_metadata["cluster_name"] = active_context["name"]

        # TODO: hardcode to backend cluster - need to figure out where to get
        # this info if users ever use a different project
        self._job_metadata["cluster_gcp_project"] = "gke-xpn-1"

        # TODO: hardcoded for now - not sure if every backend cluster is
        # setup with the same machine type, or where to get this info
        # dynamically
        self._job_metadata["machine_type"] = "e2-standard-32"

        self._set_deployment_info()
        self._set_autoscaling_info()
        return {"gke_metadata": self._job_metadata}

    def get_vcpu_count(self):
        # TODO: This actually doesn't take into account autoscaling -
        # to do so, we'd need data from GKE to correlate vCPUs with
        # a job's timeline
        cpu_requests = glom.glom(self._job_metadata, "cpu.requests")
        replicas = glom.glom(self._job_metadata, "replica_count")
        replicas = int(replicas)  # I hope this doesn't error...
        try:
            cpu_requests = float(cpu_requests)
            return cpu_requests * replicas

        # raised when cpu_requests are in milli-cpus, like "100m"
        except ValueError:
            pass

        if not cpu_requests.endswith("m"):
            # i have no idea if we'd ever get here. but it's for safety :shrug:
            logger.warning(
                "Cannot compute the total number of vCPUs the job requested. "
                "Defaulting to number of replicas. This may throw off the "
                "vCPU-based benchmark calculations. "
                "Expected format: integer, float, or millicpus (e.g. 100m)."
            )
            return replicas

        millicpus = int(cpu_requests[:-1])
        cpus = millicpus / 1_000
        return cpus * replicas


class BenchmarkKlioPipeline:
    """Start a benchmark run of a Klio job.

    Emits benchmarking metadata for the job to a Pub/Sub topic, from
    which a Dataflow job reads and then writes to a BigQuery table
    (as of Sept 2021; this may be switched to a CloudSQL table).
    """

    DEFAULT_METADATA_TOPIC = (
        "projects/sigint/topics/user-benchmarking-job-metadata"
    )
    DEFAULT_DATA_TOPIC = "projects/sigint/topics/user-benchmarking-job-data"

    def __init__(self, job_dir, job_config, job_image, benchmark_config):
        self._job_dir = job_dir
        self._job_config = job_config
        self._image_name = job_image
        self._dataset = benchmark_config.dataset
        self._run_id = benchmark_config.run_id
        self._job_id = benchmark_config.job_id
        self._enabled = benchmark_config.enabled
        self._metadata_topic = (
            benchmark_config.metadata_topic or self.DEFAULT_METADATA_TOPIC
        )
        self._data_topic = (
            benchmark_config.data_topic or self.DEFAULT_DATA_TOPIC
        )

    @property
    def _is_dataflow(self):
        runner = self._job_config.pipeline_options.runner
        if "dataflow" in runner.lower():
            return True
        return False

    @property
    def _is_gke(self):
        runner = self._job_config.pipeline_options.runner
        if "directgkerunner" == runner.lower():
            return True
        return False

    def _get_or_create_job_id(self):
        if self._job_id:
            return self._job_id

        job_name = self._job_config.job_name
        benchmark_job_name = f"{job_name}::{self._dataset}".encode("utf-8")
        benchmark_job_hash = hashlib.md5()
        benchmark_job_hash.update(benchmark_job_name)
        benchmark_job_uuid = uuid.UUID(bytes=benchmark_job_hash.digest())
        return str(benchmark_job_uuid)

    def _get_environment(self):
        environ = {}
        docker_client = docker.from_env()
        # NOTE: this one command combines three version lookups into one:
        # python version, klio (lib) version, and beam version; and prints
        # the result to stdout in which we parse below
        versions_command = [
            "-c",
            (
                "python -c 'import sys,klio,apache_beam; "
                "print(sys.version_info[:2]); "
                "print(klio.__version__); "
                "print(apache_beam.__version__)'"
            ),
        ]
        runflags = {
            "image": self._image_name,
            "entrypoint": "bash",
            "detach": False,
            "auto_remove": True,
            "command": versions_command,
        }
        try:
            result = docker_client.containers.run(**runflags)
            result = result.decode("utf-8").strip()

            python_version, klio_version, apache_beam = result.split("\n")
            major, minor = python_version[1], python_version[-2]

        # catch any/all errors from command, Docker client, and parsing
        # string output caught from stdout
        except Exception as e:
            # TODO: is it a safe assumption that if we can't grab the Python,
            # Klio, or Beam version, that the job is going to fail? and
            # therefore we should fail starting the benchmark?
            logger.error(
                "Could not gather environment information from job's image due "
                "to error. It may be an issue connecting to local Docker, "
                "or this may mean Python, Klio, and/or Apache Beam "
                "is not installed and available in your job's image. "
                f"Error: {e}"
            )
            raise SystemExit(1)

        environ["beam_sdk_version"] = apache_beam
        environ["klio_version"] = klio_version
        environ["python_version"] = f"{major}.{minor}"

        return environ

    def _get_platform_metadata_obj(self):
        Kls = _BenchmarkDefaultMetadata
        if self._is_dataflow:
            Kls = _BenchmarkDataflowMetadata
        if self._is_gke:
            Kls = _BenchmarkGKEMetadata

        return Kls(self._job_config, self._job_dir)

    def _get_basic_metadata(self):
        started_at_dt = datetime.datetime.utcnow()
        started_at = started_at_dt.strftime("%Y-%m-%d %H:%M:%S.%f UTC")
        return {
            "job_name": self._job_config.job_name,
            "gcp_project": self._job_config.pipeline_options.project,
            "started_at": started_at,
            "benchmark_dataset_id": self._dataset,
            "is_streaming": self._job_config.pipeline_options.streaming,
            "is_dataflow": self._is_dataflow,
            # TODO: this is probably needed to connect the backstage UI
            # to which job(s) to actually render for a logged-in user;
            # we'll need to read this from data-info.yaml / service-info.yaml
            # "component_id": "deadbeef",
        }

    def _get_job_metadata(self, benchmark_job_id):
        job_metadata = self._get_basic_metadata()
        job_metadata["benchmark_run_id"] = self._run_id
        job_metadata["benchmark_job_id"] = benchmark_job_id
        # This call will fail if Python, Klio, and/or Beam is not
        # installed on the job's image (which would prevent from a
        # benchmark from successfully running)
        job_metadata["environment"] = self._get_environment()

        platform = self._get_platform_metadata_obj()
        platform_metadata = platform.get_metadata()
        job_metadata.update(platform_metadata)
        job_metadata["vCPU_count"] = platform.get_vcpu_count()
        return job_metadata

    def _emit_job_metadata(self, job_metadata):
        client = pubsub_v1.PublisherClient()

        bytes_data = json.dumps(job_metadata).encode("utf-8")
        future = client.publish(self._metadata_topic, bytes_data)
        future.result()

    def start(self):
        benchmark_job_id = self._get_or_create_job_id()
        try:
            job_metadata = self._get_job_metadata(benchmark_job_id)
        except Exception:
            logger.error(
                "Could not collect job metadata to start benchmark",
                exc_info=True,
            )
            raise SystemExit(1)
        try:
            self._emit_job_metadata(job_metadata)
        except Exception as e:
            logger.error(
                "Could not emit benchmark metadata for job. The job may have "
                "successfully started and be emitting benchmarking data, "
                "though.\nIf you think this is a transient error and the job "
                "was already successfully deployed, then re-run the command "
                "with klio_job.yaml::job_config.benchmark.skip_deploy=True and "
                f"klio_job.yaml::job_config.benchmark.job_id={benchmark_job_id}"
                f"\nError encountered: {e}",
                exc_info=True,
            )
            raise SystemExit(1)

        logger.info(
            f"Created a benchmark run {self._run_id} for benchmark job "
            f"{benchmark_job_id}"
        )

    @staticmethod
    def get_run_id(skip_deploy, klio_config, image_tag):
        """Get the benchmark run ID for job.

        Either generate a new UUID if a job is being deployed (and a run ID
        has not been provided via klio_job.yaml::job_config.benchmark.run_id),
        or reuse a run ID if we're skipping deployment.
        """
        if skip_deploy is not True:
            return str(uuid.uuid4())

        # if not set, then look at the config within the job's image by
        # running `cat <config file>` within the container and parsing for
        # benchmarking config
        docker_client = docker.from_env()

        image = "{}:{}".format(
            klio_config.pipeline_options.worker_harness_container_image,
            image_tag,
        )
        runflags = {
            "image": image,
            "entrypoint": "bash",
        }
        file_names = [
            "/usr/src/app/klio-job-run-effective.yaml",
            "/usr/src/app/klio-job.yaml",
        ]
        result = None
        for fn in file_names:
            runflags["command"] = ["-c", f"cat {fn}"]
            try:
                result = docker_client.containers.run(**runflags)
                result = yaml.safe_load(result)
                result = glom.glom(
                    result, "job_config.benchmark.run_id", default=None
                )
            except Exception:
                continue
            else:
                break

        if result is None:
            logger.error(
                "Used `klio_job.yaml::job_config.benchmark.skip_deploy` to "
                "skip a job's deployment, but Klio could not find a "
                "'job_config.benchmark.run_id' to reuse in the job's "
                f"configuration within {image}. "
                "Either:\n"
                "  (1) check if this is the correct image name and tag of the "
                "already-deployed job being benchmarked; or\n"
                "  (2) if the run ID is known, set the field in "
                "`klio_job.yaml::job_config.benchmark.run_id`; or\n"
                "  (3) re-run the command without skipping deployment, which "
                "will re-generate a run ID when the image rebuilds & deploys."
            )
            raise SystemExit(1)

        return result

    @staticmethod
    def get_and_validate_dataset(klio_config, dataset):
        """Validate provided dataset and return a sanitized string."""
        is_streaming = klio_config.pipeline_options.streaming
        if dataset is None and is_streaming:
            logger.error(
                "Must configure a benchmarking dataset in "
                "`klio_job.yaml::job_config.benchmark.dataset` "
                "since job is streaming."
            )
            raise SystemExit(1)

        elif dataset is None and not is_streaming:
            bq_project = klio_config.job_config.events.inputs[0].project
            bq_dataset = klio_config.job_config.events.inputs[0].dataset
            bq_table = klio_config.job_config.events.inputs[0].table
            if not all([bq_project, bq_dataset, bq_table]):
                logger.error(
                    "Cannot determine the benchmarking dataset from the "
                    "job's configuration. Please provide the dataset via "
                    "`klio_job.yaml::job_config.benchmark.dataset`, or "
                    "define the `project`, `dataset`, and `table` under "
                    "`job_config.events.inputs[]` in your job's config."
                )
                raise SystemExit(1)

            dataset = f"{bq_project}.{bq_dataset}.{bq_table}"

        dataset = dataset.replace(":", ".")
        split_dataset = dataset.split(".")
        if len(split_dataset) != 3:
            logger.error(
                f"Invalid benchmarking dataset '{dataset}'. Expecting format "
                "'<project>.<dataset>.<table>'."
            )
            raise SystemExit(1)

        bq_client = discovery.build("bigquery", "v2")
        req = bq_client.tables().get(
            projectId=split_dataset[0],
            datasetId=split_dataset[1],
            tableId=split_dataset[2],
        )
        try:
            req.execute()
        except Exception:
            logger.error(
                f"The benchmarking dataset '{dataset}' was not found."
            )
            raise SystemExit(1)
        return dataset
