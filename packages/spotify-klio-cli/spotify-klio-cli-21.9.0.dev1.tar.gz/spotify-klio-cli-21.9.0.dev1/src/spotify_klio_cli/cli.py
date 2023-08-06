# Copyright 2020 Spotify AB

import collections
import logging

import click
import yaml

from klio_cli import cli
from klio_cli import options
from klio_cli.cli import main
from klio_cli.commands.job import configuration
from klio_cli.utils import cli_utils
from klio_core import options as core_options
from klio_core import utils as core_utils
from klio_core import variables as var

from spotify_klio_cli import cli_utils as sp_cli_utils
from spotify_klio_cli.commands.job import benchmark
from spotify_klio_cli.commands.job import publisher
from spotify_klio_cli.commands.job import run
from spotify_klio_cli.commands.job import verify

SpotifyRunJobConfig = collections.namedtuple("SpotifyRunJobConfig", ["xpn"])
SpotifyBenchmarkJobConfig = collections.namedtuple(
    "SpotifyBenchmarkJobConfig",
    ["dataset", "enabled", "job_id", "run_id", "metadata_topic", "data_topic"],
)


@cli.profile.command(
    "generate-entities",
    help="Generate a list of entity ids to profile a job with",
)
@core_options.config_file
@click.option(
    "-o",
    "--output-file",
    type=click.Path(exists=False, dir_okay=False, writable=True),
    default=None,
    show_default="stdout",
    help="Output file for results.",
)
@click.option(
    "--track-min-length",
    type=int,
    default=30,
    help="Minimum track length, in seconds. Defaults to 30.",
)
@click.option(
    "--track-max-length",
    type=int,
    default=600,
    help="Maximum track length, in seconds. Defaults to 600.",
)
@click.option(
    "--number-of-tracks",
    type=int,
    default=10,
    help="Number of tracks. Defaults to 10.",
)
@click.option(
    "--requested-format",
    type=click.Choice(
        [
            "file_id",
            "audio_uri",
            "audio_id",
            "track_uri",
            "track_id",
            "track_gid",
        ]
    ),
)
def generate_profile_entities(
    output_file,
    config_file,
    track_min_length,
    track_max_length,
    number_of_tracks,
    requested_format,
):
    from spotify_klio_cli.commands.job import profile as profile_helper

    if not requested_format:
        requested_format = "track_uri"
    if not config_file:
        click.echo("Running query ...")
        entity_ids = profile_helper.generate_entities(
            track_min_length,
            track_max_length,
            number_of_tracks,
            requested_format,
        )
    else:
        query_key = "query_for_test_data"
        config_data = core_utils.get_config_by_path(config_file)
        if query_key not in config_data.get("job_config", {}).keys():
            raise click.UsageError(
                "No query_for_test_data string found in {}".format(config_file)
            )
        query_string = config_data["job_config"]["query_for_test_data"]

        click.echo("Running query from {}...".format(config_file))
        entity_ids = profile_helper.run_query(query_string, None)

    with sp_cli_utils.smart_open(output_file, fmode="w") as f:
        f.write("\n".join(entity_ids))


@cli.job.command("run", help="Run a klio job.")
@core_options.image_tag
@options.runtime
@click.option(
    "--xpn/--no-xpn",
    default=True,
    is_flag=True,
    help=(
        "Enable/disable XPN for runtime. Default: True. XPN is not needed "
        "for Dockerized pipelines that do not interact with internal Spotify "
        "services."
    ),
)
@click.option(
    "--benchmark",
    default=False,
    is_flag=True,
    help=(
        "Run this job in benchmark mode. This flag is not needed if any other "
        "benchmark flag is used."
    ),
)
@click.option(
    "--benchmark-skip-deploy",
    default=False,
    is_flag=True,
    help=(
        "Skip deploying the job and just emit the job's benchmarking "
        "metadata."
    ),
)
@click.option(
    "--publish",
    default=False,
    is_flag=True,
    help=("Should skip publishing Klio messages to job."),
)
@click.option(
    "--publish-message-count",
    default=None,
    help=("Number of records from dataset this job will publish."),
)
@core_utils.with_klio_config
def run_sp_job(klio_config, config_meta, **kwargs):
    """Overrides `klio job run` to support easy enabling of XPN."""
    job_dir = config_meta.job_dir
    config_file = config_meta.config_file

    sp_cli_utils.has_internal_executor(job_dir)

    direct_runner = cli_utils.is_direct_runner(
        klio_config, kwargs.pop("direct_runner")
    )

    git_sha = cli_utils.get_git_sha(job_dir, kwargs.get("image_tag"))
    image_tag = kwargs.get("image_tag") or git_sha

    runtime_config = cli.DockerRuntimeConfig(
        image_tag=image_tag,
        force_build=kwargs.get("force_build"),
        config_file_override=config_file,
    )
    run_job_config = cli.RunJobConfig(
        direct_runner=direct_runner,
        update=kwargs.pop("update"),
        git_sha=git_sha,
    )
    sp_run_job_config = SpotifyRunJobConfig(xpn=kwargs.pop("xpn"))

    skip_deploy = kwargs["benchmark_skip_deploy"]
    bm_job_config = klio_config.job_config.as_dict().get("benchmark")
    # CLI flag `--benchmark` will override enable flag
    bm_job_config = bm_job_config if bm_job_config else {}
    if kwargs["benchmark"] is True:
        bm_job_config["enabled"] = True
    skip_deploy = (
        skip_deploy
        if skip_deploy is True
        else bm_job_config.get("skip_deploy", False)
    )
    if bm_job_config.get("run_id") is None:
        bm_job_config["run_id"] = benchmark.BenchmarkKlioPipeline.get_run_id(
            skip_deploy, klio_config, image_tag
        )
    should_benchmark = bm_job_config.get("enabled")
    if should_benchmark:
        bm_job_config[
            "dataset"
        ] = benchmark.BenchmarkKlioPipeline.get_and_validate_dataset(
            klio_config, bm_job_config.get("dataset")
        )
    benchmark_config = SpotifyBenchmarkJobConfig(
        dataset=bm_job_config.get("dataset"),
        enabled=bm_job_config.get("enabled"),
        job_id=bm_job_config.get("job_id"),
        run_id=bm_job_config.get("run_id"),
        metadata_topic=bm_job_config.get("metadata_topic"),
        data_topic=bm_job_config.get("data_topic"),
    )
    # Generate a new run_id if one is not already there
    # Now update klio config object in 2 spots for future handling:
    # (1) on the klio_config object, so we can access later
    effective_bm_config = dict(benchmark_config._asdict())
    setattr(klio_config.job_config, "benchmark", effective_bm_config)
    # (2) in user attributes so it gets included when generating
    # the klio-job-run-effective.yaml
    bm_job_config_dict = {"benchmark": effective_bm_config}
    klio_config.job_config.USER_ATTRIBS.append(bm_job_config_dict)

    if should_benchmark:

        if not skip_deploy:
            # benchmarking updates klio config object, and therefore the
            # regenerated klio-job-run-effective.yaml needs to be included
            # in the deployed image so we force build
            runtime_config = runtime_config._replace(force_build=True)

    if (
        not direct_runner
        and klio_config.pipeline_options.runner
        == var.KlioRunner.DIRECT_GKE_RUNNER
    ):
        gke_commands = sp_cli_utils.import_sp_gke_commands()
        RunPipelineKlass = gke_commands.SpotifyRunPipelineGKE

    else:
        RunPipelineKlass = run.SpotifyRunPipeline

    klio_pipeline = RunPipelineKlass(
        job_dir, klio_config, runtime_config, run_job_config, sp_run_job_config
    )

    if skip_deploy is False:
        klio_pipeline.run()

    if should_benchmark:
        benchmark_run = benchmark.BenchmarkKlioPipeline(
            job_dir,
            klio_config,
            klio_pipeline._full_image_name,
            benchmark_config,
        )
        benchmark_run.start()

    # TODO: Check that benchmark / job deploy was successful?
    # (for streaming jobs)? we'd probably have to wait a few minutes for
    # a streaming dataflow job to warm up
    should_publish = publisher.KlioDatasetPublisher.should_publish(
        klio_config, benchmark_config.dataset, kwargs
    )
    if should_publish:
        num_messages = kwargs["publish_message_count"]
        num_messages = num_messages if num_messages is not None else 500000
        p = publisher.KlioDatasetPublisher(klio_config)
        p.publish_messages(
            benchmark_config.dataset, message_count=num_messages
        )


@cli.job.command(
    "create",
    short_help="DEPRECATED - use Backstage 'Create Component'.",
    help=(
        "DEPRECATED. Use the Klio Streaming Skeleton in Backstage to create a "
        "new job at `https://backstage.spotify.net/create-component/klio-"
        "streaming-skeleton`."
    ),
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
        allow_interspersed_args=True,
    ),
)
def create_sp_job(*args, **kwargs):
    click.secho("This command has been deprecated!", fg="yellow")
    click.secho(
        "Use the Klio Streaming Skeleton in Backstage to create a new job "
        "at `https://backstage.spotify.net/create-component/klio-streaming-"
        "skeleton`."
    )
    raise SystemExit(1)


@cli.job.command(
    "verify",
    short_help="Verify a job's required GCP resources exist.",
    help=(
        "Verifies all GCP resources and dependencies used in the job "
        "so that the Klio Job as defined in the 'klio-info.yaml' can run "
        "properly in production."
    ),
)
@options.create_resources
@core_utils.with_klio_config
def verify_sp_job(klio_config, config_meta, create_resources):
    job = verify.SpotifyVerifyJob(klio_config, create_resources)
    job.verify_job()


@cli.job.command(
    "convert-v1-config",
    short_help="Convert v1 config to v2.",
    help=(
        "Transforms a v1 config file to be compatible with klio v2 and "
        "overwrites the existing config file."
    ),
)
@core_options.job_dir
@core_options.config_file
def convert_v1_config(job_dir, config_file):
    job_dir, config_path = core_utils.get_config_job_dir(job_dir, config_file)

    effective_config = sp_cli_utils.lift_v1_config(
        core_utils.get_config_by_path(config_path), False
    )
    with open(config_path, "w") as f:
        yaml.dump(
            effective_config,
            stream=f,
            Dumper=configuration.IndentListDumper,
            default_flow_style=False,
            sort_keys=False,
        )
    logging.info("Config file successfully updated")


if __name__ == "__main__":
    main()
