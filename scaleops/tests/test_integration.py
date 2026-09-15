import pytest


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_connect_ok(dd_run_check, aggregator, instance):
    from datadog_checks.base.constants import ServiceCheck
    from datadog_checks.scaleops import ScaleopsCheck

    check = ScaleopsCheck('scaleops', {}, [instance])
    dd_run_check(check)
    aggregator.assert_service_check('scaleops.openmetrics.health', ServiceCheck.OK)
