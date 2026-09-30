import os

from datadog_checks.celerdata import CelerdataCheck
from datadog_checks.dev.utils import get_metadata_metrics

HERE = os.path.dirname(os.path.abspath(__file__))
FE_METRICS_FIXTURE = os.path.join(HERE, "fixtures", "fe_metrics.txt")

# Values straight from the fixture. StarRocks FE interleaves `table_num` with `db_size_bytes`,
# one pair per database, so only `information_schema` was collected until the metric type was
# pinned in METRIC_MAP.
EXPECTED_TABLE_NUM = {"information_schema": 54, "_statistics_": 10, "sys": 8, "analytics": 19}

SLOW_LOCK_METRICS = ("celerdata.fe.slow_lock_held_time_ms", "celerdata.fe.slow_lock_wait_time_ms")


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


def test_slow_lock_metrics_given_summary_families_returns_quantile_and_count_only(
    aggregator, dd_run_check, mock_http_response, fe_instance
):
    _run(aggregator, dd_run_check, mock_http_response, fe_instance)

    for metric in SLOW_LOCK_METRICS:
        aggregator.assert_metric(f"{metric}.quantile")
        aggregator.assert_metric(f"{metric}.count")
        # StarRocks derives `_sum` as count * 1-minute-windowed mean, so it is neither a sum
        # nor monotonic. It is deliberately not submitted.
        assert not aggregator.metrics(f"{metric}.sum")
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_query_timeout_given_zero_valued_counter_returns_the_count_metric(
    aggregator, dd_run_check, mock_http_response, fe_instance
):
    _run(aggregator, dd_run_check, mock_http_response, fe_instance)

    # Issue #2854 reported this metric as missing, which does not reproduce: it has been mapped
    # since the first release. This pins that it is collected.
    aggregator.assert_metric("celerdata.fe.query.timeout.count", value=0)
