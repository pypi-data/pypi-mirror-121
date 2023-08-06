import pytest

from klio.transforms import io as klio_io

from spotify_klio.transforms import io


@pytest.fixture
def mock_hades(mocker, monkeypatch):
    return mocker.patch.object(io.clients, "HadesClient")


def test_readfromhadesavro(mocker, mock_hades):

    mock_hades_client = mock_hades.return_value
    mock_hades_client.get_gcs_uri.return_value = "gs://gcs/location"

    mock_init = mocker.patch.object(klio_io.beam.io.ReadFromAvro, "__init__")
    mock_init.return_value = None

    mocker.patch.object(io.klio_io, "_KlioFastAvroSource")

    io.KlioReadFromHadesAvro(location="hades:///foo/bar")

    expected_file_pattern = "gs://gcs/location/part-*"

    mock_init.assert_called_once_with(
        file_pattern=expected_file_pattern,
        min_bundle_size=0,
        use_fastavro=True,
        validate=True,
    )
