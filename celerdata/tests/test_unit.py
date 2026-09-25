import os

from datadog_checks.celerdata import CelerdataCheck
from datadog_checks.dev.utils import get_metadata_metrics

HERE = os.path.dirname(os.path.abspath(__file__))
FE_METRICS_FIXTURE = os.path.join(HERE, "fixtures", "fe_metrics.txt")

# Every database present in the fixture. StarRocks FE interleaves `table_num` with
# `db_size_bytes`, one pair per database, so only the first was collected until the
# metric type was pinned in METRIC_MAP.
EXPECTED_DATABASES = ("information_schema", "_statistics_", "sys", "analytics")

SLOW_LOCK_METRICS = ("celerdata.fe.slow_lock_held_time_ms", "celerdata.fe.slow_lock_wait_time_ms")


def test_table_num_given_interleaved_families_returns_series_for_every_db(
    aggregator, dd_run_check, mock_http_response, fe_instance
):
    # Mocked at the HTTP boundary only: the FE scrape is the check's sole input.
    mock_http_response(file_path=FE_METRICS_FIXTURE)

    dd_run_check(CelerdataCheck("celerdata", {}, [fe_instance]))

    for db_name in EXPECTED_DATABASES:
        aggregator.assert_metric_has_tag("celerdata.fe.table_num", f"db_name:{db_name}")


def test_slow_lock_metrics_given_summary_families_returns_quantile_sum_and_count(
    aggregator, dd_run_check, mock_http_response, fe_instance
):
    # Mocked at the HTTP boundary only: the FE scrape is the check's sole input.
    mock_http_response(file_path=FE_METRICS_FIXTURE)

    dd_run_check(CelerdataCheck("celerdata", {}, [fe_instance]))

    for metric in SLOW_LOCK_METRICS:
        for suffix in ("quantile", "sum", "count"):
            aggregator.assert_metric(f"{metric}.{suffix}")
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
