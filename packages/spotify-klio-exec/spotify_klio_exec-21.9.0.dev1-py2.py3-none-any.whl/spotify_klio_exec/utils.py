from spotify_klio.transforms import io

from klio_exec.commands.run import BatchEventMapper


def override_io_types():
    """overrides some of klio's built-in transforms with spotify-specific
    versions"""
    BatchEventMapper.input["avro"] = io.KlioReadFromHadesAvro
