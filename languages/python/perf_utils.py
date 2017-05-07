import contextlib, gc, statistics
from time import perf_counter  # used by timeit module, same as time.monotonic : https://github.com/python/cpython/blob/master/Modules/timemodule.c#L923


@contextlib.contextmanager
def trace_exec_time(disable_gc=False, **kwargs):
    """
    USAGE:
        with trace_exec_time(name='Heavy calculation') as timer:
            result = big_compute(list_of_things)
        print(timer['name'], "%0.3fms" % timer['exec_duration_in_ms'])  # -> Heavy calculation 10529.576ms
    """
    gc_was_enabled = gc.isenabled()
    if disable_gc:
        gc.disable()
    start = perf_counter()
    try:
        yield kwargs
    finally:
        end = perf_counter()
        kwargs['exec_duration_in_ms'] = (end - start) * 1000
        if disable_gc and gc_was_enabled:
            gc.enable()


def compute_timing_stats(timings_in_ms):
    if not timings_in_ms:
        return {'count': 0}
    timings_in_ms = sorted(timings_in_ms)
    total = sum(timings_in_ms)
    return {
        'count': len(timings_in_ms),
        'mean': total / len(timings_in_ms),
        'p00_min': timings_in_ms[0],
        'p01': percentile(timings_in_ms, .01),
        'p10': percentile(timings_in_ms, .1),
        'p50_median': percentile(timings_in_ms, .5),
        'p90': percentile(timings_in_ms, .9),
        'p99': percentile(timings_in_ms, .99),
        'p100_max': timings_in_ms[-1],
        'pstdev': statistics.pstdev(timings_in_ms),
        'sum': total
    }

def percentile(sorted_data, percent):
    """
    Find the percentile of a list of values.

    @parameter sorted_data - is an ALREADY SORTED list of values
    @parameter percent - a float value from 0.0 to 1.0.

    @return - the percentile of the values
    """
    assert 0 <= percent < 1
    index = (len(sorted_data)-1) * percent
    return sorted_data[int(index)]
