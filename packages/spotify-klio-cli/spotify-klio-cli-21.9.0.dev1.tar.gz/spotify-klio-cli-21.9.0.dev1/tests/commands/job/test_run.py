# Copyright 2020 Spotify AB

import pytest

from spotify_klio_cli import cli
from spotify_klio_cli.commands.job import run


@pytest.fixture
def config():
    return {
        "job_name": "test-job",
        "worker_harness_container_image": "gcr.io/test-project/my-job-image",
        "region": "us-central5",
        "project": "test-project",
    }


@pytest.mark.parametrize(
    "xpn,exp_flag", ((True, ["--xpn"]), (False, ["--no-xpn"]), (None, []))
)
def test_get_command(xpn, exp_flag, config):
    runtime_conf = cli.cli.DockerRuntimeConfig(
        image_tag="foo", force_build=False, config_file_override=None,
    )
    run_job_conf = cli.cli.RunJobConfig(
        direct_runner=False, update=None, git_sha="12345678",
    )
    sp_run_job_conf = cli.SpotifyRunJobConfig(xpn=xpn)

    kpipe = run.SpotifyRunPipeline(
        "job-dir", config, runtime_conf, run_job_conf, sp_run_job_conf
    )
    act_command = kpipe._get_command()

    exp_command = ["run", "--image-tag", "foo"]
    exp_command.extend(exp_flag)

    assert exp_command == act_command
