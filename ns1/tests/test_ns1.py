import json

import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.ns1 import Ns1Check


def test_empty_instance(aggregator, instance_empty):
    check = Ns1Check('ns1', {}, [instance_empty])
    with pytest.raises(ConfigurationError):
        check.checkConfig()


def test_config(aggregator, instance):
    check = Ns1Check('ns1', {}, [instance])
    check.checkConfig()
    assert check.api_endpoint is not None
    aggregator.assert_all_metrics_covered()


def test_no_metrics(aggregator, instance_nometrics):
    check = Ns1Check('ns1', {}, [instance_nometrics])
    with pytest.raises(ConfigurationError):
        check.checkConfig()

    # aggregator.assert_all_metrics_covered()
    # aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_parse_metrics(aggregator, instance):
    check = Ns1Check('ns1', {}, [instance])
    check.checkConfig()
    metric = instance["metrics"]

    assert len(metric) > 0
    assert check.api_endpoint is not None


def test_url_gen(aggregator, instance_1):
    check = Ns1Check('ns1', {}, [instance_1])
    check.checkConfig()
    aggregator.assert_all_metrics_covered()

    checkUrl = check.createUrl(check.metrics, check.query_params)

    if check.query_params:
        query_params = check.query_params
        query_string = "?"
        query_string = query_string + "period=" + query_params["pulsar_period"] + "&"
        query_string = query_string + "geo=" + query_params["pulsar_geo"] + "&"
        query_string = query_string + "asn=" + query_params["pulsar_asn"] + "&"
        query_string = query_string[:-1]
        assert query_string == "?period=1m&geo=*&asn=*"
        assert check.query_params["pulsar_period"] == "1m"

    assert len(checkUrl) > 0
    assert check.api_endpoint is not None
    assert checkUrl["qps"][0] == "https://my.nsone.net/v1/stats/qps"
    assert checkUrl["qps.dloc.com"][0] == "https://my.nsone.net/v1/stats/qps/dloc.com"
    assert checkUrl["account.ttl.dloc.com"][0] == "https://my.nsone.net/v1/zones/dloc.com"
    assert checkUrl["account.ttl.dloc.com"][2] == ["record:dloc.com"]

    expect = "https://my.nsone.net/v1/pulsar/query/decision/customer?period=1m&geo=*&asn=*&agg=avg"
    assert checkUrl["pulsar.decisions"][0] == expect
    expect = "https://my.nsone.net/v1/pulsar/apps/1xy4sn3/jobs/1xtvhvx/data?period=1m&geo=*&asn=*"
    assert checkUrl["pulsar.performance.1xy4sn3.1xtvhvx"][0] == expect
    expect = "https://my.nsone.net/v1/pulsar/apps/1xy4sn3/jobs/1xtvhvx/availability?period=1m&geo=*&asn=*"
    assert checkUrl["pulsar.availability.1xy4sn3.1xtvhvx"][0] == expect


def test_get_pulsar_app(aggregator, instance_1):
    check = Ns1Check('ns1', {}, [instance_1])
    check.checkConfig()
    pulsar_apps = check.getPulsarApplications()
    print(pulsar_apps)

    assert len(pulsar_apps) > 0
    key = next(iter(pulsar_apps))
    assert pulsar_apps[key][0] == "Pulsar community"
    assert pulsar_apps["1xy4sn3"][0] == "Pulsar community"
    jobs = pulsar_apps[key][1]
    found = False
    for job in jobs:
        if job["jobid"] == "1xtvhvx":
            found = True
    assert found


USAGE_RESULT = """
[
    {
        "jobs": 1,
        "graph": [
            [
                1619217000,
                1408
            ],
            [
                1619218800,
                1410
            ],
            [
                1619220600,
                758
            ]
        ],
        "period": "1h",
        "zones": 8,
        "records": 23,
        "queries": 3576,
        "feeds": 3
    }
]
"""


def test_usage_count(aggregator, instance_1):
    check = Ns1Check('ns1', {}, [instance_1])
    check.checkConfig()
    # checkUrl = check.createUrl(check.metrics)
    check.usage_count = {"test": [0, 0]}
    usage = check.extractUsageCount("test", json.loads(USAGE_RESULT))

    assert usage == 758
    assert check.usage_count["test"] == [1619220600, 758]


def test_read_prev_usage_count(aggregator, instance_1):
    check = Ns1Check('ns1', {}, [instance_1])
    check.checkConfig()
    check.usage_count_path = "./log"
    check.usage_count_fname = 'ns1_usage_count.txt'
    check.getUsageCount()

    assert check.usage_count["usage"] == [0, 0]
