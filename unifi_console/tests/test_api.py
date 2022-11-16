import json
import os

import pytest
from mock import MagicMock, patch
from requests import HTTPError, Timeout
from tests.common import HERE

from datadog_checks.unifi_console.api import UnifiAPI
from datadog_checks.unifi_console.config import UnifiConfig
from datadog_checks.unifi_console.errors import Unauthorized
from datadog_checks.unifi_console.types import APIConnectionError, ControllerInfo


def test__init(instance):
    config = UnifiConfig(instance, {}, MagicMock())
    api = UnifiAPI(config, MagicMock(), MagicMock())

    assert api.url is config.url
    assert api.auth_url == config.url + "/api/login"


def test_connection_success(instance):
    config = UnifiConfig(instance, {}, MagicMock())
    api = UnifiAPI(config, MagicMock(), MagicMock())
    try:
        api.connect()
    except Exception as e:
        raise AssertionError(f"connect raised an exception: {e}")


def test_connection_failure(instance):
    config = UnifiConfig(instance, {}, MagicMock())
    http = MagicMock()
    http.post.side_effect = Exception("foo")
    api = UnifiAPI(config, http, MagicMock())

    with pytest.raises(APIConnectionError):
        api.connect()


def test_status(instance):
    with patch("datadog_checks.unifi_console.api.UnifiAPI._get_json") as mock__get_json, open(
        os.path.join(HERE, "fixtures", "status_valid.json")
    ) as f:
        mock__get_json.return_value = json.load(f)
        config = UnifiConfig(instance, {}, MagicMock())
        api = UnifiAPI(config, MagicMock(), MagicMock())
        status = api.status()

        mock__get_json.assert_called_once_with("{}/status".format(config.url))
        assert type(status) is ControllerInfo
        assert status.up is True


def authetication_error(code):
    mock_response = MagicMock()
    mock_response.status_code = code
    return HTTPError(response=mock_response)


@pytest.mark.parametrize(
    "exception, expected_calls",
    [
        (
            Unauthorized(),
            2,
        ),
        (
            ConnectionError(),
            1,
        ),
        (
            Timeout(),
            1,
        ),
    ],
)
def test_smart_retry(instance, exception, expected_calls):
    with patch("datadog_checks.unifi_console.api.UnifiAPI._get_json") as mock__get_json:
        config = UnifiConfig(instance, {}, MagicMock())
        api = UnifiAPI(config, MagicMock(), MagicMock())
        mock__get_json.side_effect = [exception, "success"]
        try:
            api.get_devices_info()
        except Exception:
            pass
        assert mock__get_json.call_count == expected_calls


def test_get_devices_metrics(instance):
    with patch("datadog_checks.unifi_console.api.UnifiAPI._get_json") as mock__get_json, open(
        os.path.join(HERE, "fixtures", "device_metrics.json")
    ) as f:
        data = json.load(f)
        mock__get_json.return_value = data
        config = UnifiConfig(instance, {}, MagicMock())
        api = UnifiAPI(config, MagicMock(), MagicMock())
        devices = api.get_devices_info()

        mock__get_json.assert_called_once_with("{}/api/s/{}/stat/device/".format(config.url, config.site))
        assert isinstance(devices, list)
        assert len(devices) == 1


def test_get_clients_metrics(instance):
    with patch("datadog_checks.unifi_console.api.UnifiAPI._get_json") as mock__get_json, open(
        os.path.join(HERE, "fixtures", "client_metrics.json")
    ) as f:
        data = json.load(f)
        mock__get_json.return_value = data
        config = UnifiConfig(instance, {}, MagicMock())
        api = UnifiAPI(config, MagicMock(), MagicMock())
        clients = api.get_clients_info()

        mock__get_json.assert_called_once_with("{}/api/s/{}/stat/sta/".format(config.url, config.site))
        assert isinstance(clients, list)
        assert len(clients) == 1


def test__get_json(instance):
    http = MagicMock()
    config = UnifiConfig(instance, {}, MagicMock())
    api = UnifiAPI(config, http, MagicMock())

    try:
        api._get_json("foo")
    except Exception as e:
        raise AssertionError(f"_get_json raised an exception: {e}")

    http.get.side_effect = authetication_error(401)
    with pytest.raises(Unauthorized):
        api._get_json("foo")

    http.get.side_effect = authetication_error(400)
    with pytest.raises(HTTPError):
        api._get_json("foo")

    http.get.side_effect = Timeout()
    with pytest.raises(Timeout):
        api._get_json("foo")
