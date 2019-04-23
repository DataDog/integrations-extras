import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.traefik import TraefikCheck


def test_config(instance_invalid):
    c = TraefikCheck('traefik', {}, {}, None)

    with pytest.raises(ConfigurationError):
        c.check(instance_invalid)


def test_bad_url(aggregator, instance_bad):
    c = TraefikCheck('traefik', {}, {}, None)
    c.check(instance_bad)

    aggregator.assert_service_check('traefik.health', TraefikCheck.CRITICAL)


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_check(aggregator, instance):
    c = TraefikCheck('traefik', {}, {}, None)
    c.check(instance)

    aggregator.assert_metric('traefik.total_count', value=1)
    aggregator.assert_metric('traefik.total_status_code_count', value=1, tags=['status_code:404'])
    aggregator.assert_service_check('traefik.health', TraefikCheck.OK)
