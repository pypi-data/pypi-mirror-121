# Copyright 2020 Spotify AB

import imp
import logging

from apache_beam.options import pipeline_options

from klio_exec.commands import run as base_run


SUBNET_BASE_URL = (
    "https://www.googleapis.com/compute/v1/projects/xpn-master/regions/"
    "{region}/subnetworks/{subnetwork_name}"
)
SUBNET_REGION_TO_NAME = {
    "europe-west1": "xpn-euw1",
    "us-central1": "xpn-usc1",
    "asia-east1": "xpn-ase1",
}


class SpotifyKlioPipeline(base_run.KlioPipeline):
    """run command with Spotify-specific features"""

    def _set_worker_options(self, options):
        """Supports easy enabling of internal XPN."""
        super()._set_worker_options(options)

        worker_opts = options.view_as(pipeline_options.WorkerOptions)
        if self.runtime_conf.xpn is True:
            if worker_opts.subnetwork is None:
                region = self.config.pipeline_options.region
                subnet_name = SUBNET_REGION_TO_NAME[region]
                worker_opts.subnetwork = SUBNET_BASE_URL.format(
                    region=region, subnetwork_name=subnet_name
                )

    # TODO: remove me when done migrating from v1 -> v2
    def _check_klio_version(self):
        try:
            imp.load_source("run", "./run.py")
        except AttributeError as e:
            if "no attribute 'KlioBaseDoFn'" in str(e):
                logging.error(
                    "Trying to deploy a v1 Klio job with incompatible v2 Klio "
                    "libraries installed in the job's runtime environment."
                    "\nTo deploy the job before migrating to Klio v2, pin the "
                    "following in the job's `job-requirements.txt` then "
                    "rebuild the job's image:"
                    "\n\tklio==0.1.0"
                    "\n\tklio-core==0.1.0"
                    "\n\tklio-exec==0.1.0"
                    "\n\tspotify-klio-exec==0.1.0"
                    "\nSee https://backstage.spotify.net/docs/klio/ "
                    "v2-migration for more information on how to migrate to "
                    "Klio v2."
                )
                raise SystemExit(1)

    def run(self):
        # TODO: remove me when done migrating from v1 -> v2
        self._check_klio_version()
        return super().run()
