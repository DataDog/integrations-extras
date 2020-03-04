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
    aggregator.assert_metric(name="pihole.domains_being_blocked", value=125230.0)
    aggregator.assert_metric(name="pihole.ads_percent_blocked", value=41.21003)
    aggregator.assert_metric(name="pihole.ads_blocked_today", value=5490.0)
    aggregator.assert_metric(name="pihole.dns_queries_today", value=13322.0)
    aggregator.assert_metric(name="pihole.unique_domains", value=928.0)
    aggregator.assert_metric(name="pihole.reply_nxdomain", value=15.0)
    aggregator.assert_metric(name="pihole.queries_cached", value=1130.0)
    aggregator.assert_metric(name="pihole.queries_forwarded", value=6702.0)
    aggregator.assert_metric(name="pihole.clients_ever_seen", value=4.0)
    aggregator.assert_metric(name="pihole.unique_clients", value=4.0)
    aggregator.assert_metric(name="pihole.reply_cname", value=173.0)
    aggregator.assert_metric(name="pihole.reply_nodata", value=12.0)
    aggregator.assert_metric(name="pihole.reply_ip", value=317.0)

    aggregator.assert_all_metrics_covered()
