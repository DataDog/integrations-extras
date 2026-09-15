import pytest


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_connect_ok(dd_run_check, aggregator, instance):
    from datadog_checks.amazon_vpc_cni import AmazonVpcCniCheck
    from datadog_checks.base.constants import ServiceCheck

    check = AmazonVpcCniCheck('amazon_vpc_cni', {}, [instance])
    dd_run_check(check)
    aggregator.assert_service_check('amazon_vpc_cni.openmetrics.health', ServiceCheck.OK)
