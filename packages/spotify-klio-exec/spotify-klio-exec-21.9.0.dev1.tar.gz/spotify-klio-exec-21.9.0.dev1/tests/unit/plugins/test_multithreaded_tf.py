# Copyright 2020 Spotify AB

import pytest

from spotify_klio_exec.plugins.audit import multithreaded_tf


@pytest.mark.parametrize("tf_loaded", (True, False))
@pytest.mark.parametrize("worker_threads", (0, 1, 2))
def test_multithreaded_tf_usage(
    tf_loaded, worker_threads, klio_config, mock_emit_warning, mocker
):
    if worker_threads:
        klio_config.pipeline_options.experiments = [
            "worker_threads={}".format(worker_threads)
        ]

    if tf_loaded:
        mocker.patch.dict("sys.modules", {"tensorflow": ""})

    mt_tf_usage = multithreaded_tf.MultithreadedTFUsage(
        "job/dir", klio_config, "term_writer"
    )

    mt_tf_usage.after_tests()

    if worker_threads != 1 and tf_loaded:
        # don't care about the actual message
        assert 1 == mock_emit_warning.call_count
    else:
        mock_emit_warning.assert_not_called()
