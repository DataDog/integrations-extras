from datadog_checks.base.constants import ServiceCheck
from datadog_checks.dev.utils import assert_service_checks, get_metadata_metrics
from datadog_checks.spicedb import SpicedbCheck

from .util import get_fixture_path, get_expected_metrics


def test_metrics(aggregator, instance, dd_run_check, mock_http_response):
    mock_http_response(file_path=get_fixture_path("all_metrics.txt"))
    dd_run_check(SpicedbCheck("spicedb", {}, [instance]))

    tags = ["cluster:spicedb-cluster", "endpoint:http://localhost:9090/metrics", "node:1", "node_id:1"]

    # TODO:
    for metric in get_expected_metrics():
        aggregator.assert_metric("spicedb.{}".format(metric))
        for tag in tags:
            aggregator.assert_metric_has_tag("spicedb.{}".format(metric), tag)

    aggregator.assert_service_check("spicedb.prometheus.health", ServiceCheck.OK)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics(), check_submission_type=True)

    assert_service_checks(aggregator)


def test_emits_critical_service_check_when_service_is_down(dd_run_check, aggregator, instance):
    check = SpicedbCheck("spicedb", {}, [instance])
    dd_run_check(check)
    aggregator.assert_service_check("spicedb.prometheus.health", SpicedbCheck.CRITICAL)
