# Copyright 2020 Spotify AB

import os

import pytest
import yaml

from click import testing

from klio_core import _testing as core_testing
from klio_core import config as kconfig

from spotify_klio_exec import cli


@pytest.fixture
def cli_runner():
    return testing.CliRunner()


@pytest.fixture
def config():
    return {
        "job_name": "klio-job-name",
        "job_config": {
            "input_topics": ["test-in-topic"],
            "output_topics": ["test-out-topic"],
            "input_data_locations": ["gs://test-in-data"],
            "output_locations": ["gs://test-out-data"],
        },
        "pipeline_options": {
            "streaming": True,
            "update": False,
            "worker_harness_container_image": "a-worker-image",
            "experiments": ["beam_fn_api"],
            "project": "test-gcp-project",
            "zone": "europe-west1-c",
            "region": "europe-west1",
            "staging_location": "gs://test-gcp-project-dataflow-tmp/staging",
            "temp_location": "gs://test-gcp-project-dataflow-tmp/temp",
            "max_num_workers": 2,
            "disk_size_gb": 32,
            "worker_machine_type": "n1-standard-2",
            "subnetwork": "some/path",
            "runner": "DataflowRunner",
        },
    }


@pytest.fixture
def patch_os_getcwd(monkeypatch, tmpdir):
    test_dir = str(tmpdir.mkdir("testing"))
    monkeypatch.setattr(os, "getcwd", lambda: test_dir)
    return test_dir


@pytest.fixture
def mock_klio_config(mocker, monkeypatch, patch_os_getcwd, config):
    mock = core_testing.MockKlioConfig(
        cli, mocker, monkeypatch, patch_os_getcwd
    )
    mock.setup(config, "klio-job.yaml")
    return mock


@pytest.fixture
def klio_config(config, monkeypatch):
    conf = kconfig.KlioConfig(config)
    monkeypatch.setattr(cli.config, "KlioConfig", lambda x: conf)
    return conf


@pytest.fixture
def patch_get_config(monkeypatch, config):
    monkeypatch.setattr(cli.base_cli, "_get_config", lambda x: config)


@pytest.fixture
def mock_klio_pipeline(mocker, monkeypatch):
    mock = mocker.Mock()
    mocker.patch("spotify_klio_exec.commands.run.SpotifyKlioPipeline", mock)
    return mock


@pytest.mark.parametrize("blocking", (True, False, None))
@pytest.mark.parametrize(
    "image_tag,direct_runner,update,xpn",
    (
        (None, True, False, None),
        (None, False, True, True),
        (None, False, None, False),
        ("a-tag", True, False, None),
        ("a-tag", False, False, True),
        ("a-tag", True, True, False),  # irrelevant, but CYA
        ("a-tag", False, True, False),
    ),
)
def test_run_pipeline(
    image_tag,
    direct_runner,
    update,
    blocking,
    xpn,
    cli_runner,
    mock_klio_config,
    mock_klio_pipeline,
    mocker,
):
    runtime_conf = cli.SpotifyRuntimeConfig(
        image_tag=None,
        direct_runner=False,
        update=None,
        xpn=None,
        blocking=None,
    )

    cli_inputs = []

    if image_tag:
        cli_inputs.extend(["--image-tag", image_tag])
        runtime_conf = runtime_conf._replace(image_tag=image_tag)
    if direct_runner:
        cli_inputs.append("--direct-runner")
        runtime_conf = runtime_conf._replace(direct_runner=True)
    if update:
        cli_inputs.append("--update")
        runtime_conf = runtime_conf._replace(update=True)
    if update is False:
        cli_inputs.append("--no-update")
    if not update:  # if none or false
        runtime_conf = runtime_conf._replace(update=False)
    if xpn:
        cli_inputs.append("--xpn")
        runtime_conf = runtime_conf._replace(xpn=True)
    if xpn is False:
        cli_inputs.append("--no-xpn")
        runtime_conf = runtime_conf._replace(xpn=False)
    if xpn is None:
        runtime_conf = runtime_conf._replace(xpn=True)
    if blocking:
        cli_inputs.append("--blocking")
        runtime_conf = runtime_conf._replace(blocking=True)
    if blocking is False:
        cli_inputs.append("--no-blocking")
    if not blocking:  # if none or false
        runtime_conf = runtime_conf._replace(blocking=False)

    result = cli_runner.invoke(cli.run_sp_pipeline, cli_inputs)
    core_testing.assert_execution_success(result)
    mock_klio_config.assert_calls()

    assert 1 == mock_klio_pipeline.call_count
    # assert_called_once_with does an equality *and* identity test; we just
    # want to do an equality test so we're just comparing call args
    actual_call_args = mock_klio_pipeline.call_args
    exp_call_args = mocker.call(
        "klio-job-name", mock_klio_config.klio_config, runtime_conf
    )
    assert exp_call_args == actual_call_args
    mock_klio_pipeline.return_value.run.assert_called_once_with()


@pytest.mark.parametrize(
    "config_file_override", (None, "klio-job2.yaml"),
)
def test_run_pipeline_conf_override(
    config_file_override,
    cli_runner,
    config,
    mock_klio_config,
    mock_klio_pipeline,
    caplog,
    tmpdir,
    monkeypatch,
):

    cli_inputs = []

    temp_dir = tmpdir.mkdir("testing123uniquename")
    temp_dir_str = str(temp_dir)
    monkeypatch.setattr(os, "getcwd", lambda: temp_dir_str)

    exp_conf_file = "klio-job.yaml"
    if config_file_override:
        exp_conf_file = os.path.join(temp_dir_str, config_file_override)
        cli_inputs.extend(["--config-file", exp_conf_file])

        # create a tmp file else click will complain it doesn't exist
        with open(exp_conf_file, "w") as f:
            yaml.dump(config, f)
        mock_klio_config.setup(config, "klio-job.yaml", exp_conf_file)
    else:
        mock_klio_config.setup(config, "klio-job.yaml")

    result = cli_runner.invoke(cli.run_sp_pipeline, cli_inputs)
    core_testing.assert_execution_success(result)
