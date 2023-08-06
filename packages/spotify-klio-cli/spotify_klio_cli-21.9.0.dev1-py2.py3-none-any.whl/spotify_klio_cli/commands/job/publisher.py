# Copyright 2021 Spotify AB

import logging
import time

from google.cloud import bigquery
from google.cloud import pubsub_v1

from klio_core.proto.v1beta1 import klio_pb2


# TODO: If we decide to make this available outside
# of benchmarking, we can move this class to be
# accessible for `klio message publish` command
class KlioDatasetPublisher(object):
    def __init__(self, job_config):
        self._job_config = job_config
        batch_settings = pubsub_v1.types.BatchSettings(max_messages=500)
        self._publisher = pubsub_v1.PublisherClient(batch_settings)
        self._message_ids = []
        self._bq_client = bigquery.Client()

    @staticmethod
    def should_publish(klio_config, dataset, kwargs):
        """Determine if Klio messages should be published to job."""

        if not kwargs["publish"] and kwargs["publish_message_count"] is None:
            return False

        if klio_config.pipeline_options.streaming and dataset:
            return True
        elif klio_config.pipeline_options.streaming:
            logging.info(
                "Not dataset specified to publish "
                "while benchmarking in streaming mode."
            )
        elif dataset:
            logging.warning(
                "Klio messages can only published in streaming mode. "
                "When in batch mode the dataset should be configured in the "
                "`job_config.events.inputs` field in the `klio-job.yaml`."
            )
        return False

    def message_sent_callback(self, future):
        message_id = future.result()
        self._message_ids.append(message_id)
        logging.debug(f"Message sent with id: {message_id}")

    def _fetch_dataset_data(self, dataset, message_count=500000):

        try:
            QUERY = """
                FROM
                `{dataset}`
                LIMIT {message_count}
            """
            # Another option is to pull all messages from dataset
            # then return `message_count` number of messages.
            # This lets us use the same cached query
            select_column = "SELECT uri "

            query_job = self._bq_client.query(
                select_column
                + QUERY.format(dataset=dataset, message_count=message_count)
            )
            complete_results = list(query_job.result())

            result_count = len(complete_results)
            logging.info(
                f"Successfully fetched {result_count} results from {dataset}"
            )
            return complete_results
        except Exception as e:
            logging.error(f"Unable to fetch dataset. {e}")
            raise e

    def _create_klio_message(self, track):
        # TODO: This assumes top down publishing
        msg = klio_pb2.KlioMessage()
        msg.data.element = bytes(track, "utf-8")
        msg.version = klio_pb2.V2
        msg.metadata.intended_recipients.anyone.SetInParent()
        data = msg.SerializeToString()
        return data

    def _publish_messages(self, records):
        event_input = self._job_config.job_config.events.inputs[0].topic
        logging.info(f"Publishing to {event_input}")

        for track in records:
            track = track.uri.strip()
            if track in self._message_ids:
                logging.info(f"Already published {track}")
                continue
            self._message_ids.append(track)
            data = self._create_klio_message(track)
            future = self._publisher.publish(event_input, data=data)
            future.add_done_callback(self.message_sent_callback)

        logging.info(f"Published {len(self._message_ids)} uris.")

    def publish_messages(self, dataset, message_count=500000):
        logging.info(
            f"Publishing {message_count} " f"messages from {dataset}."
        )
        # Reset message_ids
        self._message_ids = []
        start = time.time()
        try:
            records = self._fetch_dataset_data(
                dataset, message_count=message_count
            )
            self._publish_messages(records)
            diff = time.time() - start
            logging.info(
                f"Publishing complete. Sent {len(self._message_ids)} "
                f"messages in {diff} seconds."
            )
        except Exception as e:
            raise e
        finally:
            logging.info("Waiting publisher to finish. Sleeping 10 seconds.")
            time.sleep(10)
            logging.info("Publishing complete.")
