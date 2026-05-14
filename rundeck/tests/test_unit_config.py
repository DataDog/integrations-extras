import pytest

from datadog_checks.base.errors import ConfigurationError
from datadog_checks.rundeck import RundeckCheck


def test_config_required_fields():
    config = {"url": "http://localhost:4440", "access_token": "super-token"}
    check = RundeckCheck("rundeck", {}, [config])
    check.load_configuration_models()

    assert check.config.url == config.get("url")
    assert check.config.access_token == config.get("access_token")
    assert check.config.api_version == 30


@pytest.mark.parametrize(
    "api_version",
    [
        31,
        30,
    ],
)
def test_config_required_and_optional_fields(api_version):
    config = {"url": "http://localhost:4440", "access_token": "super-token", "api_version": api_version}
    check = RundeckCheck("rundeck", {}, [config])
    check.load_configuration_models()

    assert check.config.url == config.get("url")
    assert check.config.access_token == config.get("access_token")
    assert check.config.api_version == api_version


@pytest.mark.parametrize(
    "config",
    [
        {"url": "http://localhost:4440"},
        {"access_token": "super-token"},
    ],
)
def test_config_missing_required_fields(config):
    with pytest.raises(ConfigurationError):
        check = RundeckCheck("rundeck", {}, [config])
        check.load_configuration_models()


def test_config_invalid_api_version():
    config = {"url": "http://localhost:4440", "access_token": "super-token", "api_version": 29}
    with pytest.raises(ConfigurationError, match="Minimum API version is 30"):
        check = RundeckCheck("rundeck", {}, [config])
        check.load_configuration_models()
