#!/usr/bin/env python
# Copyright 2020 Spotify AB

import collections

import click

# WARNING: be careful with what is imported here.  Any decorators that read
# config cannot be imported here (even transitively) since they will attempt to
# read the config object before it exists.
from klio.transforms import core as klio_transforms_core
from klio_core import options as core_options
from klio_core import utils as core_utils
from klio_exec import options
from klio_exec.cli import main

SpotifyRuntimeConfig = collections.namedtuple(
    "SpotifyRuntimeConfig",
    ["image_tag", "direct_runner", "update", "xpn", "blocking"],
)


@main.command("run")
@core_options.image_tag
@core_options.direct_runner
@core_options.update
@options.blocking
@click.option(
    "--xpn/--no-xpn",
    default=True,
    is_flag=True,
    help=(
        "Enable/disable XPN for runtime. Default: True. XPN is not needed "
        "for Dockerized pipelines that do not interact with internal Spotify "
        "services."
    ),
)
@core_utils.with_klio_config
def run_sp_pipeline(
    image_tag, direct_runner, update, klio_config, config_meta, xpn, blocking
):
    """Overrides `klioexec run` to support easy enabling of XPN."""

    # RunConfig ensures config is pickled and sent to worker.  Note this
    # depends on save_main_session being True
    klio_transforms_core.RunConfig.set(klio_config)

    # These can only be imported after RunConfig is set since they will import
    # classes that attempt to access config when imported!
    from spotify_klio_exec import utils
    from spotify_klio_exec.commands import run

    utils.override_io_types()

    if update is None:  # if it's not explicitly set in CLI, look at config
        update = klio_config.pipeline_options.update
    if blocking is None:  # if it's not explicitly set in CLI, look at config
        blocking = klio_config.job_config.blocking

    runtime_conf = SpotifyRuntimeConfig(
        image_tag, direct_runner, update, xpn, blocking
    )

    klio_pipeline = run.SpotifyKlioPipeline(
        klio_config.job_name, klio_config, runtime_conf
    )
    klio_pipeline.run()


if __name__ == "__main__":
    main()
