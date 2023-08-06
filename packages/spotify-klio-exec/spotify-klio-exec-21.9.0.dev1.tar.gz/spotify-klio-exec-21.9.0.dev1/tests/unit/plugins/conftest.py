# Copyright 2020 Spotify AB

import pytest

from klio_exec.commands.audit_steps import base


@pytest.fixture
def klio_config(mocker):
    conf = mocker.Mock()
    conf.pipeline_options = mocker.Mock()
    conf.pipeline_options.experiments = []
    return conf


@pytest.fixture
def mock_emit_warning(mocker, monkeypatch):
    mock = mocker.Mock()
    monkeypatch.setattr(base.BaseKlioAuditStep, "emit_warning", mock)
    return mock


@pytest.fixture
def mock_emit_error(mocker, monkeypatch):
    mock = mocker.Mock()
    monkeypatch.setattr(base.BaseKlioAuditStep, "emit_error", mock)
    return mock
