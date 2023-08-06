# Copyright 2020 Spotify AB

import logging

try:
    from google.cloud import bigquery
except ImportError:  # pragma: no cover
    logging.error(
        "Failed to import profiling dependencies. Did you install "
        "`spotify-klio-cli[debug]`?"
    )
    raise SystemExit(1)

from spotify_klio_cli.commands.job import profile_queries


def generate_entities(min_length, max_length, num_tracks, requested_format):
    query_format = _convert_format(requested_format)
    query_string = profile_queries.track_query(
        query_format, min_length, max_length, num_tracks
    )
    return run_query(query_string, requested_format)


def run_query(query_string, requested_format):
    client = bigquery.Client()
    job = client.query(query_string)
    try:
        result = job.result()
    except Exception:
        logging.error("Error querying for entities.", exc_info=True)
        raise SystemExit(1)
    return _parse(result, requested_format)


def _parse(result, requested_format):
    parsed_results = []
    for row in result:
        parsed_results.append(_parse_to_format(row, requested_format))
    return parsed_results


def _parse_to_format(row, requested_format):
    if requested_format in ("audio_id", "track_id"):
        return row.values()[0].split(":")[-1]
    else:
        return row.values()[0]


def _convert_format(requested_format):
    if requested_format == "file_id":
        return "transcoding.fileId"
    elif requested_format in ("audio_uri", "audio_id"):
        return "track_entity.audioRelation.audio.uri as audioUri"
    elif requested_format in ("track_uri", "track_id"):
        return "track_uri"
    elif requested_format == "track_gid":
        return "track_gid"
