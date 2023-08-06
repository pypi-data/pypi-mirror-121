# Copyright 2020 Spotify AB

from datetime import date, timedelta

BASE_QUERY = """
SELECT
  {}
FROM
  `spotify-entities.audio.{}` AS audio_entity,
  UNNEST(audio_entity.transcoding) AS transcoding
INNER JOIN
  `spotify-entities.track.{}` AS track_entity
ON
  track_entity.audioRelation.audio.uri = audio_entity.uri
INNER JOIN
  `knowledge-graph-112233.track_entity.track_entity_{}`
ON
  track_uri = track_entity.uri
WHERE
  audio_attributes.duration < {}
  AND audio_attributes.duration >= {}
  AND transcoding.format = "OGG_320"
LIMIT
  {}
"""


def track_query(query, min_length, max_length, limit):
    date_str = _get_date_str()
    return BASE_QUERY.format(
        query, date_str, date_str, date_str, max_length, min_length, limit
    )


def _get_date_str():
    yesterday = date.today() - timedelta(days=1)
    return yesterday.strftime("%Y%m%d")
