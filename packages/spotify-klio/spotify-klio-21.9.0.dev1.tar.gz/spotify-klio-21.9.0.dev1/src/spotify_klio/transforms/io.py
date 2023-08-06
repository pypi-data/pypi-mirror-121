# Copyright 2020 Spotify AB

import logging
import os

from klio.transforms import io as klio_io

from spotify_klio.transforms import clients


# define an I/O transform using the klio-specific avro source
# note: fast avro is default for py3 on beam
class _KlioReadFromHadesAvro(klio_io._KlioReadFromAvro):
    # TODO: This probably shouldn't override the whole method, instead create a
    # sub-method for this to extend
    # TODO: `show_unpublished` isn't yet supported - it should be added to
    # spotify-klio-core (once we setup a spotify-specific klio config)
    def _get_file_pattern(self, file_pattern, location, show_unpublished=True):
        # TODO: this should be a validator in klio_core.config
        if not any([file_pattern, location]):
            raise klio_io.KlioMissingConfiguration(
                "Must configure at least one of the following keys when "
                "reading from avro: `file_pattern`, `location`."
            )

        # TODO: this should be a validator in klio_core.config
        # TODO: also check for valid and invalid URI schemes
        if location and location.startswith("hades:///"):
            hades_client = clients.HadesClient(location)

            location = hades_client.get_gcs_uri(show_unpublished)
            if file_pattern is None:
                file_pattern = "part-*"  # default avro+hades
            # We don't normally log where we're reading from. But I figured
            # it could be helpful here, particularly when the exact URL
            # may not be known (how often is someone going to provide a
            # revision?). It's only logged once per instantiation.
            logging.getLogger("klio").info(
                "Reading avro files from the following GCS bucket: "
                "%s" % location
            )

        if all([file_pattern, location]):
            file_pattern = os.path.join(location, file_pattern)

        elif file_pattern is None:
            file_pattern = location

        return file_pattern


class KlioReadFromHadesAvro(klio_io.KlioReadFromAvro):
    """ReadFromAvro transform that also supports Hades Endpoints"""

    def __init__(self, *args, **kwargs):
        self._reader = _KlioReadFromHadesAvro(*args, **kwargs)
        self.__counter = klio_io._KlioIOCounter(
            "read", "KlioReadFromHadesAvro"
        )
