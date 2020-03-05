import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.pihole import PiholeCheck


@pytest.mark.unit
def test_config():
    instance = {}
    c = PiholeCheck('pihole', {}, [instance])

    # empty should fail
    with pytest.raises(ConfigurationError):
        c.check(instance)


# Testing integration status check using docker
@pytest.mark.integrations
@pytest.mark.usefixtures('dd_environment_pass')
def test_service_check(aggregator, instance_pass):
    c = PiholeCheck('pihole', {}, [instance_pass])

    c.check(instance_pass)
    aggregator.assert_service_check('pihole.running', PiholeCheck.OK)


# Testing known metric value using docker
@pytest.mark.integrations
@pytest.mark.usefixtures('dd_environment_pass')
def test_positive_response(aggregator, instance_pass):
    c = PiholeCheck('pihole', {}, [instance_pass])

    c.check(instance_pass)

    METRICS = {
        "pihole.domains_being_blocked": 125230.0,
        "pihole.ads_percent_blocked": 41.21003,
        "pihole.ads_blocked_today": 5490.0,
        "pihole.dns_queries_today": 13322.0,
        "pihole.unique_domains": 928.0,
        "pihole.reply_nxdomain": 15.0,
        "pihole.queries_cached": 1130.0,
        "pihole.queries_forwarded": 6702.0,
        "pihole.clients_ever_seen": 4.0,
        "pihole.unique_clients": 4.0,
        "pihole.reply_cname": 173.0,
        "pihole.reply_nodata": 12.0,
        "pihole.reply_ip": 317.0,
    }
    for metric, value in METRICS.items():
        aggregator.assert_metric(name=metric, value=value)

    aggregator.assert_all_metrics_covered()
