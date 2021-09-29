from datadog_checks.vespa import VespaCheck
from datadog_checks.base.errors import CheckException
import os
import json
import pytest
from mock import MagicMock

HERE = os.path.dirname(os.path.abspath(__file__))


def test_no_consumer_raises():
    check = VespaCheck("vespa", {}, {})
    with pytest.raises(CheckException):
        check.check({})


def test_cannot_connect_is_critical(aggregator):
    check = VespaCheck("vespa", {}, {})
    check.URL = 'http://localhost:19333/state/v1/metrics'
    check.check({'consumer': 'default'})
    aggregator.assert_service_check(check.METRICS_SERVICE_CHECK,
                                    VespaCheck.CRITICAL,
                                    count=1)
    aggregator.assert_service_check(check.METRICS_SERVICE_CHECK,
                                    VespaCheck.WARNING,
                                    count=0)


def test_no_services_object_in_json_yields_metrics_health_warning(aggregator):
    check = VespaCheck("vespa", {}, {})
    with open(os.path.join(HERE, 'no_services_object.json'), 'r') as f:
        check._get_metrics_json = MagicMock(return_value=json.load(f))
    check.check({'consumer': 'default'})
    aggregator.assert_service_check(check.METRICS_SERVICE_CHECK,
                                    VespaCheck.WARNING,
                                    count=1,
                                    message="No services in response from metrics proxy on " +
                                            check.URL + "?consumer=default")


def test_service_reports_down(aggregator):
    check = VespaCheck("vespa", {}, {})
    with open(os.path.join(HERE, 'service_down.json'), 'r') as f:
        check._get_metrics_json = MagicMock(return_value=json.load(f))
    check.check({'consumer': 'default', 'tags': ['tag1:val1']})
    aggregator.assert_service_check(check.PROCESS_SERVICE_CHECK,
                                    VespaCheck.CRITICAL,
                                    count=1,
                                    message='Service vespa.down-service reports down: No response',
                                    tags=['instance:down-service', 'vespaVersion:7.0.0',
                                          'vespa-service:vespa.down-service', 'tag1:val1'])
    aggregator.assert_service_check(check.PROCESS_SERVICE_CHECK, VespaCheck.OK, count=0)


def test_service_reports_unknown(aggregator):
    check = VespaCheck("vespa", {}, {})
    with open(os.path.join(HERE, 'service_unknown.json'), 'r') as f:
        check._get_metrics_json = MagicMock(return_value=json.load(f))
    check.check({'consumer': 'default', 'tags': ['tag1:val1']})
    aggregator.assert_service_check(check.PROCESS_SERVICE_CHECK,
                                    VespaCheck.WARNING,
                                    count=1,
                                    message='Service vespa.unknown-service reports unknown status: Empty status page',
                                    tags=['instance:unknown-service', 'vespaVersion:7.0.0',
                                          'vespa-service:vespa.unknown-service', 'tag1:val1'])
    aggregator.assert_service_check(check.PROCESS_SERVICE_CHECK, VespaCheck.OK, count=0)


def test_down_service_does_not_raise(aggregator):
    check = VespaCheck("vespa", {}, {})
    with open(os.path.join(HERE, 'service_up_and_down.json'), 'r') as f:
        check._get_metrics_json = MagicMock(return_value=json.load(f))
    check.check({'consumer': 'default', 'tags': ['tag1:val1']})
    aggregator.assert_service_check(check.PROCESS_SERVICE_CHECK,
                                    VespaCheck.CRITICAL,
                                    count=1,
                                    message='Service vespa.down-service reports down: No response',
                                    tags=['instance:down-service', 'vespaVersion:7.0.0',
                                          'vespa-service:vespa.down-service', 'tag1:val1'])
    aggregator.assert_service_check(check.PROCESS_SERVICE_CHECK,
                                    VespaCheck.OK,
                                    count=1,
                                    tags=['instance:up-service', 'vespaVersion:7.0.0',
                                          'vespa-service:vespa.up-service', 'tag1:val1'])
    assert 3 == check.metric_count


def test_check_metrics(aggregator):
    check = VespaCheck("vespa", {}, {})
    with open(os.path.join(HERE, 'metrics_all.json'), 'r') as f:
        check._get_metrics_json = MagicMock(return_value=json.load(f))

    check.check({'consumer': 'default', 'tags': ['tag1:val1']})
    aggregator.assert_service_check(check.PROCESS_SERVICE_CHECK, VespaCheck.OK, count=7)
    aggregator.assert_service_check(check.PROCESS_SERVICE_CHECK, VespaCheck.WARNING, count=0)
    aggregator.assert_service_check(check.METRICS_SERVICE_CHECK, VespaCheck.OK, count=1)

    aggregator.assert_metric("vespa.http.status.2xx.rate",
                             value=10,
                             tags=['metrictype:standard', 'instance:container', 'scheme:http', 'httpMethod:GET',
                                   'clustername:default', 'vespaVersion:7.0.0', 'vespa-service:vespa.container',
                                   'tag1:val1'])
    aggregator.assert_metric("vespa.http.status.2xx.rate", count=5)
    assert_number_of_metrics_and_services(check)


def test_check_counters_are_reset_between_check_calls():
    check = VespaCheck("vespa", {}, {})
    with open(os.path.join(HERE, 'metrics_all.json'), 'r') as f:
        check._get_metrics_json = MagicMock(return_value=json.load(f))
    for _ in 1, 2:
        check.check({'consumer': 'default'})
        assert_number_of_metrics_and_services(check)


def assert_number_of_metrics_and_services(check):
    assert 38 == check.metric_count
    assert 7 == check.services_up
