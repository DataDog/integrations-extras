from mock import Mock
import pytest
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
    return [
        {
            "status": "success",
            "checkStatus": None,
            "instanceId": "i-000000001",
            "eventId": "dummy_event_id1",
            "type": "recovery",
            "startTime": "2021-01-25T01:06:55.683Z",
            "endTime": "2021-01-25T01:07:07.594Z",
            "services": [
                "crond"
            ],
            "awsAccountId": "1234556789012",
            "region": "eu-central-1",
            "instanceName": "dummyInstance01",
            "coatiRecovery": True,
            "requester": "api",
            "faultLogId": None,
        },
        {
            "status": "success",
            "checkStatus": None,
            "instanceId": "i-000000002",
            "eventId": "dummy_event_id2",
            "type": "recovery",
            "startTime": "2021-01-25T00:50:45.274Z",
            "endTime": "2021-01-25T00:50:49.027Z",
            "services": [
                "crond"
            ],
            "awsAccountId": "123456789012",
            "region": "eu-central-1",
            "instanceName": "dummyInstance02",
            "coatiRecovery": True,
            "requester": "api",
            "faultLogId": None,
        },
        {
            "status": "success",
            "checkStatus": "success",
            "instanceId": "i-00000001",
            "eventId": "dummy_event_id3",
            "type": "recovery",
            "startTime": "2020-10-09T01:29:10.959Z",
            "endTime": "2020-10-09T01:29:27.673Z",
            "services": [
                "ntpd.service"
            ],
            "awsAccountId": "123456789012",
            "region": "eu-central-1",
            "instanceName": "dummyInstance01",
            "coatiRecovery": True,
            "requester": "coati",
            "faultLogId": None,
        },
    ]

def mock_call_instances_api(account, token):
    return [
        {
            "instanceId": "i-00000001",
            "instanceType": "t2.small",
            "instanceState": "running",
            "region": "ap-northeast-1",
            "tags": [],
            "state": "monitoringStopped",
            "configuration": "notMonitored",
            "check": False,
            "serviceSearchStatus": "success",
            "recovery": "full"
        },
        {
            "instanceId": "i-00000002",
            "instanceType": "t2.small",
            "instanceState": "stopped",
            "region": "ap-northeast-1",
            "tags": [],
            "state": "ssmNotAvailable",
            "configuration": "outOfMonitored",
            "check": False,
            "serviceSearchStatus": None,
            "recovery": "full"
        },
        {
            "instanceId": "i-00000003",
            "instanceType": "t3.small",
            "instanceState": "running",
            "region": "eu-central-1",
            "tags": [],
            "state": "monitoring",
            "configuration": "monitored",
            "check": True,
            "serviceSearchStatus": "success",
            "recovery": "apiOnly"
        },
    ]