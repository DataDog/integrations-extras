import pytest


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_connect_ok(dd_run_check, aggregator, instance):
    from datadog_checks.base.constants import ServiceCheck
    from datadog_checks.external_secrets import ExternalSecretsCheck

    check = ExternalSecretsCheck('external_secrets', {}, [instance])
    dd_run_check(check)
    aggregator.assert_service_check('external_secrets.openmetrics.health', ServiceCheck.OK)
