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
    instance = {"host": "localhost:8888/fail", "token": "abcdefghijklmnop"}
    c = PiholeCheck('pihole', {}, [instance])
    with pytest.raises(Exception):
        c.check(instance)
        aggregator.assert_service_check('pihole.running', PiholeCheck.CRITICAL)


# Testing integration status check using docker - bad "status" returned
@pytest.mark.integrations
@pytest.mark.usefixtures('dd_environment_pass')
def test_bad_status(aggregator):
    instance = {"host": "localhost:8888/bad_status", "token": "abcdefghijklmnop"}
    c = PiholeCheck('pihole', {}, [instance])
    with pytest.raises(Exception):
        c.check(instance)
        aggregator.assert_service_check('pihole.running', PiholeCheck.CRITICAL)


# Testing integration status check using docker - no "status" returned
@pytest.mark.integrations
@pytest.mark.usefixtures('dd_environment_pass')
def test_no_status(aggregator):
    instance = {"host": "localhost:8888/no_status", "token": "abcdefghijklmnop"}
    c = PiholeCheck('pihole', {}, [instance])
    with pytest.raises(Exception):
        c.check(instance)
        aggregator.assert_service_check('pihole.running', PiholeCheck.CRITICAL)


# Testing known metric value using docker - valid response
@pytest.mark.integrations
#@pytest.mark.usefixtures('dd_environment_pass')
def test_good_response(aggregator, instance_pass):
    instance = {"host": "None", "type": "None"}
    c = PiholeCheck('pihole', {}, [instance_pass])

    c.check(instance_pass)

    METRICS = {
        # Pihole metrics are actually strings
        # and use thousand-separators
        "pihole.domains_being_blocked": "125,230",
        "pihole.dns_queries_today": "13,322",
        "pihole.ads_blocked_today": "5,490",
        # The only non thousand-separator
        # metric is ads_percentage_today
        "pihole.ads_percentage_today": "5.6",
        "pihole.unique_domains": "3,928",
        "pihole.queries_forwarded": "6,702",
        "pihole.queries_cached": "1,130",
        "pihole.clients_ever_seen": "4",
        "pihole.unique_clients": "4",
        "pihole.dns_queries_all_types": "13,322",
        "pihole.reply_nodata": "12",
        "pihole.reply_nxdomain": "15",
        "pihole.reply_cname": "173.0",
        "pihole.reply_ip": "317",
    }
    for metric, value in METRICS.items():
        aggregator.assert_metric(name=metric, value=value)

    aggregator.assert_all_metrics_covered()
