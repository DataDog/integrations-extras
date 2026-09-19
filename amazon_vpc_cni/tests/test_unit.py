import pytest

from datadog_checks.amazon_vpc_cni import AmazonVpcCniCheck
from datadog_checks.base.constants import ServiceCheck
from datadog_checks.dev.utils import get_metadata_metrics

from .common import BAD_HOSTNAME_INSTANCE, EXPECTED_PROMETHEUS_METRICS

pytestmark = [pytest.mark.unit]


def test_connect_exception(dd_run_check, aggregator, caplog):
    with pytest.raises(Exception, match="Failed to resolve 'invalid-hostname'|Max retries exceeded"):
        check = AmazonVpcCniCheck('amazon_vpc_cni', {}, [BAD_HOSTNAME_INSTANCE])
        dd_run_check(check)

    aggregator.assert_service_check('amazon_vpc_cni.openmetrics.health', ServiceCheck.CRITICAL)


def test_check_mock_amazon_vpc_cni_metrics(dd_run_check, aggregator, check, mock_prometheus_metrics):
    dd_run_check(check)
    for metric_name in EXPECTED_PROMETHEUS_METRICS:
        aggregator.assert_metric(metric_name, at_least=1)
    aggregator.assert_metrics_using_metadata(get_metadata_metrics(), check_symmetric_inclusion=True)

    aggregator.assert_service_check('amazon_vpc_cni.openmetrics.health', ServiceCheck.OK)


def test_empty_instance(dd_run_check):
    with pytest.raises(
        Exception,
        match='\nopenmetrics_endpoint\n  Field required',
    ):
        check = AmazonVpcCniCheck('amazon_vpc_cni', {}, [{}])
        dd_run_check(check)
