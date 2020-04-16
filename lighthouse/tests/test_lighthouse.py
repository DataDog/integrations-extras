import os

import pytest
from mock import MagicMock

from datadog_checks.base.errors import CheckException
from datadog_checks.lighthouse import LighthouseCheck

HERE = os.path.dirname(os.path.abspath(__file__))


def mock_get_lighthouse_report(cmd, lgr, re=False):
    if "https" not in cmd[1]:
        return "", "error", 1
    elif "404" in cmd[1]:
        with open(os.path.join(HERE, 'lighthouse_example_invalid_response.json'), 'r') as f:
            return f.read(), "", 0
    else:
        # example lighthouse report json for https://docs.datadoghq.com
        with open(os.path.join(HERE, 'lighthouse_example_valid_response.json'), 'r') as f:
            return f.read(), "", 0


@pytest.mark.integration
def test_check(aggregator, instance):
    instance = {'url': 'https://www.google.com', 'name': 'google'}
    lighthouse_check = LighthouseCheck('lighthouse', {}, {})
    LighthouseCheck._get_lighthouse_report = MagicMock(side_effect=mock_get_lighthouse_report)

    lighthouse_check.check(instance)

    tags = []
    tags.append("url:{0}".format(instance["url"]))
    tags.append("name:{0}".format(instance["name"]))

    aggregator.assert_metric(name="lighthouse.accessibility", value=86, tags=tags)
    aggregator.assert_metric(name="lighthouse.best_practices", value=79, tags=tags)
    aggregator.assert_metric(name="lighthouse.performance", value=74, tags=tags)
    aggregator.assert_metric(name="lighthouse.pwa", value=58, tags=tags)
    aggregator.assert_metric(name="lighthouse.seo", value=90, tags=tags)

    aggregator.assert_all_metrics_covered()


@pytest.mark.integration
def test_missing_url_instance_check(aggregator, instance):
    # incomplete instance in yaml missing url
    incomplete_instance = {'name': 'datadoghq'}
    lighthouse_check = LighthouseCheck('lighthouse', {}, {})
    LighthouseCheck._get_lighthouse_report = MagicMock(side_effect=mock_get_lighthouse_report)

    with pytest.raises(CheckException):
        lighthouse_check.check(incomplete_instance)


@pytest.mark.integration
def test_missing_name_instance_check(aggregator, instance):
    # incomplete instance in yaml missing name
    incomplete_instance = {'url': 'https://www.datadoghq.com'}
    lighthouse_check = LighthouseCheck('lighthouse', {}, {})
    LighthouseCheck._get_lighthouse_report = MagicMock(side_effect=mock_get_lighthouse_report)

    with pytest.raises(CheckException):
        lighthouse_check.check(incomplete_instance)


def test_malformed_url_instance_check(aggregator, instance):
    # example malformed url
    malformed_instance = {'url': 'htp://www.datadoghq.comz', 'name': 'malformed_url'}
    lighthouse_check = LighthouseCheck('lighthouse', {}, {})
    LighthouseCheck._get_lighthouse_report = MagicMock(side_effect=mock_get_lighthouse_report)

    with pytest.raises(CheckException):
        lighthouse_check.check(malformed_instance)


def test_invalid_response_check(aggregator, instance):
    # an example 404 response, will skip check but not throw error
    instance = {'url': 'https://httpstat.us/404', 'name': '404 response'}

    lighthouse_check = LighthouseCheck('lighthouse', {}, {})
    LighthouseCheck._get_lighthouse_report = MagicMock(side_effect=mock_get_lighthouse_report)

    lighthouse_check.check(instance)

    aggregator.assert_metric(name="lighthouse.accessibility", count=0, at_least=0)
    aggregator.assert_metric(name="lighthouse.best_practices", count=0, at_least=0)
    aggregator.assert_metric(name="lighthouse.performance", count=0, at_least=0)
    aggregator.assert_metric(name="lighthouse.pwa", count=0, at_least=0)
    aggregator.assert_metric(name="lighthouse.seo", count=0, at_least=0)
