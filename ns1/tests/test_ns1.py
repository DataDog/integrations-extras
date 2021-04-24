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
    print(metric)
    assert len(metric) > 0
    assert check.api_endpoint is not None
    # raise AssertionError("not error")


def test_url_gen(aggregator, instance_1):
    check = Ns1Check('ns1', {}, [instance_1])
    check.checkConfig()
    checkUrl = check.createUrl(check.metrics)

    assert len(checkUrl) > 0
    assert check.api_endpoint is not None
    assert checkUrl["qps"][0] == "https://my.nsone.net/v1/stats/qps"
    assert checkUrl["qps.test.com"][0] == "https://my.nsone.net/v1/stats/qps/test.com"


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
