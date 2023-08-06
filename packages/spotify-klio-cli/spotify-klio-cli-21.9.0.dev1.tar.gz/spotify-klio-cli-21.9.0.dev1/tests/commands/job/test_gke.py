# Copyright 2021 Spotify AB

import pytest

from klio_core import config

from spotify_klio_cli import cli
from spotify_klio_cli.commands.job import gke


@pytest.fixture
def klio_config():
    conf = {
        "job_name": "test-job",
        "version": 1,
        "pipeline_options": {
            "worker_harness_container_image": (
                "gcr.io/sigint/gke-baseline-random-music-gke"
            ),
            "region": "some-region",
            "project": "test-project",
            "runner": "DirectGKERunner",
        },
        "job_config": {
            "inputs": [
                {
                    "topic": "foo-topic",
                    "subscription": "foo-sub",
                    "data_location": "foo-input-location",
                }
            ],
            "outputs": [
                {
                    "topic": "foo-topic-output",
                    "data_location": "foo-output-location",
                }
            ],
        },
    }
    return config.KlioConfig(conf)


def test_gke_run_pipeline(klio_config, mocker):
    sp_run_job_config = cli.SpotifyRunJobConfig(xpn=True)
    runtime_config = mocker.Mock()
    run_job_config = mocker.Mock()

    klio_pipeline = gke.SpotifyRunPipelineGKE(
        job_dir="/test/dir/jobs/",
        klio_config=klio_config,
        docker_runtime_config=runtime_config,
        run_job_config=run_job_config,
        sp_run_job_config=sp_run_job_config,
    )

    assert sp_run_job_config == klio_pipeline.sp_run_job_config
    assert isinstance(klio_pipeline, gke.gke.RunPipelineGKE)
