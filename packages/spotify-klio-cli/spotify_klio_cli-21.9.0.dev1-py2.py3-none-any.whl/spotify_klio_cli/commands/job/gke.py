# Copyright 2021 Spotify AB

from klio_cli.commands.job import gke


class SpotifyRunPipelineGKE(gke.RunPipelineGKE):
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
