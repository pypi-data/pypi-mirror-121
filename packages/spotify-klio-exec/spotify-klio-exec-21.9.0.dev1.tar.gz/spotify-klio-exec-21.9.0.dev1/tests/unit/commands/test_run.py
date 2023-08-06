# Copyright 2020 Spotify AB

from unittest import mock

import pytest

from apache_beam.options import pipeline_options

from klio.transforms import core

from tests.unit import conftest

# NOTE: When the config attribute is accessed (when setting up
# a metrics counter object), it will try to read a
# `/usr/src/config/.effective-klio-job.yaml` file. Since some helper transforms
# use some decorators that access config, we just patch on the module level
# instead of within each and every test function.
patcher = mock.patch.object(core.RunConfig, "get", conftest._klio_config)
patcher.start()

from spotify_klio_exec.commands import run  # NOQA: E402, I100, I202


@pytest.fixture
def config(mocker):
    mock_config = mocker.Mock()
    mock_config.job_name = "my-job"
    mock_pipeline_options = mocker.Mock(
        region="europe-west1", experiments=list()
    )
    mock_config.pipeline_options = mock_pipeline_options
    return mock_config


@pytest.mark.parametrize(
    "xpn,subnetwork_conf,exp_subnetwork",
    (
        (
            True,
            None,
            run.SUBNET_BASE_URL.format(
                region="europe-west1", subnetwork_name="xpn-euw1"
            ),
        ),
        (False, None, None),
        (None, None, None),
        (True, "a-preconfig-subnetwork", "a-preconfig-subnetwork"),
        (False, "a-preconfig-subnetwork", "a-preconfig-subnetwork"),
        (None, "a-preconfig-subnetwork", "a-preconfig-subnetwork"),
    ),
)
def test_set_worker_options(
    xpn, subnetwork_conf, exp_subnetwork, config, mocker, monkeypatch
):
    config.pipeline_options.subnetwork = subnetwork_conf
    pipeline_opts_dict = {
        "region": "europe-west1",
        "experiments": list(),
    }
    if subnetwork_conf:
        pipeline_opts_dict["subnetwork"] = subnetwork_conf

    options = pipeline_options.PipelineOptions().from_dictionary(
        pipeline_opts_dict
    )

    mocker.patch("spotify_klio_exec.commands.run.base_run.KlioPipeline")

    kpipe = run.SpotifyKlioPipeline("test-job", config, mocker.Mock(xpn=xpn))
    kpipe._set_worker_options(options)

    actual_worker_options = options.view_as(pipeline_options.WorkerOptions)

    assert exp_subnetwork == actual_worker_options.subnetwork


def test_check_klio_version(mocker, monkeypatch):
    mock_run_module = mocker.Mock()
    monkeypatch.setattr(run.imp, "load_source", mock_run_module)

    mock_conf = mocker.Mock()
    mock_runtime_conf = mocker.Mock()
    kpipe = run.SpotifyKlioPipeline("test-job", mock_conf, mock_runtime_conf)

    kpipe._check_klio_version()

    mock_run_module.assert_called_once_with("run", "./run.py")


def test_check_klio_version_raises(mocker, monkeypatch):
    mock_run_module = mocker.Mock()
    mock_run_module.side_effect = AttributeError(
        "module 'klio.transforms' has no attribute 'KlioBaseDoFn'"
    )
    monkeypatch.setattr(run.imp, "load_source", mock_run_module)

    mock_conf = mocker.Mock()
    mock_runtime_conf = mocker.Mock()
    kpipe = run.SpotifyKlioPipeline("test-job", mock_conf, mock_runtime_conf)

    with pytest.raises(SystemExit):
        kpipe._check_klio_version()

    mock_run_module.assert_called_once_with("run", "./run.py")
