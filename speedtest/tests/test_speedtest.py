from typing import Any, Dict  # noqa: F401

import mock
import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.base.stubs.aggregator import AggregatorStub  # noqa: F401
from datadog_checks.speedtest import MEGABYTE_TO_MEBIBYTE, SpeedtestCheck

MOCK_RESPONSE = {
    "type": "result",
    "timestamp": "2020-06-14T19:41:48Z",
    "ping": {"jitter": 10, "latency": 20},
    "download": {"bandwidth": 30 / MEGABYTE_TO_MEBIBYTE, "bytes": 40, "elapsed": 50},
    "upload": {"bandwidth": 60 / MEGABYTE_TO_MEBIBYTE, "bytes": 70, "elapsed": 80},
    "packetLoss": 90,
    "isp": "Some ISP",
    "interface": {
        "internalIp": "1.2.3.4",
        "name": "en0",
        "macAddr": "01:23:45:67:89:01",
        "isVpn": False,
        "externalIp": "2.3.4.5",
    },
    "server": {
        "id": 100,
        "name": "Foo",
        "location": "Somewhere, City",
        "country": "United States",
        "host": "foo.example.com",
        "port": 1234,
        "ip": "3.4.5.6",
    },
    "result": {
        "id": "01234567-0123-0123-0123-012345678901",
        "url": "https://www.speedtest.net/result/c/01234567-0123-0123-0123-012345678901",
    },
}


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
@mock.patch('datadog_checks.speedtest.SpeedtestCheck._call_command')
def test_check(mock_cmd, aggregator, instance):
    # type: (mock.MagicMock, AggregatorStub, Dict[str, Any]) -> None
    mock_cmd.return_value = MOCK_RESPONSE
    tags = sorted(
        [
            "foo:bar",
            "isp:{}".format(MOCK_RESPONSE["isp"]),
            "interface_name:{}".format(MOCK_RESPONSE["interface"]["name"]),
            "server_id:{}".format(MOCK_RESPONSE["server"]["id"]),
            "server_name:{}".format(MOCK_RESPONSE["server"]["name"]),
            "server_country:{}".format(MOCK_RESPONSE["server"]["country"]),
            "server_host:{}".format(MOCK_RESPONSE["server"]["host"]),
        ]
    )

    check = SpeedtestCheck('speedtest', {}, [instance])
    check.check(instance)
    aggregator.assert_service_check('speedtest.run', SpeedtestCheck.OK)
    aggregator.assert_event("", count=1, tags=tags, exact_match=False)
    aggregator.assert_metric("speedtest.ping.jitter", 10.0, tags=tags, count=1)
    aggregator.assert_metric("speedtest.ping.latency", 20.0, tags=tags, count=1)
    aggregator.assert_metric("speedtest.download.bandwidth", 30.0, tags=tags, count=1)
    aggregator.assert_metric("speedtest.download.bytes", 40.0, tags=tags, count=1)
    aggregator.assert_metric("speedtest.download.elapsed", 50.0, tags=tags, count=1)
    aggregator.assert_metric("speedtest.upload.bandwidth", 60.0, tags=tags, count=1)
    aggregator.assert_metric("speedtest.upload.bytes", 70.0, tags=tags, count=1)
    aggregator.assert_metric("speedtest.upload.elapsed", 80.0, tags=tags, count=1)
    aggregator.assert_metric("speedtest.packet_loss", 90.0, tags=tags, count=1)

    aggregator.assert_all_metrics_covered()


@pytest.mark.unit
@mock.patch('datadog_checks.speedtest.SpeedtestCheck._call_command')
def test_config(mock_cmd, *args, **kwargs):
    mock_cmd.return_value = MOCK_RESPONSE

    # okay to specify nothing
    instance = {}
    check = SpeedtestCheck('speedtest', {}, [instance])
    check.check(instance)

    # okay to specify a specific option
    instance = {"host": "foo.example.com"}
    check = SpeedtestCheck('speedtest', {}, [instance])
    check.check(instance)

    # not okay to specify more than one specific option
    instance = {"host": "foo.example.com", "ip": "1.2.3.4"}
    check = SpeedtestCheck('speedtest', {}, [instance])
    with pytest.raises(ConfigurationError):
        check.check(instance)
