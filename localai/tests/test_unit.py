from unittest import mock

import pytest

from datadog_checks.base.constants import ServiceCheck
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.localai import LocalAICheck

from .common import BAD_HOSTNAME_INSTANCE, EXPECTED_PROMETHEUS_METRICS

pytestmark = [pytest.mark.unit]


def test_connect_exception(dd_run_check, aggregator):
    with pytest.raises(Exception, match="Failed to resolve 'invalid-hostname'|Max retries exceeded"):
        check = LocalAICheck('localai', {}, [BAD_HOSTNAME_INSTANCE])
        dd_run_check(check)

    aggregator.assert_service_check('localai.openmetrics.health', ServiceCheck.CRITICAL)


def test_check_mock_localai_metrics(dd_run_check, aggregator, check, mock_prometheus_metrics):
    dd_run_check(check)

    for metric_name in EXPECTED_PROMETHEUS_METRICS:
        aggregator.assert_metric(metric_name, at_least=1)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics(), check_symmetric_inclusion=True)
    aggregator.assert_service_check('localai.openmetrics.health', ServiceCheck.OK)


def test_labels(dd_run_check, aggregator, check, mock_prometheus_metrics):
    dd_run_check(check)

    endpoint_tag = 'endpoint:' + check.instance['openmetrics_endpoint']
    user_tag = 'user:f438cd9d-3abb-4c5c-a91b-70ada559e0ed'
    aggregator.assert_metric(
        'localai.tokens.count',
        value=140,
        tags=[endpoint_tag, user_tag, 'served_model:stories', 'kind:completion'],
    )
    aggregator.assert_metric(
        'localai.billed_requests.count',
        value=5,
        tags=[endpoint_tag, user_tag, 'served_model:stories', 'api_endpoint:/v1/chat/completions'],
    )
    aggregator.assert_metric(
        'localai.failover.target_up', value=0, metric_type=aggregator.GAUGE, tags=[endpoint_tag, 'target:broken']
    )
    aggregator.assert_metric(
        'localai.failover.switches.count',
        value=1,
        tags=[endpoint_tag, 'chain:chain', 'from:broken', 'to:stories', 'reason:trip'],
    )
    aggregator.assert_metric_has_tag('localai.request.duration.count', 'path:/v1/chat/completions')


def test_requests_uncompressed_metrics(dd_run_check, check):
    with mock.patch('requests.Session.get') as get:
        get.return_value = mock.MagicMock(
            status_code=200, iter_lines=lambda **kwargs: [], headers={'Content-Type': 'text/plain'}, close=lambda: None
        )
        dd_run_check(check)

    assert get.call_args.kwargs['headers']['Accept-Encoding'] == 'identity'


def test_empty_instance(dd_run_check):
    with pytest.raises(
        Exception,
        match='\nopenmetrics_endpoint\n  Field required',
    ):
        check = LocalAICheck('localai', {}, [{}])
        dd_run_check(check)
