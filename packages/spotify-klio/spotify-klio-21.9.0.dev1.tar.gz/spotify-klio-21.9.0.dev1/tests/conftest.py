# Copyright 2021 Spotify AB


import logging

import pytest

from klio_core import config


@pytest.fixture
def caplog(caplog):
    """Set global test logging levels."""
    caplog.set_level(logging.DEBUG)
    return caplog


def _job_config_dict():
    return {
        "metrics": {"logger": {}, "timer_unit": "ns"},
        "allow_non_klio_messages": False,
        "number_of_retries": 3,
        "events": {
            "inputs": [
                {
                    "type": "pubsub",
                    "topic": "test-parent-job-out",
                    "subscription": "test-parent-job-out-sub",
                    "data_location": "gs://sigint-output/test-parent-job-out",
                }
            ],
            "outputs": [
                {
                    "type": "pubsub",
                    "topic": "test-job-out",
                    "data_location": "gs://sigint-output/test-job-out",
                }
            ],
        },
        "data": {
            "inputs": [
                {
                    "type": "gcs",
                    "location": "gs://sigint-output/test-parent-job-out",
                }
            ],
            "outputs": [
                {"type": "gcs", "location": "gs://sigint-output/test-job-out",}
            ],
        },
        "more": "config",
        "that": {"the": "user"},
        "might": ["include"],
    }


def _benchmark_config_dict():
    return {
        "dataset": "sigint.benchmarking_uris.episodes_random_20210822",
        "enabled": True,
        "run_id": "8c438095-587c-4abc-9f49-6a35ed5d8dc4",
        "job_id": None,
        "skip_deploy": False,
        "metadata_topic": None,
        "data_topic": None,
    }


@pytest.fixture
def job_config_dict():
    return _job_config_dict()


def _pipeline_config_dict():
    return {
        "project": "test-project",
        "staging_location": "gs://some/stage",
        "temp_location": "gs://some/temp",
        "worker_harness_container_image": "gcr.io/sigint/foo",
        "streaming": True,
        "experiments": ["beam_fn_api"],
        "region": "us-central1",
        "num_workers": 3,
        "max_num_workers": 5,
        "disk_size_gb": 50,
        "worker_machine_type": "n1-standard-4",
        "runner": "direct",
        "autoscaling_algorithm": "THROUGHPUT_BASED",
        "update": False,
    }


@pytest.fixture
def pipeline_config_dict():
    return _pipeline_config_dict()


def _config_dict():
    return {
        "job_config": _job_config_dict(),
        "pipeline_options": _pipeline_config_dict(),
        "job_name": "test-job",
        "version": 2,
    }


@pytest.fixture
def config_dict():
    return _config_dict()


def _klio_config():
    return config.KlioConfig(_config_dict())


def _klio_config_w_benchmark():
    kconfig = _config_dict()
    kconfig["job_config"]["benchmark"] = _benchmark_config_dict()
    return config.KlioConfig(kconfig)
