import pytest, os, json
from mock import Mock
from datadog_checks.appkeeper.appkeeper import AppKeeperCheck
from datadog_checks.base import ConfigurationError
from datadog_checks.base.errors import CheckException


@pytest.mark.unit
def test_config():
    c = AppKeeperCheck()

    # An empty instance
    with pytest.raises(ConfigurationError):
        instance = {}
        c.check(instance)

    # Lack of account
    with pytest.raises(ConfigurationError):
        instance = {'integrationToken': 'xxx'}
        c.check(instance)

    # Lack of token
    with pytest.raises(ConfigurationError):
        instance = {'account': '000000000000'}
        c.check(instance)

def test_check(aggregator):
    c = AppKeeperCheck()
    c.get_token = Mock(return_value='xxx')
    c.get_events = Mock(side_effect=mock_call_events_api)
    c.get_instances = Mock(side_effect=mock_call_instances_api)
    instance = {'account': '000000000000', 'integrationToken': 'xxx'}
    c.check(instance)

    # aggregator.assert_all_metrics_covered()

def mock_call_events_api(account, token):
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'events_data.json'), 'r') as f:
        return json.load(f)

def mock_call_instances_api(account, token):
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'instances_data.json'), 'r') as f:
        return json.load(f)
