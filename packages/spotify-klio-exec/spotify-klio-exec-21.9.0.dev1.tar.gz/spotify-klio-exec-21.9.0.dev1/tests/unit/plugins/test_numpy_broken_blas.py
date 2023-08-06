# Copyright 2020 Spotify AB

import pytest

from spotify_klio_exec.plugins.audit import numpy_broken_blas


@pytest.mark.parametrize(
    "worker_threads,platform,has_numpy,version,exp_emit_calls",
    (
        (1, None, False, None, 0),
        (2, "Darwin", False, None, 0),
        (0, "Linux", False, None, 0),
        (2, "Linux", False, None, 0),
        (2, "Linux", True, "1.17.0", 0),
        (2, "Linux", True, "1.16.3", 0),
        (2, "Linux", True, "1.16.2", 1),
    ),
)
def test_numpy_broken_blas_usage(
    worker_threads,
    platform,
    has_numpy,
    version,
    exp_emit_calls,
    klio_config,
    mock_emit_error,
    mocker,
    monkeypatch,
):
    if worker_threads:
        klio_config.pipeline_options.experiments = [
            "worker_threads={}".format(worker_threads)
        ]

    monkeypatch.setattr(numpy_broken_blas.platform, "system", lambda: platform)
    if has_numpy is False:
        mocker.patch.dict("sys.modules", {"numpy": None})
    else:
        monkeypatch.setattr("numpy.version.short_version", version)

    numpy_broken_blas_usage = numpy_broken_blas.NumPyBrokenBLASUsage(
        "job/dir", klio_config, "term_writer"
    )

    numpy_broken_blas_usage.after_tests()

    # don't care about the actual message
    assert exp_emit_calls == mock_emit_error.call_count
