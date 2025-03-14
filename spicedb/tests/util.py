import os
from itertools import chain

from datadog_checks.dev import get_docker_hostname, get_here
from datadog_checks.spicedb.metrics import COUNTER_METRICS, GAUGE_METRICS, HISTOGRAM_METRICS

HOST = get_docker_hostname()
PORT = "9090"


def get_expected_non_histogram_metrics():
    return list(
        chain(
            # We add a .count suffix because datadog is going to append it before it's sent.
            (f"{datadog_name}.count" for datadog_name in COUNTER_METRICS.values()),
            # We pass through the other metrics straight.
            GAUGE_METRICS.values(),
        )
    )


def get_expected_histogram_metrics():
    return HISTOGRAM_METRICS.values()


def get_fixture_path(filename):
    return os.path.join(get_here(), "fixtures", filename)
