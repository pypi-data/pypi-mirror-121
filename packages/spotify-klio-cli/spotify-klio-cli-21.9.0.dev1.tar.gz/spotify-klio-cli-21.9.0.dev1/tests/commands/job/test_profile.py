# Copyright 2020 Spotify AB

import pytest
from google.cloud import bigquery

from spotify_klio_cli.commands.job import profile
from spotify_klio_cli.commands.job import profile_queries


def test_generate_entities(mocker, monkeypatch):
    fake_result = [
        "a-file-id-1",
        "a-file-id-2",
        "a-file-id-3",
        "a-file-id-4",
        "a-file-id-5",
    ]

    mock_run_query = mocker.Mock()
    mock_run_query.return_value = fake_result
    monkeypatch.setattr(profile, "run_query", mock_run_query)
    expected_query_string = profile_queries.track_query(
        "transcoding.fileId", 30, 600, 5
    )

    results = profile.generate_entities(30, 600, 5, "file_id")
    assert 5 == len(results)
    assert "a-file-id-1" == results[0]
    mock_run_query.assert_called_once_with(expected_query_string, "file_id")


def test_run_query(mocker, monkeypatch):
    fake_result = [bigquery.Row(("a-file-id-1",), {"fileId": 0})]

    mock_client_constructor = mocker.Mock()
    mock_client = mock_client_constructor.return_value
    mock_query = mock_client.query.return_value
    mock_query.result.return_value = fake_result
    monkeypatch.setattr(bigquery, "Client", mock_client_constructor)

    results = profile.run_query("a-query-string", "file_id")
    assert 1 == len(results)
    assert "a-file-id-1" == results[0]
    mock_client_constructor.assert_called_once_with()
    mock_client.query.assert_called_once_with("a-query-string")
    mock_query.result.assert_called_once_with()


def test_run_query_fails_raises_exceptions(mocker, monkeypatch):
    mock_client_constructor = mocker.Mock()
    mock_client = mock_client_constructor.return_value
    mock_query = mock_client.query.return_value
    mock_query.result.side_effect = Exception("an-error")
    monkeypatch.setattr(bigquery, "Client", mock_client_constructor)

    with pytest.raises(SystemExit):
        profile.run_query("a-query-string", "file_id")


@pytest.mark.parametrize(
    "requested_format,row,expected",
    [
        ("file_id", bigquery.Row(("abc123",), {"fileId": 0}), "abc123"),
        (
            "audio_uri",
            bigquery.Row(("spotify:audio:9876",), {"audioUri": 0}),
            "spotify:audio:9876",
        ),
        (
            "audio_id",
            bigquery.Row(("spotify:audio:9876",), {"audioUri": 0}),
            "9876",
        ),
        (
            "track_uri",
            bigquery.Row(("spotify:track:12345",), {"track_uri": 0}),
            "spotify:track:12345",
        ),
        (
            "track_id",
            bigquery.Row(("spotify:track:12345",), {"track_uri": 0}),
            "12345",
        ),
        ("track_gid", bigquery.Row(("456def",), {"track_gid": 0}), "456def"),
    ],
)
def test_parse_to_format(requested_format, row, expected):
    assert expected == profile._parse_to_format(row, requested_format)


@pytest.mark.parametrize(
    "requested_format,expected",
    [
        ("file_id", "transcoding.fileId"),
        ("audio_uri", "track_entity.audioRelation.audio.uri as audioUri"),
        ("audio_id", "track_entity.audioRelation.audio.uri as audioUri"),
        ("track_uri", "track_uri"),
        ("track_id", "track_uri"),
        ("track_gid", "track_gid"),
    ],
)
def test_convert_format(requested_format, expected):
    assert expected == profile._convert_format(requested_format)
