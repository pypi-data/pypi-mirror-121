# Copyright 2020 Spotify AB

import requests


class HadesRevisionNotFound(Exception):
    pass


class HadesClient(object):
    """Basic client for making Hades Requests"""

    HADES_HOST = "https://hades.spotify.net/api/v3/revisions"
    URL_TPL = HADES_HOST + "/{endpoint}/{partition}"

    def __init__(self, location):
        self.hades_uri = location

    def _parse_hades_uri(self):
        _, uri = self.hades_uri.split("hades:///")
        endpoint, partition, *revision = uri.split("/")
        if len(revision):
            # *revision is a list, but if a revision is given, then it's
            # only one string
            revision = revision[0]
        return endpoint, partition, revision

    def get_gcs_uri(self, show_unpublished=False):
        endpoint, partition, revision = self._parse_hades_uri()

        url = self.URL_TPL.format(endpoint=endpoint, partition=partition)
        if revision:
            url = "{url}/{revision}".format(url=url, revision=revision)

        if show_unpublished:
            url = "{url}?showUnpublished".format(url=url)

        resp = requests.get(url)
        resp.raise_for_status()

        data = resp.json()["data"]
        if revision:
            # `uri` should be in `data`, otherwise we get a 404 which
            # will be caught in `resp.raise_for_status()`
            return data["uri"]

        revisions = data.get("revisions")
        if not revisions:
            raise HadesRevisionNotFound(
                "No revisions found for partition '{}' of endpoint "
                "'{}'.".format(partition, endpoint)
            )
        latest_rev = max(revisions, key=lambda r: r["creationTime"])
        return latest_rev["uri"]
