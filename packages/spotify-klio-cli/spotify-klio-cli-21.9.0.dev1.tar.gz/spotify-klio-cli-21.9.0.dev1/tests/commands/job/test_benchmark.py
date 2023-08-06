# Copyright 2021 Spotify AB
import datetime

import kubernetes
import pytest
import yaml

from spotify_klio_cli import cli
from spotify_klio_cli.commands.job import benchmark


# making tests a little more readable
get_and_validate_dataset = (
    benchmark.BenchmarkKlioPipeline.get_and_validate_dataset
)


@pytest.fixture
def mock_dataflow_job_config(mocker):
    mock_config = mocker.Mock()
    mock_config.job_name = "test-job"
    mock_config.pipeline_options.runner = "DataflowRunner"
    mock_config.pipeline_options.project = "test-project"
    mock_config.pipeline_options.streaming = True
    mock_config.pipeline_options.max_num_workers = 100
    mock_config.pipeline_options.autoscaling_algorithm = "NONE"
    mock_config.pipeline_options.as_dict.return_value = {
        "number_of_worker_harness_threads": 1
    }
    mock_config.pipeline_options.worker_disk_type = "some/url/path/pd-ssd"
    mock_config.pipeline_options.worker_machine_type = "n1-standard-4"
    mock_config.pipeline_options.num_workers = 10
    mock_config.pipeline_options.region = "boonies"
    mock_config.pipeline_options.experiments = ["foo-exp", "bar-exp"]

    return mock_config


@pytest.fixture
def mock_gke_job_config(mocker):
    mock_config = mocker.Mock()
    mock_config.job_name = "test-job"
    mock_config.pipeline_options.runner = "DirectGKERunner"
    mock_config.pipeline_options.project = "test-project"
    mock_config.pipeline_options.streaming = True
    return mock_config


@pytest.fixture
def mock_k8s_deployment():
    return {
        "spec": {
            "replicas": 10,
            "template": {
                "spec": {
                    "containers": [
                        {
                            "resources": {
                                "requests": {"cpu": 1, "memory": "1G"},
                                "limits": {"cpu": 2, "memory": "2G"},
                            }
                        }
                    ]
                }
            },
        }
    }


@pytest.fixture
def mock_k8s_hpa():
    return {"spec": {"minReplicas": 1, "maxReplicas": 10}}


@pytest.fixture
def benchmark_job_config():
    return cli.SpotifyBenchmarkJobConfig(
        dataset="foo.bar.baz",
        enabled=True,
        job_id=None,
        run_id=None,
        metadata_topic=None,
        data_topic=None,
    )


@pytest.fixture
def benchmark_klio_pipeline_df(
    mocker, mock_dataflow_job_config, benchmark_job_config
):
    mock_config = mocker.Mock()
    mock_config.job_name = "test-job"
    return benchmark.BenchmarkKlioPipeline(
        job_dir="/test/",
        job_config=mock_dataflow_job_config,
        job_image="gcr.io/foo/bar",
        benchmark_config=benchmark_job_config,
    )


@pytest.fixture
def benchmark_klio_pipeline_gke(
    mocker, mock_gke_job_config, benchmark_job_config
):
    mock_config = mocker.Mock()
    mock_config.job_name = "test-job"
    return benchmark.BenchmarkKlioPipeline(
        job_dir="/test/",
        job_config=mock_gke_job_config,
        job_image="gcr.io/foo/bar",
        benchmark_config=benchmark_job_config,
    )


@pytest.fixture
def dataflow_client(mocker, monkeypatch):
    mock_client = mocker.MagicMock()
    mock_client().find_job_by_name.return_value = {"id": "d4t4fl0w-j0b-1d"}
    monkeypatch.setattr(benchmark.dataflow, "DataflowClient", mock_client)
    return mock_client


@pytest.fixture
def k8s_client(mocker, monkeypatch):
    mock_client = mocker.MagicMock()
    mock_client.list_kube_config_contexts.return_value = (
        {},
        {"name": "some-cluster-name"},
    )
    monkeypatch.setattr(kubernetes, "config", mock_client)
    return mock_client


@pytest.fixture
def pubsub_client(mocker, monkeypatch):
    mock_pubsub_client = mocker.Mock()
    monkeypatch.setattr(
        benchmark.pubsub_v1, "PublisherClient", mock_pubsub_client
    )
    return mock_pubsub_client


class TestBenchmarkDefaultMetadata:
    @pytest.fixture
    def bm_default_inst(self, mocker):
        mock_config = mocker.Mock()
        return benchmark._BenchmarkDefaultMetadata(mock_config, "/test/")

    def test_get_metadata(self, bm_default_inst):
        act_ret = bm_default_inst.get_metadata()
        assert {} == act_ret

    def test_get_vcpu_count(self, bm_default_inst):
        act_ret = bm_default_inst.get_vcpu_count()
        assert 1 == act_ret


class TestBenchmarkDataflowMetadata:
    @pytest.fixture
    def bm_df_inst(self, mock_dataflow_job_config, dataflow_client):
        return benchmark._BenchmarkDataflowMetadata(
            mock_dataflow_job_config, "/test/"
        )

    def test_get_dataflow_job_id(self, bm_df_inst, dataflow_client):
        ret_id = bm_df_inst._get_dataflow_job_id()
        assert "d4t4fl0w-j0b-1d" == ret_id

        dataflow_client().find_job_by_name.assert_called_once_with(
            job_name="test-job", gcp_project="test-project", region="boonies"
        )

    def test_get_dataflow_job_id_raises(
        self, bm_df_inst, dataflow_client, caplog
    ):
        dataflow_client().find_job_by_name.side_effect = Exception("oh nooo")

        ret_id = bm_df_inst._get_dataflow_job_id()
        assert "NOT_FOUND" == ret_id
        dataflow_client().find_job_by_name.assert_called_once_with(
            job_name="test-job", gcp_project="test-project", region="boonies"
        )
        assert 1 == len(caplog.records)
        assert (
            "Unable to find Dataflow Job ID for " in caplog.records[0].message
        )

    @pytest.mark.parametrize(
        "autoscaling_algo,exp_max_num_workers,exp_autoscaling",
        (("NONE", None, False), ("THROUGHPUT_BASE", 100, True),),
    )
    def test_get_metadata(
        self,
        autoscaling_algo,
        exp_max_num_workers,
        exp_autoscaling,
        mock_dataflow_job_config,
        bm_df_inst,
        monkeypatch,
    ):
        monkeypatch.setattr(
            mock_dataflow_job_config.pipeline_options,
            "autoscaling_algorithm",
            autoscaling_algo,
        )
        exp_metadata = {
            "dataflow_metadata": {
                "dataflow_job_id": "d4t4fl0w-j0b-1d",
                "machine_type": "n1-standard-4",
                "num_workers": 10,
                "max_num_workers": exp_max_num_workers,
                "autoscaling_on": exp_autoscaling,
                "disk_type": "pd-ssd",
                "region": "boonies",
                "experiments": ["foo-exp", "bar-exp"],
                "number_of_worker_harness_threads": 1,
            }
        }
        assert exp_metadata == bm_df_inst.get_metadata()

    def test_get_vcpu_count(self, bm_df_inst):
        assert 40 == bm_df_inst.get_vcpu_count()


class TestBenchmarkGKEMetadata:
    @pytest.fixture
    def bm_gke_inst(self, mock_gke_job_config, k8s_client):
        return benchmark._BenchmarkGKEMetadata(mock_gke_job_config, "/test/")

    def test_set_deployment_info(
        self, bm_gke_inst, mock_k8s_deployment, mocker
    ):
        m_open = mocker.mock_open(read_data=yaml.dump(mock_k8s_deployment))
        mock_open = mocker.patch(
            "spotify_klio_cli.commands.job.benchmark.open", m_open
        )

        assert bm_gke_inst._job_metadata == {}  # sanity
        bm_gke_inst._set_deployment_info()
        exp_job_metadata = {
            "replica_count": 10,
            "cpu": {"requests": 1, "limits": 2},
            "memory": {"requests": "1G", "limits": "2G"},
        }
        assert exp_job_metadata == bm_gke_inst._job_metadata
        mock_open.assert_called_once_with(
            "/test/kubernetes/deployment.yaml", "r"
        )

    # TODO: case when hpa.yaml doesn't exist
    def test_set_autoscaling_info(
        self, bm_gke_inst, mock_k8s_hpa, mocker, monkeypatch
    ):
        m_open = mocker.mock_open(read_data=yaml.dump(mock_k8s_hpa))
        mock_open = mocker.patch(
            "spotify_klio_cli.commands.job.benchmark.open", m_open
        )
        mock_path_exists = mocker.Mock(return_value=True)
        monkeypatch.setattr(benchmark.os.path, "exists", mock_path_exists)

        assert bm_gke_inst._job_metadata == {}  # sanity
        bm_gke_inst._set_autoscaling_info()
        exp_job_metadata = {
            "autoscaling_on": True,
            "min_replica_count": 1,
            "max_replica_count": 10,
        }
        assert exp_job_metadata == bm_gke_inst._job_metadata
        mock_open.assert_called_once_with("/test/kubernetes/hpa.yaml", "r")
        mock_path_exists.assert_called_once_with("/test/kubernetes/hpa.yaml")

    def test_get_metadata(self, bm_gke_inst, mocker, monkeypatch):
        mock_set_deployment_info = mocker.Mock()
        mock_set_autoscaling_info = mocker.Mock()
        monkeypatch.setattr(
            bm_gke_inst, "_set_deployment_info", mock_set_deployment_info
        )
        monkeypatch.setattr(
            bm_gke_inst, "_set_autoscaling_info", mock_set_autoscaling_info
        )

        assert bm_gke_inst._job_metadata == {}  # sanity
        act_ret = bm_gke_inst.get_metadata()
        exp_ret = {
            "gke_metadata": {
                "cluster_name": "some-cluster-name",
                "cluster_gcp_project": "gke-xpn-1",
                "machine_type": "e2-standard-32",
            }
        }
        assert exp_ret == act_ret

    # TODO: parametrize different cpu values
    @pytest.mark.parametrize(
        "cpu,exp_cpu",
        (
            (1, 1 * 10),
            ("1", 1 * 10),
            (1.5, 1.5 * 10),
            ("1.5", 1.5 * 10),
            ("100m", 0.1 * 10),
        ),
    )
    def test_get_vcpu_count(self, cpu, exp_cpu, bm_gke_inst, monkeypatch):
        job_metadata = {"cpu": {"requests": cpu}, "replica_count": 10}
        monkeypatch.setattr(bm_gke_inst, "_job_metadata", job_metadata)

        ret_cpu = bm_gke_inst.get_vcpu_count()
        assert exp_cpu == ret_cpu


class TestBenchmarkKlioPipeline:
    @pytest.fixture
    def bm_df_inst(self, mock_dataflow_job_config, dataflow_client):
        return benchmark._BenchmarkDataflowMetadata(
            mock_dataflow_job_config, "/test/"
        )

    @pytest.fixture
    def bm_gke_inst(self, mock_gke_job_config, k8s_client):
        return benchmark._BenchmarkGKEMetadata(mock_gke_job_config, "/test/")

    @pytest.mark.parametrize(
        "beam_runner,exp_ret_val",
        (
            ("Dataflow", True),
            ("DataflowRunner", True),
            ("dataflow", True),
            ("DirectGKERunner", False),
            ("DirectRunner", False),
        ),
    )
    def test_is_dataflow(
        self, beam_runner, exp_ret_val, mocker, benchmark_job_config
    ):
        mock_job_config = mocker.Mock()
        mock_job_config.pipeline_options.runner = beam_runner
        pipeline = benchmark.BenchmarkKlioPipeline(
            job_dir="",
            job_config=mock_job_config,
            job_image="gcr.io/foo/bar",
            benchmark_config=benchmark_job_config,
        )
        assert exp_ret_val == pipeline._is_dataflow

    @pytest.mark.parametrize(
        "beam_runner,exp_ret_val",
        (
            ("DirectGKERunner", True),
            ("Dataflow", False),
            ("DataflowRunner", False),
            ("dataflow", False),
            ("DirectRunner", False),
        ),
    )
    def test_is_gke(
        self, beam_runner, exp_ret_val, mocker, benchmark_job_config
    ):
        mock_job_config = mocker.Mock()
        mock_job_config.pipeline_options.runner = beam_runner
        pipeline = benchmark.BenchmarkKlioPipeline(
            job_dir="",
            job_config=mock_job_config,
            job_image="gcr.io/foo/bar",
            benchmark_config=benchmark_job_config,
        )
        assert exp_ret_val == pipeline._is_gke

    def test_get_or_create_job_id(
        self, benchmark_klio_pipeline_df, mocker, monkeypatch
    ):
        mock_md5 = mocker.Mock()
        monkeypatch.setattr(benchmark.hashlib, "md5", mock_md5)
        mock_uuid = mocker.Mock(return_value="deadbeef")
        monkeypatch.setattr(benchmark.uuid, "UUID", mock_uuid)

        act_job_id = benchmark_klio_pipeline_df._get_or_create_job_id()
        assert "deadbeef" == act_job_id

        exp_benchmark_name = b"test-job::foo.bar.baz"
        mock_md5.return_value.update.assert_called_once_with(
            exp_benchmark_name
        )
        mock_md5.return_value.digest.assert_called_once_with()
        mock_uuid.assert_called_once_with(
            bytes=mock_md5.return_value.digest.return_value
        )

    @pytest.mark.parametrize(
        "beam_runner,exp_inst_type",
        (
            ("dataflow", benchmark._BenchmarkDataflowMetadata),
            ("directgkerunner", benchmark._BenchmarkGKEMetadata),
            ("directrunner", benchmark._BenchmarkDefaultMetadata),
            ("other", benchmark._BenchmarkDefaultMetadata),
        ),
    )
    def test_get_platform_metadata_obj(
        self,
        beam_runner,
        exp_inst_type,
        benchmark_klio_pipeline_df,
        monkeypatch,
    ):
        monkeypatch.setattr(
            benchmark_klio_pipeline_df._job_config.pipeline_options,
            "runner",
            beam_runner,
        )

        platform_metadata_inst = (
            benchmark_klio_pipeline_df._get_platform_metadata_obj()
        )
        if exp_inst_type is None:
            assert platform_metadata_inst is None
        else:
            assert isinstance(platform_metadata_inst, exp_inst_type)

    def test_get_job_metadata_dataflow(
        self, mocker, benchmark_klio_pipeline_df, bm_df_inst, monkeypatch
    ):
        monkeypatch.setattr(
            benchmark_klio_pipeline_df,
            "_get_platform_metadata_obj",
            lambda: bm_df_inst,
        )
        monkeypatch.setattr(
            benchmark_klio_pipeline_df, "_get_environment", lambda: {}
        )
        mock_datetime = mocker.MagicMock(wraps=benchmark.datetime.datetime)
        mock_datetime.utcnow.return_value = datetime.datetime(
            2021, 1, 1, 12, 34, 56
        )
        monkeypatch.setattr(benchmark.datetime, "datetime", mock_datetime)

        act_ret = benchmark_klio_pipeline_df._get_job_metadata("deadbeef")

        exp_ret = {
            "job_name": "test-job",
            "started_at": "2021-01-01 12:34:56.000000 UTC",
            "benchmark_job_id": "deadbeef",
            "benchmark_run_id": None,
            "benchmark_dataset_id": "foo.bar.baz",
            "environment": {},
            "vCPU_count": 40,
            "is_dataflow": True,
            "is_streaming": True,
            "gcp_project": "test-project",
            "dataflow_metadata": {
                "dataflow_job_id": "d4t4fl0w-j0b-1d",
                "machine_type": "n1-standard-4",
                "num_workers": 10,
                "max_num_workers": None,
                "autoscaling_on": False,
                "disk_type": "pd-ssd",
                "region": "boonies",
                "experiments": ["foo-exp", "bar-exp"],
                "number_of_worker_harness_threads": 1,
            },
        }
        assert exp_ret == act_ret

    def test_get_job_metadata_gke(
        self, mocker, benchmark_klio_pipeline_gke, bm_gke_inst, monkeypatch
    ):
        monkeypatch.setattr(
            benchmark_klio_pipeline_gke,
            "_get_platform_metadata_obj",
            lambda: bm_gke_inst,
        )
        monkeypatch.setattr(
            benchmark_klio_pipeline_gke, "_get_environment", lambda: {}
        )
        mock_datetime = mocker.MagicMock(wraps=benchmark.datetime.datetime)
        mock_datetime.utcnow.return_value = datetime.datetime(
            2021, 1, 1, 12, 34, 56
        )
        monkeypatch.setattr(benchmark.datetime, "datetime", mock_datetime)
        mock_set_deployment_info = mocker.Mock()
        mock_set_autoscaling_info = mocker.Mock()
        mock_get_vcpu_count = mocker.Mock(return_value=40)
        monkeypatch.setattr(
            bm_gke_inst, "_set_deployment_info", mock_set_deployment_info
        )
        monkeypatch.setattr(
            bm_gke_inst, "_set_autoscaling_info", mock_set_autoscaling_info
        )
        monkeypatch.setattr(bm_gke_inst, "get_vcpu_count", mock_get_vcpu_count)

        act_ret = benchmark_klio_pipeline_gke._get_job_metadata("deadbeef")

        exp_ret = {
            "job_name": "test-job",
            "started_at": "2021-01-01 12:34:56.000000 UTC",
            "benchmark_job_id": "deadbeef",
            "benchmark_run_id": None,
            "benchmark_dataset_id": "foo.bar.baz",
            "environment": {},
            "vCPU_count": 40,
            "is_dataflow": False,
            "is_streaming": True,
            "gcp_project": "test-project",
            "gke_metadata": {
                "cluster_gcp_project": "gke-xpn-1",
                "cluster_name": "some-cluster-name",
                "machine_type": "e2-standard-32",
            },
        }
        assert exp_ret == act_ret

    def test_emit_job_metadata(
        self, benchmark_klio_pipeline_df, pubsub_client
    ):
        job_metadata = {"some": "metadata"}
        exp_published_data = b'{"some": "metadata"}'

        benchmark_klio_pipeline_df._emit_job_metadata(job_metadata)

        pubsub_client.assert_called_once_with()
        pubsub_client.return_value.publish.assert_called_once_with(
            benchmark_klio_pipeline_df._metadata_topic, exp_published_data
        )
        mock_future = pubsub_client.return_value.publish.return_value
        mock_future.result.assert_called_once_with()

    def test_start(
        self, mocker, monkeypatch, benchmark_klio_pipeline_df, caplog
    ):
        mock_get_or_create_job_id = mocker.Mock(return_value="deadbeef")
        monkeypatch.setattr(
            benchmark_klio_pipeline_df,
            "_get_or_create_job_id",
            mock_get_or_create_job_id,
        )
        job_metadata = {
            "job_name": "test-job",
            "started_at": "2021-01-01 12:34:56.000000 UTC",
            "benchmark_job_id": "deadbeef",
            "benchmark_run_id": None,
            "benchmark_dataset_id": "foo.bar.baz",
            "environment": {},
            "vCPU_count": 40,
            "is_dataflow": True,
            "is_streaming": True,
            "gcp_project": "test-project",
            "dataflow_metadata": {
                "dataflow_job_id": "d4t4fl0w-j0b-1d",
                "machine_type": "n1-standard-4",
                "num_workers": 10,
                "max_num_workers": None,
                "autoscaling_on": False,
                "disk_type": "pd-ssd",
                "region": "boonies",
                "experiments": ["foo-exp", "bar-exp"],
                "number_of_worker_harness_threads": 1,
            },
        }
        mock_job_metadata = mocker.Mock(return_value=job_metadata)
        monkeypatch.setattr(
            benchmark_klio_pipeline_df, "_get_job_metadata", mock_job_metadata
        )
        mock_emit_job_metadata = mocker.Mock()
        monkeypatch.setattr(
            benchmark_klio_pipeline_df,
            "_emit_job_metadata",
            mock_emit_job_metadata,
        )

        benchmark_klio_pipeline_df.start()

        mock_get_or_create_job_id.assert_called_once_with()
        mock_job_metadata.assert_called_once_with(
            mock_get_or_create_job_id.return_value
        )
        mock_emit_job_metadata.assert_called_once_with(job_metadata)
        assert 1 == len(caplog.records)
        assert "Created a benchmark run " in caplog.records[0].message

    def test_start_raises_metadata(
        self, mocker, monkeypatch, benchmark_klio_pipeline_df, caplog
    ):
        mock_get_or_create_job_id = mocker.Mock(return_value="deadbeef")
        monkeypatch.setattr(
            benchmark_klio_pipeline_df,
            "_get_or_create_job_id",
            mock_get_or_create_job_id,
        )
        mock_job_metadata = mocker.Mock(side_effect=Exception("fuuu"))
        monkeypatch.setattr(
            benchmark_klio_pipeline_df, "_get_job_metadata", mock_job_metadata
        )

        with pytest.raises(SystemExit):
            benchmark_klio_pipeline_df.start()

        mock_get_or_create_job_id.assert_called_once_with()
        mock_job_metadata.assert_called_once_with(
            mock_get_or_create_job_id.return_value
        )
        assert 1 == len(caplog.records)
        assert (
            "Could not collect job metadata to start benchmark"
            in caplog.records[0].message
        )

    def test_start_raises_emit(
        self, mocker, monkeypatch, benchmark_klio_pipeline_df, caplog
    ):
        mock_get_or_create_job_id = mocker.Mock(return_value="deadbeef")
        monkeypatch.setattr(
            benchmark_klio_pipeline_df,
            "_get_or_create_job_id",
            mock_get_or_create_job_id,
        )
        job_metadata = {
            "job_name": "test-job",
            "started_at": "2021-01-01 12:34:56.000000 UTC",
            "benchmark_job_id": "deadbeef",
            "benchmark_run_id": None,
            "benchmark_dataset_id": "foo.bar.baz",
            "environment": {},
            "vCPU_count": 40,
            "is_dataflow": True,
            "is_streaming": True,
            "gcp_project": "test-project",
            "dataflow_metadata": {
                "dataflow_job_id": "d4t4fl0w-j0b-1d",
                "machine_type": "n1-standard-4",
                "num_workers": 10,
                "max_num_workers": None,
                "autoscaling_on": False,
                "disk_type": "pd-ssd",
                "region": "boonies",
                "experiments": ["foo-exp", "bar-exp"],
                "number_of_worker_harness_threads": 1,
            },
        }
        mock_job_metadata = mocker.Mock(return_value=job_metadata)
        monkeypatch.setattr(
            benchmark_klio_pipeline_df, "_get_job_metadata", mock_job_metadata
        )
        mock_emit_job_metadata = mocker.Mock(side_effect=Exception("fuu"))
        monkeypatch.setattr(
            benchmark_klio_pipeline_df,
            "_emit_job_metadata",
            mock_emit_job_metadata,
        )

        with pytest.raises(SystemExit):
            benchmark_klio_pipeline_df.start()

        mock_get_or_create_job_id.assert_called_once_with()
        mock_job_metadata.assert_called_once_with(
            mock_get_or_create_job_id.return_value
        )
        assert 1 == len(caplog.records)
        assert (
            "Could not emit benchmark metadata for job. "
            in caplog.records[0].message
        )

    @pytest.mark.parametrize(
        "skip_deploy,exp_run_id", ((False, "1234"), (True, "deadbeef"),)
    )
    def test_get_run_id(self, skip_deploy, exp_run_id, mocker, monkeypatch):
        mock_uuid = mocker.Mock(return_value="1234")
        monkeypatch.setattr(benchmark.uuid, "uuid4", mock_uuid)
        mock_klio_conf = mocker.Mock()
        image = "gcr.io/foo/bar"
        image_tag = "image-tag"
        mock_klio_conf.pipeline_options.worker_harness_container_image = image
        mock_from_env = mocker.Mock()
        mock_docker_client = mock_from_env.return_value
        klio_job_yaml = """
        job_name: foo
        job_config:
          benchmark:
            run_id: deadbeef
        """
        mock_docker_client.containers.run.return_value = klio_job_yaml
        monkeypatch.setattr(benchmark.docker, "from_env", mock_from_env)

        BmPipeline = benchmark.BenchmarkKlioPipeline
        act_run_id = BmPipeline.get_run_id(
            skip_deploy, mock_klio_conf, image_tag
        )

        assert exp_run_id == act_run_id

        if skip_deploy is False:
            mock_uuid.assert_called_once_with()
            mock_from_env.assert_not_called()
        else:
            mock_uuid.assert_not_called()
            mock_from_env.assert_called_once_with()
            exp_run_flags = {
                "image": f"{image}:{image_tag}",
                "entrypoint": "bash",
                "command": [
                    "-c",
                    "cat /usr/src/app/klio-job-run-effective.yaml",
                ],
            }
            mock_docker_client.containers.run.assert_called_once_with(
                **exp_run_flags
            )

    @pytest.mark.parametrize(
        "dataset,exp_ret",
        (("foo.bar.baz", "foo.bar.baz"), ("foo:bar.baz", "foo.bar.baz"),),
    )
    def test_get_and_validate_dataset(
        self, dataset, exp_ret, mocker, monkeypatch
    ):
        """Happy path - dataset is valid"""
        mock_bq = mocker.Mock()
        monkeypatch.setattr(benchmark.discovery, "build", mock_bq)
        klio_config = mocker.Mock()
        assert exp_ret == get_and_validate_dataset(klio_config, dataset)

    def test_get_and_validate_dataset_batch(self, mocker, monkeypatch):
        """Happy path - configured dataset is valid"""
        mock_bq = mocker.Mock()
        monkeypatch.setattr(benchmark.discovery, "build", mock_bq)
        klio_config = mocker.Mock()
        klio_config.pipeline_options.streaming = False
        mock_event_input = mocker.Mock(
            project="foo", dataset="bar", table="baz"
        )
        klio_config.job_config.events.inputs = [mock_event_input]
        assert "foo.bar.baz" == get_and_validate_dataset(klio_config, None)

    def test_get_and_validate_dataset_streaming_raises(self, mocker, caplog):
        """Raise when --benchmark-dataset isn't provided when streaming."""
        klio_config = mocker.Mock()
        klio_config.pipeline_options.streaming = True

        with pytest.raises(SystemExit):
            get_and_validate_dataset(klio_config, None)

        assert (
            "Must configure a benchmarking dataset"
            in caplog.records[0].message
        )

    @pytest.mark.parametrize(
        "project,dataset,table",
        (
            (None, None, None),
            ("foo", None, None),
            ("foo", "bar", None),
            ("foo", None, "baz"),
            (None, "bar", None),
            (None, "bar", "baz"),
            (None, None, "baz"),
        ),
    )
    def test_get_and_validate_dataset_batch_raises(
        self, project, dataset, table, mocker, caplog
    ):
        """Raise when dataset isn't configured for batch"""
        klio_config = mocker.Mock()
        klio_config.pipeline_options.streaming = False
        mock_event_input = mocker.Mock(
            project=project, dataset=dataset, table=table
        )
        klio_config.job_config.events.inputs = [mock_event_input]

        with pytest.raises(SystemExit):
            get_and_validate_dataset(klio_config, None)

        assert (
            "Cannot determine the benchmarking " in caplog.records[0].message
        )

    @pytest.mark.parametrize(
        "input_dataset", ("foo", "foo.bar", "foo.bar.baz.bla")
    )
    def test_get_and_validate_dataset_invalid_str(
        self, input_dataset, mocker, caplog
    ):
        """Raise when dataset's string doesn't have three parts."""
        klio_config = mocker.Mock()
        klio_config.pipeline_options.streaming = True

        with pytest.raises(SystemExit):
            get_and_validate_dataset(klio_config, input_dataset)

        assert "Invalid benchmarking dataset " in caplog.records[0].message

    def test_get_and_validate_dataset_client_raises(
        self, mocker, monkeypatch, caplog
    ):
        mock_bq = mocker.MagicMock()
        mock_req = mock_bq().tables().get()
        mock_req.execute.side_effect = Exception("not found")
        monkeypatch.setattr(benchmark.discovery, "build", mock_bq)
        klio_config = mocker.Mock()

        input_dataset = "foo.bar.baz"
        with pytest.raises(SystemExit):
            get_and_validate_dataset(klio_config, input_dataset)
        assert "was not found" in caplog.records[0].message
