# Copyright 2020 Spotify AB

import logging

from klio_cli.commands.job.verify import VerifyJob


class SpotifyVerifyJob(VerifyJob):
    def _add_tingle_access(self, bucket_name):
        # From: https://backstage.spotify.net/docs/tingle/secrets
        tingle = "build-agent-mounter@xpn-tingle-1.iam.gserviceaccount.com"
        tingle_sa = "serviceAccount:{}".format(tingle)
        try:
            bucket_obj = self.storage_client.get_bucket(bucket_name)
            iam_policy = bucket_obj.get_iam_policy()
            iam_policy.update({"roles/storage.objectViewer": {tingle_sa}})
            bucket_obj.set_iam_policy(iam_policy)
            msg = "Granted read access to Tingle for bucket: gs://{}/".format(
                bucket_name
            )
            logging.info(msg)
        except Exception as e:
            logging.error(
                "Could not give Tingle permission "
                "to read bucket: gs://{}/".format(bucket_name)
            )
            logging.error(e)
            raise SystemExit(1)

    def _confirm_tingle_access(self, tingle_sa, bucket_obj):
        iam_policy = bucket_obj.get_iam_policy()
        tingle_policy = iam_policy.get("roles/storage.objectViewer")
        if tingle_sa in tingle_policy:
            logging.info("Tingle has access to your Klio job.")
            return True
        elif self.create_resources:
            try:
                self._add_tingle_access(bucket_obj.name)
                logging.info("Tingle now has access to your Klio job.")
                return True
            except SystemExit:
                return False
        return False

    def _verify_tingle_access(self):
        logging.info("Verifying Tingle access.")
        tingle_bucket_path = "gs://{}-{}".format(
            "tingle-deploy", self.klio_config.job_name
        )
        tingle = "build-agent-mounter@xpn-tingle-1.iam.gserviceaccount.com"
        tingle_sa = "serviceAccount:{}".format(tingle)

        verified = self._verify_gcs_bucket(tingle_bucket_path)

        if verified:
            tingle_bucket = tingle_bucket_path.replace("gs://", "")
            bucket_obj = self.storage_client.get_bucket(tingle_bucket)
            return self._confirm_tingle_access(tingle_sa, bucket_obj)
        return False

    def _verify_all(self):
        return all([super()._verify_all(), self._verify_tingle_access()])
