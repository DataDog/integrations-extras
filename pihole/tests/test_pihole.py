import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.pihole import PiholeCheck


@pytest.mark.unit
def test_config():
    instance = {}

    # empty should fail
    with pytest.raises(ConfigurationError):
        c = PiholeCheck('pihole', {}, [instance])
        c.check(instance)


@pytest.mark.unit
def test_invalid_config(aggregator):
    instance = {"host": "www.google.com"}

    # Invalid host parameter - should fail
    with pytest.raises(Exception):
        c = PiholeCheck('pihole', {}, [instance])
        c.check(instance)
        aggregator.assert_service_check('pihole.running', PiholeCheck.CRITICAL)


# Testing integration status check using docker (200 endpoint)
@pytest.mark.integrations
@pytest.mark.usefixtures('dd_environment_pass')
def test_service_check(aggregator, instance_pass):
    c = PiholeCheck('pihole', {}, [instance_pass])

    c.check(instance_pass)
    aggregator.assert_service_check('pihole.running', PiholeCheck.OK)


# Testing integration status check using docker (404 endpoint) - no metrics returned
@pytest.mark.integrations
@pytest.mark.usefixtures('dd_environment_pass')
def test_bad_response(aggregator):
    instance = {"host": "localhost:8888/fail"}
    c = PiholeCheck('pihole', {}, [instance])
    with pytest.raises(Exception):
        c.check(instance)
        aggregator.assert_service_check('pihole.running', PiholeCheck.CRITICAL)


# Testing integration status check using docker - bad "status" returned
@pytest.mark.integrations
@pytest.mark.usefixtures('dd_environment_pass')
def test_bad_status(aggregator):
    instance = {"host": "localhost:8888/bad_status"}
    c = PiholeCheck('pihole', {}, [instance])
    with pytest.raises(Exception):
        c.check(instance)
        aggregator.assert_service_check('pihole.running', PiholeCheck.CRITICAL)


# Testing integration status check using docker - no "status" returned
@pytest.mark.integrations
@pytest.mark.usefixtures('dd_environment_pass')
def test_no_status(aggregator):
    instance = {"host": "localhost:8888/no_status"}
    c = PiholeCheck('pihole', {}, [instance])
    with pytest.raises(Exception):
        c.check(instance)
        aggregator.assert_service_check('pihole.running', PiholeCheck.CRITICAL)


# Testing known metric value using docker - valid response
@pytest.mark.integrations
@pytest.mark.usefixtures('dd_environment_pass')
def test_good_response(aggregator, instance_pass):
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
        "pihole.dns_queries_all_types": 13322.0,
        "pihole.reply_cname": 173.0,
        "pihole.reply_nodata": 12.0,
        "pihole.reply_ip": 317.0,
    }
    for metric, value in METRICS.items():
        aggregator.assert_metric(name=metric, value=value)

    aggregator.assert_all_metrics_covered()
