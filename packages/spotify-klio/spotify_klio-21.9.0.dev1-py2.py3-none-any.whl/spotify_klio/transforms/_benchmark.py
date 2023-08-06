# Copyright 2021 Spotify AB

import collections
import datetime
import json
import logging
import time
import types

from google.cloud import pubsub_v1


BQ_DATE_FORMAT = "%Y-%m-%d %H:%M:%S.000000 UTC"

Result = collections.namedtuple(
    "Result",
    [
        "uri",
        "transform",
        "timestamp_started",
        "benchmark_run_id",
        "successful",
        "processed_time",
    ],
)


class KlioBenchmarkWrapper(object):
    """Wrap a function with benchmarking."""

    DEFAULT_EXC_MSG = (
        "Failed to benchmark function: {function}."
        "Last exception: {last_exception}"
    )

    DEFAULT_DATA_TOPIC = "projects/sigint/topics/user-benchmarking-job-data"

    def __init__(
        self, function, klio_context, exception=None, exception_message=None,
    ):
        self._function = function
        self._func_name = getattr(function, "__qualname__", function.__name__)
        self._klio_context = klio_context
        self._exception = exception or Exception
        self._exception_message = exception_message
        self._logger = logging.getLogger("klio")
        self._job_name = klio_context.config.job_name

        if not getattr(klio_context.config.job_config, "benchmark", False):
            raise RuntimeError(
                "Benchmarking decorator in use with missing configurations. "
                "Please provide `klio-job.yaml::job_config.benchmark` "
                "as a dictionary with the field `dataset` configured to the "
                "dataset you would like to benchmark against and the field "
                "`enabled` set to `True`. "
                "Else remove the `@benchmark` decorator."
            )
        elif not klio_context.config.job_config.benchmark["enabled"]:
            raise RuntimeError(
                "Benchmarking decorator in use but benchmarking is "
                "not enabled. Either (1) update the field "
                "`klio-job.yaml::job_config.benchmark.enabled` to True, "
                "(2) rerun you job with the flag `--benchmark` "
                "to enable benchmarking, or "
                f"(3) remove `@benchmark` decorator from {self._func_name} "
                "if you do not intend to benchmark this job."
            )
        self._benchmark_data_topic = (
            klio_context.config.job_config.benchmark["data_topic"]
            or self.DEFAULT_DATA_TOPIC
        )
        self._benchmark_run_id = klio_context.config.job_config.benchmark[
            "run_id"
        ]
        self._publisher_client = pubsub_v1.PublisherClient()

    def __call__(self, *args, **kwargs):

        incoming_item = args[1]
        successful, duration = False, 0
        entity_uri = incoming_item.element.decode("utf-8")
        try:
            timestamp_started = datetime.datetime.utcnow().strftime(
                BQ_DATE_FORMAT
            )
            start_time = time.monotonic()
            ret = self._function(*args, **kwargs)

            if isinstance(ret, types.GeneratorType):
                ret = next(ret)
            successful = True
            return ret

        except self._exception as e:
            self._raise_exception(e)

        finally:
            duration = time.monotonic() - start_time
            result = Result(
                uri=entity_uri,
                transform=self._func_name,
                timestamp_started=timestamp_started,
                benchmark_run_id=self._benchmark_run_id,
                successful=successful,
                processed_time=duration,
            )
            self.emit_benchmark(result)

    def _raise_exception(self, last_exception):
        # TODO: This is where we can capture error_message
        # for benchmark.
        if self._exception_message is None:
            self._exception_message = self.DEFAULT_EXC_MSG.format(
                function=self._func_name, last_exception=last_exception
            )
        self._logger.warning(self._exception_message)
        raise last_exception

    def _submit_callback(self, fut):
        try:
            fut.result()
        except Exception as e:
            msg = "Error emitting benchmark '{}': {}".format(fut.uri, e)
            self.logger.warning(msg)

    def emit_benchmark(self, result):
        result_json = {
            "uri": result.uri,
            "transform": result.transform,
            "benchmark_run_id": result.benchmark_run_id,
            "timestamp_started": result.timestamp_started,
            "successful": result.successful,
            "processed_time": result.processed_time,
        }
        self._logger.info(
            f"Emitting benchmark {result_json}"
            f"to topic {self._benchmark_data_topic}"
        )
        try:
            bytes_data = json.dumps(result_json).encode("utf-8")
            future = self._publisher_client.publish(
                self._benchmark_data_topic, bytes_data
            )
            future.uri = result.uri
            future.add_done_callback(self._submit_callback)
            return future
        except Exception as e:
            self._logger.error(
                f"Failed to write benchmark for {result.uri}: {e}"
            )
        else:
            self._logger.info(
                f"Successfully wrote benchmark for {result.uri}."
            )
