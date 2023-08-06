# Copyright 2020 Spotify AB

from klio_cli.commands.job import run


class SpotifyRunPipeline(run.RunPipeline):
    DOCKER_LOGGER_NAME = "spklio.job.run"

    def __init__(
        self,
        job_dir,
        klio_config,
        docker_runtime_config,
        run_job_config,
        sp_run_job_config,
    ):
        super().__init__(
            job_dir, klio_config, docker_runtime_config, run_job_config
        )
        self.sp_run_job_config = sp_run_job_config

    def _get_command(self):
        """Supports easy enabling of internal XPN."""
        command = super()._get_command()

        if self.sp_run_job_config.xpn is True:
            command.append("--xpn")
        # don't do anything if `None`
        elif self.sp_run_job_config.xpn is False:
            command.append("--no-xpn")

        return command
