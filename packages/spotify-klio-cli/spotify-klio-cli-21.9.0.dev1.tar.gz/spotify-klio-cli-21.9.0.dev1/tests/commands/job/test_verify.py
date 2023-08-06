# Copyright 2020 Spotify AB

import logging

import pytest

from klio_cli.commands.job import verify
from klio_core import config as kconfig

from spotify_klio_cli.commands.job import verify as sverify
from spotify_klio_cli.commands.job.verify import SpotifyVerifyJob


@pytest.fixture
def mock_storage(mocker):
    return mocker.patch.object(verify.storage, "Client")


@pytest.fixture
def mock_bucket(mocker):
    return mocker.patch.object(verify.storage.Client, "bucket")


@pytest.fixture
def config():
    return {
        "version": 2,
        "job_name": "klio-job-name",
        "job_config": {"events": {}, "data": {}},
        "pipeline_options": {
            "streaming": True,
            "worker_harness_container_image": "a-worker-image",
            "experiments": ["beam_fn_api"],
            "project": "test-gcp-project",
            "zone": "europe-west1-c",
            "region": "europe-west1",
            "staging_location": "gs://test-gcp-project-dataflow-tmp/staging",
            "temp_location": "gs://test-gcp-project-dataflow-tmp/temp",
            "max_num_workers": 2,
            "autoscaling_algorithm": "NONE",
            "disk_size_gb": 32,
            "worker_machine_type": "n1-standard-2",
            "runner": "DataflowRunner",
        },
    }


@pytest.fixture
def klio_config(config):
    return kconfig.KlioConfig(config)


def test_add_tingle_access(mock_storage, mocker, klio_config, caplog):
    tingle = "build-agent-mounter@xpn-tingle-1.iam.gserviceaccount.com"
    tingle_sa = "serviceAccount:{}".format(tingle)

    client = mock_storage.return_value
    mock_bucket = mocker.Mock()
    mock_bucket.get_iam_policy.return_value = {}
    client.get_bucket.return_value = mock_bucket

    job = SpotifyVerifyJob(klio_config, False)
    job._storage_client = client
    job._add_tingle_access("test-bucket")

    client.get_bucket.assert_called_once_with("test-bucket")
    mock_bucket.get_iam_policy.assert_called_once_with()
    mock_bucket.set_iam_policy.assert_called_once_with(
        {"roles/storage.objectViewer": {tingle_sa}}
    )
    assert 1 == len(caplog.records)


def test_add_tingle_access_raises(mock_storage, mocker, klio_config, caplog):
    client = mock_storage.return_value
    mock_bucket = mocker.Mock()
    client.get_bucket.return_value = mock_bucket
    mock_bucket.get_iam_policy.side_effect = Exception("foo")

    job = SpotifyVerifyJob(klio_config, False)
    job._storage_client = client

    with pytest.raises(SystemExit):
        job._add_tingle_access("test-bucket")

    client.get_bucket.assert_called_once_with("test-bucket")
    mock_bucket.set_iam_policy.assert_not_called()
    assert 2 == len(caplog.records)


@pytest.mark.parametrize(
    "create_resources, verified_tingle",
    ((True, True), (False, False), (False, True), (True, False)),
)
def test_confirm_tingle_access(
    klio_config,
    mocker,
    mock_bucket,
    create_resources,
    mock_storage,
    verified_tingle,
):
    mock_policy = mocker.patch.object(mock_bucket, "get_iam_policy")
    tingle_sa = (
        "serviceAccount:build-agent-mounter"
        "@xpn-tingle-1.iam.gserviceaccount.com"
    )
    if verified_tingle:
        mock_policy.return_value = {
            "roles/storage.objectViewer": {
                "serviceAccount:build-agent-mounter"
                "@xpn-tingle-1.iam.gserviceaccount.com"
            }
        }
        expected = True
    else:
        mock_policy.return_value = {"roles/storage.objectViewer": {}}
        if create_resources:
            expected = True
        else:
            expected = False

    job = SpotifyVerifyJob(klio_config, create_resources)
    job._storage_client = mock_storage
    actual = job._confirm_tingle_access(tingle_sa, mock_bucket)
    assert expected == actual


def test_confirm_tingle_access_handle_sysexit(
    klio_config, mocker, monkeypatch, mock_bucket, mock_storage
):
    tingle_sa = (
        "serviceAccount:build-agent-mounter"
        "@xpn-tingle-1.iam.gserviceaccount.com"
    )

    job = SpotifyVerifyJob(klio_config, True)
    mock_add_tingle_access = mocker.Mock(side_effect=SystemExit(1))
    monkeypatch.setattr(job, "_add_tingle_access", mock_add_tingle_access)

    job._storage_client = mock_storage
    assert job._confirm_tingle_access(tingle_sa, mock_bucket) is False


@pytest.mark.parametrize("verified", (True, False))
def test_verify_tingle_access(mocker, mock_storage, klio_config, verified):
    job = SpotifyVerifyJob(klio_config, True)
    job._storage_client = mock_storage
    job.klio_config.job_name = "test-job"
    mock_confirm_tingle = mocker.patch.object(job, "_confirm_tingle_access")
    mock_verify_bucket = mocker.patch.object(job, "_verify_gcs_bucket")
    if verified:
        mock_verify_bucket.return_value = True
        mock_confirm_tingle.return_value = True
        actual = job._verify_tingle_access()
        assert actual is True
    else:
        mock_verify_bucket.return_value = False
        actual = job._verify_tingle_access()
        assert actual is False


@pytest.mark.parametrize(
    "verified_all, verified_tingle",
    ((True, True), (False, True), (True, False), (False, False)),
)
def test_verify(
    mocker, klio_config, mock_storage, caplog, verified_all, verified_tingle
):
    caplog.set_level(logging.INFO)
    mock_verify_all = mocker.patch.object(sverify.VerifyJob, "_verify_all")
    job = SpotifyVerifyJob(klio_config, False)
    job._storage_client = mock_storage
    mock_verify_tingle = mocker.patch.object(job, "_verify_tingle_access")

    mock_storage.return_value = mock_storage

    mock_verify_tingle.return_value = verified_all
    mock_verify_all.return_value = verified_tingle

    if not all([verified_all, verified_tingle]):
        with pytest.raises(SystemExit) as pytest_wrapped_verify_job:
            job.verify_job()
        assert pytest_wrapped_verify_job.type == SystemExit
        assert pytest_wrapped_verify_job.value.code == 1
    else:
        job.verify_job()
        assert 1 == len(caplog.records)

    assert mock_verify_tingle.called
    assert mock_verify_all.called
