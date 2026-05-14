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
@pytest.mark.usefixtures('dd_environment_pass')
def test_service_check(aggregator, instance_pass):
    c = PiholeCheck('pihole', {}, [instance_pass])

    c.check(instance_pass)
    aggregator.assert_service_check('pihole.running', PiholeCheck.OK)


# Testing integration status check using docker (404 endpoint) - no metrics returned
@pytest.mark.usefixtures('dd_environment_pass')
def test_bad_response(aggregator):
    instance = {"host": "localhost:8888/fail"}
    c = PiholeCheck('pihole', {}, [instance])
    with pytest.raises(Exception):
        c.check(instance)
        aggregator.assert_service_check('pihole.running', PiholeCheck.CRITICAL)


# Testing integration status check using docker - bad "status" returned
@pytest.mark.usefixtures('dd_environment_pass')
def test_bad_status(aggregator):
    instance = {"host": "localhost:8888/bad_status"}
    c = PiholeCheck('pihole', {}, [instance])
    with pytest.raises(Exception):
        c.check(instance)
        aggregator.assert_service_check('pihole.running', PiholeCheck.CRITICAL)


# Testing integration status check using docker - no "status" returned
@pytest.mark.usefixtures('dd_environment_pass')
def test_no_status(aggregator):
    instance = {"host": "localhost:8888/no_status"}
    c = PiholeCheck('pihole', {}, [instance])
    with pytest.raises(Exception):
        c.check(instance)
        aggregator.assert_service_check('pihole.running', PiholeCheck.CRITICAL)


# Testing known metric value using docker - valid response
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


# Testing integration status check using docker (200 endpoint)
@pytest.mark.usefixtures('v6_dd_environment_pass')
def test_service_check_v6(aggregator, v6_instance_pass):
    c = PiholeCheck('pihole', {}, [v6_instance_pass])

    c.check(v6_instance_pass)
    aggregator.assert_service_check('pihole.running', PiholeCheck.OK)


# Testing known metric value using docker - valid response
@pytest.mark.usefixtures('v6_dd_environment_pass')
def test_v6_metrics(aggregator, v6_instance_pass):
    c = PiholeCheck('pihole', {}, [v6_instance_pass])

    c.check(v6_instance_pass)

    V6_METRICS = {
        'pihole.clients.active': 0,
        'pihole.clients.total': 0,
        'pihole.gravity.domains_being_blocked': 79984,
        'pihole.gravity.last_update': 1759837296,
        'pihole.queries.blocked': 0,
        'pihole.queries.cached': 0,
        'pihole.queries.forwarded': 0,
        'pihole.queries.frequency': 0,
        'pihole.queries.percent_blocked': 0,
        'pihole.queries.replies.BLOB': 0,
        'pihole.queries.replies.CNAME': 0,
        'pihole.queries.replies.DNSSEC': 0,
        'pihole.queries.replies.DOMAIN': 0,
        'pihole.queries.replies.IP': 0,
        'pihole.queries.replies.NODATA': 0,
        'pihole.queries.replies.NONE': 0,
        'pihole.queries.replies.NOTIMP': 0,
        'pihole.queries.replies.NXDOMAIN': 0,
        'pihole.queries.replies.OTHER': 0,
        'pihole.queries.replies.REFUSED': 0,
        'pihole.queries.replies.RRNAME': 0,
        'pihole.queries.replies.SERVFAIL': 0,
        'pihole.queries.replies.UNKNOWN': 0,
        'pihole.queries.status.CACHE': 0,
        'pihole.queries.status.CACHE_STALE': 0,
        'pihole.queries.status.DBBUSY': 0,
        'pihole.queries.status.DENYLIST': 0,
        'pihole.queries.status.DENYLIST_CNAME': 0,
        'pihole.queries.status.EXTERNAL_BLOCKED_EDE15': 0,
        'pihole.queries.status.EXTERNAL_BLOCKED_IP': 0,
        'pihole.queries.status.EXTERNAL_BLOCKED_NULL': 0,
        'pihole.queries.status.EXTERNAL_BLOCKED_NXRA': 0,
        'pihole.queries.status.FORWARDED': 0,
        'pihole.queries.status.GRAVITY': 0,
        'pihole.queries.status.GRAVITY_CNAME': 0,
        'pihole.queries.status.IN_PROGRESS': 0,
        'pihole.queries.status.REGEX': 0,
        'pihole.queries.status.REGEX_CNAME': 0,
        'pihole.queries.status.RETRIED': 0,
        'pihole.queries.status.RETRIED_DNSSEC': 0,
        'pihole.queries.status.SPECIAL_DOMAIN': 0,
        'pihole.queries.status.UNKNOWN': 0,
        'pihole.queries.total': 0,
        'pihole.queries.types.A': 0,
        'pihole.queries.types.AAAA': 0,
        'pihole.queries.types.ANY': 0,
        'pihole.queries.types.DNSKEY': 0,
        'pihole.queries.types.DS': 0,
        'pihole.queries.types.HTTPS': 0,
        'pihole.queries.types.MX': 0,
        'pihole.queries.types.NAPTR': 0,
        'pihole.queries.types.NS': 0,
        'pihole.queries.types.OTHER': 0,
        'pihole.queries.types.PTR': 0,
        'pihole.queries.types.RRSIG': 0,
        'pihole.queries.types.SOA': 0,
        'pihole.queries.types.SRV': 0,
        'pihole.queries.types.SVCB': 0,
        'pihole.queries.types.TXT': 0,
        'pihole.queries.unique_domains': 0,
        'pihole.took': 4.076957702636719e-05,
    }

    for metric, value in V6_METRICS.items():
        aggregator.assert_metric(name=metric, value=value)

    aggregator.assert_all_metrics_covered()
