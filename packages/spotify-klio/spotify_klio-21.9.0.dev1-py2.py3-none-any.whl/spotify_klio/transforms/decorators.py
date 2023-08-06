# Copyright 2021 Spotify AB

import functools

from klio.transforms import _utils as txf_utils
from klio.transforms import decorators as klio_decorators

from spotify_klio.transforms import _benchmark as kbenchmark


def _benchmark(*args, exception=None, exception_message=None, **kwargs):
    def inner(func_or_meth):
        with klio_decorators._klio_context() as ctx:
            kctx = ctx

        benchmark_wrapper = kbenchmark.KlioBenchmarkWrapper(
            function=func_or_meth,
            klio_context=kctx,
            exception=exception,
            exception_message=exception_message,
        )

        @functools.wraps(func_or_meth)
        def method_wrapper(self, incoming_item, *args, **kwargs):
            args = (self, incoming_item) + args
            return benchmark_wrapper(*args, **kwargs)

        @functools.wraps(func_or_meth)
        def func_wrapper(kctx, incoming_item, *args, **kwargs):
            args = (kctx, incoming_item) + args
            return benchmark_wrapper(*args, **kwargs)

        if klio_decorators.__is_method(func_or_meth):
            return method_wrapper
        return func_wrapper

    if args and callable(args[0]):
        return inner(args[0])

    return inner


@txf_utils.experimental()
def benchmark(*args, **kwargs):
    """Run the decorated method/function with a benchmark emitter
    in a separate thread.
    Publishes benchmark to topic
        projects/sigint/topics/user-benchmarking-job-data and
    Dataflow job https://console.cloud.google.com/dataflow/jobs/
        europe-west1/2021-08-23_11_55_08-11381037738354644031?project=sigint
        will write to bigquery table `sigint.user_benchmarks.job_data`

    Order Matters when used with other Klio decorators.
    When using the `@handle_klio`, then the
    `@benchmark` decorator should be applied to a method/function
    **after** `@handle_klio` .
    .. code-block:: python
        @handle_klio
        @benchmark
        def my_map_func(ctx, item):
            ctx.logger.info(f"Received {item.element}")

        class MyDoFn(beam.DoFn):
            @handle_klio
            @benchmark
            def process(self, item):
                self._klio.logger.info(
                    f"Received {item.element}"
                )
    When using benchmarking with retries and timeout decorators,
    placement of the `@benchmark` decorator will affect benchmark results.
    If `@benchmark` is placed **before** `@timeout` or `@retry`, benchmark
    results will include results for messages that have timed out or have
    been retried.
    .. code-block:: python
        class MyDoFn(beam.DoFn):
            @handle_klio
            @timeout
            @retry
            @benchmark
            def process(self, item):
                self._klio.logger.info(
                    f"Received {item.element}"
                )
    If `@benchmark` is placed **after** `@timeout` or `@retry`, benchmark
    results will only include results for messages that have completed the
    logic of the inner `@timeout` or `@retry` logic.
    .. code-block:: python
        class MyDoFn(beam.DoFn):
            @handle_klio
            @benchmark
            @timeout
            @retry
            def process(self, item):
                self._klio.logger.info(
                    f"Received {item.element}"
                )
    """
    return _benchmark(*args, **kwargs,)
