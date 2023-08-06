import asyncio
from unittest import mock

import pytest

from klio.transforms import core
from klio.transforms import decorators
from klio_core.proto import klio_pb2

from spotify_klio.transforms import decorators as sp_decorators
from tests import conftest


# NOTE: When the config attribute is accessed (when setting up
# a metrics counter object), it will try to read a
# `/usr/src/config/.effective-klio-job.yaml` file.
patcher = mock.patch.object(
    core.RunConfig, "get", conftest._klio_config_w_benchmark
)
patcher.start()


@pytest.fixture
def kmsg():
    msg = klio_pb2.KlioMessage()
    msg.data.element = b"spotify:episode:45h7rggVBoRwJPKpRNFzsn"
    return msg


def test_benchmark(mocker, monkeypatch, kmsg):
    mock_function = mocker.Mock()
    mock_pubsub = mocker.Mock()
    mock_pubsub_client = mocker.Mock()
    future = asyncio.Future()
    mock_pubsub_client.publish.return_value = future
    mock_pubsub.PublisherClient.return_value = mock_pubsub_client
    monkeypatch.setattr(sp_decorators.kbenchmark, "pubsub_v1", mock_pubsub)

    @decorators._handle_klio
    @sp_decorators._benchmark
    def func(kmsg, *args, **kwargs):
        mock_function(*args, **kwargs)
        yield

    func(kmsg.SerializeToString())
    func(kmsg.SerializeToString())
    func(kmsg.SerializeToString())
    assert len(mock_function.mock_calls) == 3
    assert len(mock_pubsub_client.publish.mock_calls) == 3


def test_benchmark_raises_parents(kmsg, mocker, monkeypatch):
    with pytest.raises(RuntimeError):

        @sp_decorators.benchmark
        def func(kmsg, *args, **kwargs):
            raise RuntimeError

        func(conftest._klio_config, kmsg.data)


def test_benchmark_off(mocker, monkeypatch, kmsg):
    mock_function = mocker.Mock()
    mock_pubsub = mocker.Mock()
    mock_pubsub_client = mocker.Mock()
    mock_pubsub_client.publish.return_value = mocker.Mock()
    mock_pubsub.PublisherClient.return_value = mock_pubsub_client
    monkeypatch.setattr(sp_decorators.kbenchmark, "pubsub_v1", mock_pubsub)

    with mock.patch.object(core.RunConfig, "get", conftest._klio_config):
        with pytest.raises(RuntimeError):

            @decorators._handle_klio
            @sp_decorators._benchmark
            def func(kmsg, *args, **kwargs):
                mock_function(*args, **kwargs)
                yield

            func(kmsg.SerializeToString())
