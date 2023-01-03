import json
import os

import pytest
from mock import MagicMock, patch
from requests import HTTPError, Timeout
from tests.common import HERE

from datadog_checks.unifi_console.config import UnifiConfig
from datadog_checks.unifi_console.errors import APIConnectionError, Unauthorized
from datadog_checks.unifi_console.types import (
    APIClientPath,
    APIDevicePath,
    APILoginPath,
    APILoginPathNew,
    APIPrefixNew,
    APIStatusPath,
    ControllerInfo,
)
from datadog_checks.unifi_console.unifi import Unifi


@pytest.mark.parametrize(
    "status_code, expected",
    [
        (
            200,
            True,
        ),
        (
            400,
            False,
        ),
    ],
)
def test__checkNewStyleAPI(instance, status_code, expected):
    with patch("requests.get") as mock_request:
        mock_request.return_value.status_code = status_code
        config = UnifiConfig(instance)
        api = Unifi(config, MagicMock(), MagicMock())

        assert api.new is expected


def test__checkNewStyleAPI_raise(instance):
    with patch("requests.get") as mock_request:
        config = UnifiConfig(instance)

        mock_request.side_effect = authetication_error(401)
        with pytest.raises(Unauthorized):
            Unifi(config, MagicMock(), MagicMock())

        mock_request.side_effect = authetication_error(400)
        with pytest.raises(HTTPError):
            Unifi(config, MagicMock(), MagicMock())

        mock_request.side_effect = Timeout()
        with pytest.raises(Timeout):
            Unifi(config, MagicMock(), MagicMock())


@pytest.mark.usefixtures("mock___checkNewStyleAPI")
def test__init(instance):
    config = UnifiConfig(instance)
    api = Unifi(config, MagicMock(), MagicMock())

    assert api.new is False


@pytest.mark.usefixtures("mock___checkNewStyleAPI")
def test_connection_success(instance):
    config = UnifiConfig(instance)
    api = Unifi(config, MagicMock(), MagicMock())
    try:
        api.login()
    except Exception as e:
        raise AssertionError(f"connect raised an exception: {e}")


@pytest.mark.usefixtures("mock___checkNewStyleAPI")
def test_connection_failure(instance):
    config = UnifiConfig(instance)
    http = MagicMock()
    http.post.side_effect = Exception("foo")
    api = Unifi(config, http, MagicMock())

    with pytest.raises(APIConnectionError):
        api.login()


@pytest.mark.usefixtures("mock___checkNewStyleAPI")
def test_status(instance):
    with patch("datadog_checks.unifi_console.unifi.Unifi._get_json") as mock__get_json, open(
        os.path.join(HERE, "fixtures", "status_valid.json")
    ) as f:
        mock__get_json.return_value = json.load(f)
        config = UnifiConfig(instance)
        api = Unifi(config, MagicMock(), MagicMock())
        status = api.status()

        mock__get_json.assert_called_once_with(APIStatusPath)
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
@pytest.mark.usefixtures("mock___checkNewStyleAPI")
def test_smart_retry(instance, exception, expected_calls):
    with patch("datadog_checks.unifi_console.unifi.Unifi._get_json") as mock__get_json:
        config = UnifiConfig(instance)
        api = Unifi(config, MagicMock(), MagicMock())
        mock__get_json.side_effect = [exception, "success"]
        try:
            api.get_devices_info()
        except Exception:
            pass
        assert mock__get_json.call_count == expected_calls


@pytest.mark.usefixtures("mock___checkNewStyleAPI")
def test_get_devices_metrics(instance):
    with patch("datadog_checks.unifi_console.unifi.Unifi._get_json") as mock__get_json, open(
        os.path.join(HERE, "fixtures", "device_metrics.json")
    ) as f:
        data = json.load(f)
        mock__get_json.return_value = data
        config = UnifiConfig(instance)
        api = Unifi(config, MagicMock(), MagicMock())
        devices = api.get_devices_info()

        mock__get_json.assert_called_once_with(APIDevicePath.format(config.site))
        assert isinstance(devices, list)
        assert len(devices) == 1


@pytest.mark.usefixtures("mock___checkNewStyleAPI")
def test_get_clients_metrics(instance):
    with patch("datadog_checks.unifi_console.unifi.Unifi._get_json") as mock__get_json, open(
        os.path.join(HERE, "fixtures", "client_metrics.json")
    ) as f:
        data = json.load(f)
        mock__get_json.return_value = data
        config = UnifiConfig(instance)
        api = Unifi(config, MagicMock(), MagicMock())
        clients = api.get_clients_info()

        mock__get_json.assert_called_once_with(APIClientPath.format(config.site))
        assert isinstance(clients, list)
        assert len(clients) == 1


@pytest.mark.parametrize(
    "newAPI, path, expect",
    [
        (
            False,
            APILoginPath,
            APILoginPath,
        ),
        (
            True,
            APILoginPath,
            APILoginPathNew,
        ),
        (
            True,
            APIStatusPath,
            APIPrefixNew + APIStatusPath,
        ),
        (
            True,
            APILoginPathNew,
            APILoginPathNew,
        ),
        (
            True,
            '/proxy/network/test',
            '/proxy/network/test',
        ),
    ],
)
@pytest.mark.usefixtures("mock___checkNewStyleAPI")
def test__path(instance, newAPI, path, expect):
    config = UnifiConfig(instance)
    api = Unifi(config, MagicMock(), MagicMock())

    api.new = newAPI
    p = api._Unifi__path(path)
    assert p == expect


@pytest.mark.usefixtures("mock___checkNewStyleAPI")
def test__get_json(instance):
    http = MagicMock()
    config = UnifiConfig(instance)
    api = Unifi(config, http, MagicMock())

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
