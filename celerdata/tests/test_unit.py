import os

import pytest

from datadog_checks.celerdata import CelerdataCheck
from datadog_checks.dev.utils import get_metadata_metrics

from . import common

HERE = os.path.dirname(os.path.abspath(__file__))
FE_METRICS_FIXTURE = os.path.join(HERE, "fixtures", "fe_metrics.txt")

# Values straight from the fixture. StarRocks FE interleaves `table_num` with `db_size_bytes`,
# one pair per database, so only `information_schema` was collected until the metric type was
# pinned in METRIC_MAP.
EXPECTED_TABLE_NUM = {"information_schema": 54, "_statistics_": 10, "sys": 8, "analytics": 19}


def _run(aggregator, dd_run_check, mock_http_response, fe_instance):
    # Mocked at the HTTP boundary only: the FE scrape is the check's sole input.
    mock_http_response(file_path=FE_METRICS_FIXTURE)
    dd_run_check(CelerdataCheck("celerdata", {}, [fe_instance]))


def test_table_num_given_interleaved_families_returns_series_for_every_db(
    aggregator, dd_run_check, mock_http_response, fe_instance
):
    _run(aggregator, dd_run_check, mock_http_response, fe_instance)

    collected = {
        tag.split(":", 1)[1]: metric.value
        for metric in aggregator.metrics("celerdata.fe.table_num")
        for tag in metric.tags
        if tag.startswith("db_name:")
    }
    assert collected == EXPECTED_TABLE_NUM


@pytest.mark.parametrize(
    "metric, p99",
    [
        pytest.param("celerdata.fe.slow_lock_held_time_ms", 1725.0, id="held"),
        pytest.param("celerdata.fe.slow_lock_wait_time_ms", 655.0, id="wait"),
    ],
)
def test_slow_lock_metrics_given_summary_families_returns_quantile_and_count_only(
    aggregator, dd_run_check, mock_http_response, fe_instance, metric, p99
):
    _run(aggregator, dd_run_check, mock_http_response, fe_instance)

    endpoint_tag = f"endpoint:{common.FE_METRICS_URL}"
    # One point per upstream quantile; a sixth would mean `_sum` leaked into the gauge.
    aggregator.assert_metric(f"{metric}.quantile", count=5)
    aggregator.assert_metric(f"{metric}.quantile", value=p99, tags=["quantile:0.99", endpoint_tag], count=1)
    # `_count` is 137 in both fixture families and `_sum` is far larger, so the value proves which
    # sample feeds `.count`. The first scrape must not flush the FE's lifetime count as one delta.
    aggregator.assert_metric(
        f"{metric}.count", value=137, metric_type=aggregator.MONOTONIC_COUNT, flush_first_value=False, count=1
    )
    # StarRocks derives `_sum` as count * 1-minute-windowed mean, so it is neither a sum nor
    # monotonic. It is deliberately not submitted.
    aggregator.assert_metric(f"{metric}.sum", count=0)


def test_submitted_metrics_given_fe_payload_returns_metrics_declared_in_metadata(
    aggregator, dd_run_check, mock_http_response, fe_instance
):
    _run(aggregator, dd_run_check, mock_http_response, fe_instance)

    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_query_timeout_given_zero_valued_counter_returns_the_count_metric(
    aggregator, dd_run_check, mock_http_response, fe_instance
):
    _run(aggregator, dd_run_check, mock_http_response, fe_instance)

    # Issue #2854 reported this metric as missing, which does not reproduce: it has been mapped
    # since the first release. This pins that it is collected.
    aggregator.assert_metric("celerdata.fe.query.timeout.count", value=0)
