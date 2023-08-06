# Copyright 2020 Spotify AB

import os
from unittest import mock

import click
import pytest
from _pytest.monkeypatch import MonkeyPatch
from click import testing

from klio_cli.utils import cli_utils
from klio_core import _testing as core_testing
from klio_core import utils as core_utils

from spotify_klio_cli import cli  # noqa: E402
from spotify_klio_cli import cli_utils as sp_cli_utils  # noqa E402
from spotify_klio_cli.commands.job import gke
from spotify_klio_cli.commands.job import profile  # noqa: E402
from spotify_klio_cli.commands.job import run
from spotify_klio_cli.commands.job import verify

# NOTE: Because `klio_cli.options.image_tag` is a decorator, and
#       decorators get "executed" upon import – and therefore attaches
#       `klio_cli.cli_utils.get_git_sha` to the option's default (it doesn't
#       execute that function, just imports it) – we have to patch cli_utils
#       before we import `spotify_klio_cli.cli` which is the code that
#       uses it. See https://stackoverflow.com/a/7667621/1579977
mock_get_git_sha = mock.Mock()
_patch_git_sha = MonkeyPatch()
_patch_git_sha.setattr(cli_utils, "get_git_sha", mock_get_git_sha)


@pytest.fixture
def mock_klio_config(mocker, monkeypatch, patch_os_getcwd):
    return core_testing.MockKlioConfig(
        cli, mocker, monkeypatch, patch_os_getcwd
    )


@pytest.fixture
def runner():
    return testing.CliRunner()


@pytest.fixture
def mock_klio_pipeline(mocker, monkeypatch):
    mock = mocker.Mock()
    monkeypatch.setattr(cli.run, "SpotifyRunPipeline", mock)
    return mock


@pytest.fixture
def patch_os_getcwd(monkeypatch, tmpdir):
    test_dir = str(tmpdir.mkdir("testing"))
    monkeypatch.setattr(os, "getcwd", lambda: test_dir)
    return test_dir


@pytest.fixture
def config_file(patch_os_getcwd):
    conf = os.path.join(patch_os_getcwd, "klio-job.yaml")
    return conf


@pytest.fixture
def mock_warn_if_py2_job(mocker, monkeypatch):
    mock = mocker.Mock()
    monkeypatch.setattr(cli.core_utils, "warn_if_py2_job", mock)
    return mock


@pytest.fixture
def mock_get_config_job_dir(mocker, monkeypatch):
    mock = mocker.Mock()
    monkeypatch.setattr(cli.core_utils, "get_config_job_dir", mock)
    return mock


@pytest.fixture
def mock_has_internal_executor(mocker, monkeypatch):
    mock = mocker.Mock()
    monkeypatch.setattr(cli.sp_cli_utils, "has_internal_executor", mock)
    return mock


@pytest.fixture
def pipeline_config_dict():
    return {
        "project": "test-project",
        "staging_location": "gs://some/stage",
        "temp_location": "gs://some/temp",
        "worker_harness_container_image": "gcr.io/sigint/foo",
        "streaming": True,
        "update": False,
        "experiments": ["beam_fn_api"],
        "region": "us-central1",
        "num_workers": 3,
        "max_num_workers": 5,
        "disk_size_gb": 50,
        "worker_machine_type": "n1-standard-4",
    }


@pytest.mark.parametrize(
    "job_dir,image_tag,direct_runner,force_build,update,xpn,conf_override",
    (
        (None, None, None, None, None, None, None),
        ("jobs", "foobar", True, True, True, True, "klio-job2.yaml"),
    ),
)
def test_run_sp_job(
    job_dir,
    image_tag,
    direct_runner,
    force_build,
    update,
    xpn,
    config_file,
    conf_override,
    patch_os_getcwd,
    mock_klio_pipeline,
    mock_klio_config,
    mock_warn_if_py2_job,
    mock_has_internal_executor,
    runner,
):

    # Start of with option defaults
    exp_runtime_conf = cli.cli.DockerRuntimeConfig(
        image_tag=mock_get_git_sha.return_value,
        force_build=False,
        config_file_override=None,
    )
    exp_run_job_conf = cli.cli.RunJobConfig(
        direct_runner=False, update=None, git_sha=mock_get_git_sha.return_value
    )
    exp_sp_run_job_conf = cli.SpotifyRunJobConfig(xpn=True)

    config_data = {
        "job_name": "test-job",
        "version": 2,
        "job_config": {"events": {}, "data": {}},
        "pipeline_options": {
            "project": "test-project",
            "staging_location": "gs://foo/bar/staging",
            "temp_location": "gs://foo/bar/temp",
            "region": "us-central5",
        },
    }

    exp_job_dir = None

    cli_inputs = []
    if job_dir:
        cli_inputs.extend(["--job-dir", patch_os_getcwd])
        exp_job_dir = patch_os_getcwd
    if image_tag:
        cli_inputs.extend(["--image-tag", image_tag])
        exp_runtime_conf = exp_runtime_conf._replace(image_tag=image_tag)
    if direct_runner:
        cli_inputs.append("--direct-runner")
        exp_run_job_conf = exp_run_job_conf._replace(direct_runner=True)
    if force_build:
        cli_inputs.append("--force-build")
        exp_runtime_conf = exp_runtime_conf._replace(force_build=True)
    if update:
        cli_inputs.append("--update")
        exp_run_job_conf = exp_run_job_conf._replace(update=True)
    elif update is False:
        cli_inputs.append("--no-update")
        exp_run_job_conf = exp_run_job_conf._replace(update=False)
    if xpn:
        cli_inputs.append("--xpn")
        exp_sp_run_job_conf = exp_sp_run_job_conf._replace(xpn=True)
    elif xpn is False:
        cli_inputs.append("--no-xpn")
        exp_sp_run_job_conf = exp_sp_run_job_conf._replace(xpn=False)
    if conf_override:
        cli_inputs.extend(["--config-file", conf_override])
        exp_runtime_conf = exp_runtime_conf._replace(
            config_file_override=conf_override
        )
    mock_klio_config.setup(
        config_data, config_file, conf_override, exp_job_dir
    )
    result = runner.invoke(cli.run_sp_job, cli_inputs)

    core_testing.assert_execution_success(result)

    mock_klio_config.assert_calls()

    mock_has_internal_executor.assert_called_once_with(patch_os_getcwd)
    mock_klio_pipeline.assert_called_once_with(
        patch_os_getcwd,
        mock_klio_config.klio_config,
        exp_runtime_conf,
        exp_run_job_conf,
        exp_sp_run_job_conf,
    )
    mock_klio_pipeline.return_value.run.assert_called_once_with()


@pytest.mark.parametrize("direct_on_gke", (True, False))
def test_run_sp_job_gke(
    runner, mocker, monkeypatch, tmpdir, direct_on_gke, mock_klio_config,
):
    mock_has_internal_exec = mocker.Mock(return_value=True)
    monkeypatch.setattr(
        sp_cli_utils, "has_internal_executor", mock_has_internal_exec
    )

    config_data = {
        "job_name": "test-job",
        "pipeline_options": {
            "worker_harness_container_image": "gcr.register.io/squad/feature",
            "project": "test-project",
            "region": "boonies",
            "staging_location": "gs://somewhere/over/the/rainbow",
            "temp_location": "gs://somewhere/over/the/rainbow",
            "runner": "DirectGKERunner" if direct_on_gke else "DirectRunner",
        },
        "job_config": {"events": {}, "data": {}},
    }

    mock_klio_config.setup(config_data, None, None, None)
    mock_sp_run_pipeline = mocker.Mock()
    monkeypatch.setattr(run, "SpotifyRunPipeline", mock_sp_run_pipeline)
    mock_sp_run_pipeline_gke = mocker.Mock()
    monkeypatch.setattr(gke, "SpotifyRunPipelineGKE", mock_sp_run_pipeline_gke)

    cli_inputs = ["job", "run"]

    result = runner.invoke(cli.main, cli_inputs)

    core_testing.assert_execution_success(result)
    assert "" == result.output

    mock_klio_config.assert_calls()

    if direct_on_gke:
        mock_sp_run_pipeline_gke.return_value.run.assert_called_once_with()
        mock_sp_run_pipeline.return_value.run.assert_not_called()
    else:
        mock_sp_run_pipeline_gke.return_value.run.assert_not_called()
        mock_sp_run_pipeline.return_value.run.assert_called_once_with()


@pytest.mark.parametrize(
    "bm_flags,bm_config,should_bm",
    (
        ([], {"dataset": "foo.bar.baz", "enabled": False}, False),
        (["--benchmark"], {"dataset": "foo.bar.baz", "enabled": False}, True),
        ([], {}, False),
        ([], {"dataset": "foo.bar.baz", "enabled": True}, True),
    ),
)
def test_run_sp_job_benchmark(
    bm_flags,
    bm_config,
    should_bm,
    runner,
    mock_klio_config,
    patch_os_getcwd,
    mocker,
    monkeypatch,
):
    mock_has_internal_exec = mocker.Mock(return_value=True)
    monkeypatch.setattr(
        sp_cli_utils, "has_internal_executor", mock_has_internal_exec
    )

    config_data = {
        "job_name": "test-job",
        "pipeline_options": {
            "streaming": False,
            "worker_harness_container_image": "gcr.register.io/squad/feature",
            "project": "test-project",
            "region": "boonies",
            "staging_location": "gs://somewhere/over/the/rainbow",
            "temp_location": "gs://somewhere/over/the/rainbow",
            "runner": "DataflowRunner",
        },
        "job_config": {"events": {}, "data": {}},
    }
    if bm_config:
        config_data["job_config"]["benchmark"] = bm_config
    mock_klio_config.setup(config_data, None, None, None)
    mock_sp_run_pipeline = mocker.Mock()
    monkeypatch.setattr(run, "SpotifyRunPipeline", mock_sp_run_pipeline)
    mock_bm_pipeline = mocker.Mock(name="MockBenchmarkKlioPipeline")
    mock_bm_pipeline.get_run_id.return_value = (
        "496dcecb-5e1a-487a-b1b4-4562253502b2"
    )
    monkeypatch.setattr(
        cli.benchmark, "BenchmarkKlioPipeline", mock_bm_pipeline
    )
    monkeypatch.setattr(
        cli.benchmark.BenchmarkKlioPipeline,
        "get_and_validate_dataset",
        lambda x, y: bm_config["dataset"],
    )

    cli_inputs = ["job", "run"]
    cli_inputs.extend(bm_flags)

    result = runner.invoke(cli.main, cli_inputs)

    core_testing.assert_execution_success(result)
    assert "" == result.output

    mock_klio_config.assert_calls()

    if should_bm:
        exp_benchmark_config = cli.SpotifyBenchmarkJobConfig(
            dataset=bm_config["dataset"],
            enabled=True,
            job_id=None,
            run_id="496dcecb-5e1a-487a-b1b4-4562253502b2",
            metadata_topic=None,
            data_topic=None,
        )
        mock_bm_pipeline.assert_called_once_with(
            patch_os_getcwd,
            mock_klio_config.klio_config,
            mock_sp_run_pipeline.return_value._full_image_name,
            exp_benchmark_config,
        )
        mock_bm_pipeline.return_value.start.assert_called_once_with()
    else:
        mock_bm_pipeline.assert_not_called()
        mock_bm_pipeline.return_value.start.assert_not_called()


@pytest.mark.parametrize(
    "output_file,config_file,min_length,max_length,num_tracks,requested_format",
    (
        (None, None, None, None, None, "track_uri"),
        (None, None, 1, 1000, 100, "track_id"),
        (None, None, 1, 1000, 100, "track_uri"),
        ("an-output-file", None, 1, 1000, 100, None),
    ),
)
def test_profile_generate_without_config_file(
    output_file,
    config_file,
    min_length,
    max_length,
    num_tracks,
    requested_format,
    mocker,
    monkeypatch,
    runner,
    capsys,
):
    mock_generate = mocker.Mock()
    mock_generate.return_value = ["abc123", "def456", "ghi789"]
    monkeypatch.setattr(profile, "generate_entities", mock_generate)

    mock_write_function = mocker.Mock()
    mock_smart_open = mocker.patch.object(sp_cli_utils, "smart_open")
    mock_smart_open.return_value.__enter__.return_value.write = (
        mock_write_function
    )

    cli_inputs = [
        "--config-file",
        config_file,
        "--track-min-length",
        min_length,
        "--track-max-length",
        max_length,
        "--number-of-tracks",
        num_tracks,
        "--requested-format",
        requested_format,
    ]
    min_call = 30
    if min_length is not None:
        min_call = min_length
    max_call = 600
    if max_length is not None:
        max_call = max_length
    num_call = 10
    if num_tracks is not None:
        num_call = num_tracks
    requested_call = "track_uri"
    if requested_format is not None:
        requested_call = requested_format

    result = runner.invoke(cli.generate_profile_entities, cli_inputs)
    assert 0 == result.exit_code
    mock_generate.assert_called_once_with(
        min_call, max_call, num_call, requested_call
    )
    expected_string = "abc123\ndef456\nghi789"
    mock_write_function.assert_called_with(expected_string)


@pytest.mark.parametrize(
    "output_file,config_file,min_length,max_length,num_tracks,requested_format",
    (
        (None, "some-config.yaml", None, None, None, None),
        (None, "some-config.yaml", 1, 1000, 100, "track_id"),
    ),
)
def test_profile_generate_with_config_file(
    output_file,
    config_file,
    min_length,
    max_length,
    num_tracks,
    requested_format,
    mocker,
    monkeypatch,
    runner,
):
    mock_click_echo = mocker.Mock()
    monkeypatch.setattr(click, "echo", mock_click_echo)

    fake_config = {"job_config": {"query_for_test_data": "a-query-string"}}
    mock_get_config_by_path = mocker.Mock()
    mock_get_config_by_path.return_value = fake_config
    monkeypatch.setattr(
        core_utils, "get_config_by_path", mock_get_config_by_path
    )

    mock_run_query = mocker.Mock()
    mock_run_query.return_value = ["abc123", "def456", "ghi789"]
    monkeypatch.setattr(profile, "run_query", mock_run_query)

    mock_write_function = mocker.Mock()
    mock_smart_open = mocker.patch.object(sp_cli_utils, "smart_open")
    mock_smart_open.return_value.__enter__.return_value.write = (
        mock_write_function
    )

    cli_inputs = [
        "--config-file",
        config_file,
        "--track-min-length",
        min_length,
        "--track-max-length",
        max_length,
        "--number-of-tracks",
        num_tracks,
        "--requested-format",
        requested_format,
    ]
    result = runner.invoke(cli.generate_profile_entities, cli_inputs)
    assert 0 == result.exit_code
    mock_run_query.assert_called_once_with("a-query-string", None)
    expected_string = "abc123\ndef456\nghi789"
    mock_write_function.assert_called_with(expected_string)


@pytest.mark.parametrize(
    "config_file,min_length,max_length,num_tracks,requested_format",
    (
        ("some-config.yaml", None, None, None, None),
        ("some-config.yaml", 1, 1000, 100, "track_id"),
    ),
)
def test_profile_generate_with_config_file_missing_query(
    config_file,
    min_length,
    max_length,
    num_tracks,
    requested_format,
    mocker,
    monkeypatch,
    runner,
):
    mock_click_echo = mocker.Mock()
    monkeypatch.setattr(click, "echo", mock_click_echo)

    fake_config = {"job_config": {}}
    mock_get_config_by_path = mocker.Mock()
    mock_get_config_by_path.return_value = fake_config
    monkeypatch.setattr(
        core_utils, "get_config_by_path", mock_get_config_by_path
    )

    cli_inputs = ["--config-file", config_file]
    result = runner.invoke(cli.generate_profile_entities, cli_inputs)
    expected_error = (
        "Error: No query_for_test_data string found in some-config.yaml"
    )
    assert 2 == result.exit_code
    assert expected_error in result.output


def test_create_sp_job(runner):
    ret = runner.invoke(cli.create_sp_job, [])

    assert 1 == ret.exit_code
    assert "deprecated" in ret.output


@pytest.mark.parametrize(
    "create_resources,conf_override",
    (
        (False, None),
        (False, "klio-job2.yaml"),
        (True, None),
        (True, "klio-job2.yaml"),
    ),
)
def test_verify_sp_job(
    runner,
    mocker,
    patch_os_getcwd,
    create_resources,
    conf_override,
    mock_warn_if_py2_job,
    mock_get_config_job_dir,
):
    mock_verify_job = mocker.patch.object(
        verify.SpotifyVerifyJob, "verify_job"
    )
    mock_get_config_job_dir.return_value = (
        patch_os_getcwd,
        conf_override or config_file,
    )
    mock_get_config = mocker.patch.object(core_utils, "get_config_by_path")

    config = {
        "version": 2,
        "job_name": "klio-job-name",
        "job_config": {"events": {}, "data": {}},
        "pipeline_options": {},
    }
    mock_get_config.return_value = config

    cli_inputs = ["job", "verify"]
    if create_resources:
        cli_inputs.append("--create-resources")
    if conf_override:
        cli_inputs.extend(["--config-file", conf_override])

    result = runner.invoke(cli.main, cli_inputs)
    assert 0 == result.exit_code

    mock_get_config_job_dir.assert_called_once_with(None, conf_override)
    mock_get_config.assert_called_once_with(conf_override or config_file)
    mock_warn_if_py2_job.assert_called_once_with(patch_os_getcwd)
    mock_verify_job.assert_called_once_with()
