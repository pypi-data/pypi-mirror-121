# Copyright 2021 Spotify AB

from unittest import mock

import pytest
from google.cloud import bigquery

from klio_core import config

from spotify_klio_cli.commands.job import publisher


@pytest.fixture
def klio_config():
    conf = {
        "job_name": "test-job",
        "pipeline_options": {
            "worker_harness_container_image": (
                "gcr.io/sigint/gke-baseline-random-music-gke"
            ),
            "region": "some-region",
            "project": "test-project",
        },
        "job_config": {
            "events": {
                "inputs": [
                    {
                        "type": "pubsub",
                        "topic": "projects/sigint/topics/foo-topic",
                        "subscription": "foo-sub",
                    }
                ]
            },
        },
    }
    return config.KlioConfig(conf)


@pytest.fixture
def uris():
    return [
        "spotify:episode:45h7rggVBoRwJPKpRNFzsn",
        "spotify:episode:2kTRMFJWhU2eGRsF5E90br",
        "spotify:episode:12ccUt25aT7wmf70LgYxkn",
        "spotify:episode:1tiBoz0BPd58V7N71wnpD3",
        "spotify:episode:3Dl17uUqfPbkGjPPJ2hW11",
    ]


@pytest.fixture
def records(uris):
    return list([bigquery.table.Row((uri,), {"uri": 0}) for uri in uris])


def test_fetch_dataset(mocker, monkeypatch, records):
    mock_query_job = mock.Mock()
    mock_query_job.result.return_value = records
    run_job_config = mocker.Mock()
    p = publisher.KlioDatasetPublisher(job_config=run_job_config)
    mock_bq = mocker.Mock()
    mock_bq.query.return_value = mock_query_job
    monkeypatch.setattr(p, "_bq_client", mock_bq)
    results = p._fetch_dataset_data("some-dataset")
    mock_bq.query.assert_called_once()
    assert results == records


def test_publish_messages(mocker, monkeypatch, klio_config, records, uris):
    full_topic = klio_config.job_config.events.inputs[0].topic
    message_sent_callback = mocker.Mock()
    mock_query_job = mock.Mock()
    mock_query_job.result.return_value = records
    mock_bq = mocker.Mock()
    mock_bq.query.return_value = mock_query_job
    mock_publisher = mocker.Mock()
    p = publisher.KlioDatasetPublisher(job_config=klio_config)
    monkeypatch.setattr(p, "_bq_client", mock_bq)
    monkeypatch.setattr(p, "_publisher", mock_publisher)
    monkeypatch.setattr(p, "message_sent_callback", message_sent_callback)
    p.publish_messages("some-dataset")
    publish_calls = []
    for uri in uris:
        msg = p._create_klio_message(uri)
        publish_calls.append(mocker.call(full_topic, data=msg))
        publish_calls.append(
            mocker.call().add_done_callback(message_sent_callback)
        )
    mock_publisher.publish.assert_has_calls(publish_calls, any_order=True)
