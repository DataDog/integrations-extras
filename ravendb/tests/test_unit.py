from pathlib import Path

import pytest

from datadog_checks.ravendb import RavendbCheck

from .common import METRICS
from .common_no_db_no_idx_no_collec_no_gc import METRICS_NO_DB_NO_IDX_NO_COLLEC_NO_GC
from .test_utils import (
    is_excluded_metric,
    metric_stubs,
    tags_contain_prefix,
)

FIXTURE = Path(__file__).parent / "fixtures" / "ravendb_metrics.txt"
FIXTURE_NO_DB = Path(__file__).parent / "fixtures" / "ravendb_metrics_no_db_metrics.txt"
FIXTURE_NO_DB_NO_IDX = Path(__file__).parent / "fixtures" / "ravendb_metrics_no_db_idx_metrics.txt"
FIXTURE_NO_DB_NO_IDX_NO_COLLEC = Path(__file__).parent / "fixtures" / "ravendb_metrics_no_db_idx_collec_metrics.txt"
FIXTURE_NO_DB_NO_IDX_NO_COLLEC_NO_GC = (
    Path(__file__).parent / "fixtures" / "ravendb_metrics_no_db_idx_collec_gc_metrics.txt"
)

METRIC_WITH_LABELS = "ravendb.server.info"
EXCLUDED_LABEL_PREFIXES = [
    "server_urls:",
    "public_server_url:",
    "tcp_server_urls:",
    "public_tcp_server_urls:",
    "well_known_admin_issuers:",
]


def test_check_default(dd_run_check, aggregator, instance, mock_http_response):
    mock_http_response(file_path=FIXTURE_NO_DB_NO_IDX_NO_COLLEC_NO_GC)
    check = RavendbCheck("ravendb", {}, [instance])

    dd_run_check(check)

    for m in METRICS_NO_DB_NO_IDX_NO_COLLEC_NO_GC:
        if is_excluded_metric(m, instance):
            continue
        aggregator.assert_metric(m)

    assert not aggregator.metrics("ravendb.gc.heap.size.mb")
    assert not aggregator.metrics("ravendb.database.statistics.requests.count")
    assert not aggregator.metrics("ravendb.index.status")
    assert not aggregator.metrics("ravendb.collection.documents.count")

    aggregator.assert_all_metrics_covered()


def test_check_all_enabled(dd_run_check, aggregator, instance, mock_http_response):
    mock_http_response(file_path=FIXTURE)

    instance["enable_gc_metrics"] = True
    instance["enable_database_metrics"] = True
    instance["enable_index_metrics"] = True
    instance["enable_collection_metrics"] = True

    check = RavendbCheck("ravendb", {}, [instance])

    dd_run_check(check)

    for m in METRICS:
        if is_excluded_metric(m, instance):
            continue
        aggregator.assert_metric(m)

    aggregator.assert_all_metrics_covered()


def test_check_no_db_metrics(dd_run_check, aggregator, instance, mock_http_response):
    mock_http_response(file_path=FIXTURE_NO_DB)

    instance["enable_gc_metrics"] = True
    instance["enable_index_metrics"] = True
    instance["enable_collection_metrics"] = True

    check = RavendbCheck("ravendb", {}, [instance])

    dd_run_check(check)

    for m in METRICS:
        if is_excluded_metric(m, instance):
            continue
        aggregator.assert_metric(m)

    assert not aggregator.metrics("ravendb.database.statistics.requests.count")

    aggregator.assert_all_metrics_covered()


def test_emits_critical_service_check_when_service_is_down(dd_run_check, aggregator, instance, mock_http_response):
    mock_http_response(status_code=404)
    check = RavendbCheck('ravendb', {}, [instance])
    with pytest.raises(Exception, match="requests.exceptions.HTTPError"):
        dd_run_check(check)

    aggregator.assert_service_check('ravendb.openmetrics.health', RavendbCheck.CRITICAL)


def test_rename_labels_applied(dd_run_check, aggregator, instance, mock_http_response):
    mock_http_response(file_path=FIXTURE)

    check = RavendbCheck("ravendb", {}, [instance])
    dd_run_check(check)

    stubs = metric_stubs(aggregator, METRIC_WITH_LABELS)

    # renamed prom labels should appear as dd tags
    assert tags_contain_prefix(stubs, "ravendb_cluster_id:")
    assert tags_contain_prefix(stubs, "ravendb_server_version:")
    assert tags_contain_prefix(stubs, "ravendb_server_full_version:")
    # original porm label keys should not appear
    assert not tags_contain_prefix(stubs, "cluster_id:")
    assert not tags_contain_prefix(stubs, "server_version:")
    assert not tags_contain_prefix(stubs, "server_full_version:")


def test_metric_patterns_exclude_prevents_emission(dd_run_check, aggregator, instance, mock_http_response):
    mock_http_response(file_path=FIXTURE_NO_DB_NO_IDX_NO_COLLEC)

    check = RavendbCheck("ravendb", {}, [instance])

    dd_run_check(check)

    with pytest.raises(AssertionError):
        aggregator.assert_metric("ravendb.database.uptime.seconds")

    with pytest.raises(AssertionError):
        aggregator.assert_metric("ravendb.index.time.since.last.query.seconds")

    with pytest.raises(AssertionError):
        aggregator.assert_metric("ravendb.collection.documents.count")

    aggregator.assert_metric("ravendb.server.uptime.seconds")
