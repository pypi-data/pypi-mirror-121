# Copyright 2020 Spotify AB

import contextlib
import logging
import os
import sys

import click

from klio_core.config import _preprocessing as preprocessing


@contextlib.contextmanager
def smart_open(filename=None, fmode=None):
    """Handle both stdout and files in the same manner."""
    if filename and filename != "-":
        fh = open(filename, fmode)
    else:
        fh = sys.stdout

    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()


def import_sp_gke_commands():
    # Importing GKE commands needs to be behind a try/except because the
    # kubernetes dependency is not part of the base install dependencies
    try:
        from spotify_klio_cli.commands.job import gke as gke_commands

        # the import is only local to this function so we need to return the
        # module
        return gke_commands
    except ImportError as e:
        if "kubernetes" in e.msg:
            logging.error(
                "Failed to import DirectGKERunner dependencies."
                " Did you install `spotify-klio-cli[kubernetes]`?"
            )
            raise SystemExit(1)
        logging.error(e)
        raise SystemExit(1)


def has_internal_executor(job_dir):
    """Try to deduce if job is using spotify-klio-exec."""
    dockerfile_path = os.path.join(job_dir, "Dockerfile")
    with open(dockerfile_path, "r") as f:
        contents = f.read()
    if "spotify-klio-exec" not in contents:
        msg = (
            "You're using `spotify-klio-cli` but the job's Dockerfile does "
            "not install `spotify-klio-exec` that provides internal "
            "features. Do you want to continue?"
        )
        click.confirm(msg, abort=True)


def register_v1_config_lifting_plugin():
    preprocessing.KlioConfigPreprocessor.add_plugin_preprocessor(
        lift_v1_config
    )


def lift_v1_config(config_dict, log=True):

    detected_v1 = False

    if any(
        [
            config_dict.get("version", None) == 1,
            config_dict.get("job_config", {}).get("inputs"),
            config_dict.get("job_config", {}).get("outputs"),
        ]
    ):
        detected_v1 = True
        if log:
            logging.warn(
                "Detected v1 config, please upgrade your job's config file "
                "to klio v2.  You can also run 'klio job convert-v1-config' "
                "to rewrite your klio-job.yaml file."
            )

    if not detected_v1:
        return config_dict

    lifted = config_dict.copy()

    # bump the version
    lifted["version"] = 2

    # convert I/O
    lifted["job_config"]["events"] = {
        "inputs": [
            {
                "type": "pubsub",
                "topic": config_dict["job_config"]["inputs"][0]["topic"],
                "subscription": config_dict["job_config"]["inputs"][0][
                    "subscription"
                ],
            }
        ]
    }
    lifted["job_config"]["data"] = {
        "inputs": [
            {
                "type": "gcs",
                "location": config_dict["job_config"]["inputs"][0][
                    "data_location"
                ],
            }
        ]
    }

    if len(config_dict["job_config"].get("outputs", [])) > 0:
        lifted["job_config"]["events"]["outputs"] = [
            {
                "type": "pubsub",
                "topic": config_dict["job_config"]["outputs"][0]["topic"],
            }
        ]
        lifted["job_config"]["data"]["outputs"] = [
            {
                "type": "gcs",
                "location": config_dict["job_config"]["outputs"][0][
                    "data_location"
                ],
            }
        ]

    # drop deprecated keys
    lifted.pop("owner", None)
    lifted.pop("owner_email", None)

    lifted["job_config"].pop("inputs", None)
    lifted["job_config"].pop("outputs", None)
    lifted["job_config"].pop("timeout_threshold", None)
    lifted["job_config"].pop("number_of_retries", None)
    lifted["job_config"].pop("binary_non_klio_messages", None)
    lifted["job_config"].pop("dependencies", None)

    return lifted


# calling this here ensures the v1->v2 conversion plugin is registered before
# any config parsing begins via the @with_klio_config decorator
register_v1_config_lifting_plugin()
