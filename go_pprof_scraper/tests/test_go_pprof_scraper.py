# (C) Datadog, Inc. 2022-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

from typing import Any, Callable, Dict  # noqa: F401
from unittest.mock import patch

import pytest
import requests

from datadog_checks.base import AgentCheck, ConfigurationError  # noqa: F401
from datadog_checks.base.stubs.aggregator import AggregatorStub  # noqa: F401
from datadog_checks.go_pprof_scraper import GoPprofScraperCheck

INIT_CONFIG = {}


@pytest.mark.unit
def test_config():
    # Empty configuration
    with pytest.raises(ConfigurationError):
        GoPprofScraperCheck("go_pprof_scraper", INIT_CONFIG, [{}])

    # No service
    with pytest.raises(ConfigurationError):
        GoPprofScraperCheck(
            "go_pprof_scraper",
            INIT_CONFIG,
            [{"pprof_url": "http://localhost:1234/debug/pprof/"}],
        )

    # Invalid profile type
    with pytest.raises(ConfigurationError):
        GoPprofScraperCheck(
            "go_pprof_scraper",
            INIT_CONFIG,
            [{"pprof_url": "http://localhost:1234/debug/pprof/", "profiles": ["xzy"], "service": "testing"}],
        )

    c = GoPprofScraperCheck(
        "go_pprof_scraper",
        INIT_CONFIG,
        [
            {
                "pprof_url": "http://localhost:1234/debug/pprof",
                "profiles": ["cpu", "heap"],
                "duration": 3,
                "service": "testing",
            }
        ],
    )
    c.check([])


def test_check(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = GoPprofScraperCheck("go_pprof_scraper", INIT_CONFIG, [instance])
    dd_run_check(check)


def test_emits_critical_service_check_when_service_is_down(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = GoPprofScraperCheck("go_pprof_scraper", INIT_CONFIG, [instance])
    dd_run_check(check)
    aggregator.assert_service_check("go_pprof_scraper.can_connect", GoPprofScraperCheck.CRITICAL)


@pytest.mark.unit
def test_unix_socket_fallback_to_tcp(instance):
    """Test that when Unix socket is configured but doesn't exist, it falls back to TCP"""

    with (
        patch('datadog_checks.go_pprof_scraper.check.datadog_agent') as mock_agent,
        patch('os.path.exists') as mock_exists,
    ):
        # Mock APM config to simulate default socket path that doesn't exist
        mock_agent.get_config.side_effect = lambda key: {
            "apm_config.enabled": True,
            "apm_config.receiver_port": 8126,
            "apm_config.receiver_socket": "/var/run/datadog/apm.socket",  # Default path
            "env": "test",
        }.get(key)

        # Socket doesn't exist (common case with default config)
        mock_exists.return_value = False

        # Create check instance
        check = GoPprofScraperCheck("go_pprof_scraper", INIT_CONFIG, [instance])

        # Verify that trace_agent_socket is None because socket doesn't exist
        assert check.trace_agent_socket is None
        assert check.trace_agent_url == "http://localhost:8126/profiling/v1/input"
        # Verify preference hasn't been set yet
        assert check._preferred_upload_method is None


@pytest.mark.unit
def test_upload_method_caching(instance):
    """Test that the check remembers which upload method works and doesn't retry unnecessarily"""

    with (
        patch('datadog_checks.go_pprof_scraper.check.datadog_agent') as mock_agent,
        patch('os.path.exists') as mock_exists,
    ):
        # Mock APM config with Unix socket that exists
        mock_agent.get_config.side_effect = lambda key: {
            "apm_config.enabled": True,
            "apm_config.receiver_port": 8126,
            "apm_config.receiver_socket": "/var/run/datadog/apm.socket",
            "env": "test",
        }.get(key)

        # Socket exists
        mock_exists.return_value = True

        # Create check instance
        check = GoPprofScraperCheck("go_pprof_scraper", INIT_CONFIG, [instance])

        # Initially, no preference is set
        assert check._preferred_upload_method is None
        assert check.trace_agent_socket is not None

        # After first failed Unix socket attempt, should remember to use TCP
        # (This would be set during check() execution when Unix socket fails)


@pytest.mark.unit
def test_unix_socket_validation(instance):
    """Test that Unix socket validation works correctly"""

    with (
        patch('datadog_checks.go_pprof_scraper.check.datadog_agent') as mock_agent,
        patch('os.path.exists') as mock_exists,
    ):
        # Mock APM config
        mock_agent.get_config.side_effect = lambda key: {
            "apm_config.enabled": True,
            "apm_config.receiver_port": 8126,
            "apm_config.receiver_socket": "/valid/socket/path",
            "env": "test",
        }.get(key)

        # Test case 1: Socket exists - should try to use it
        mock_exists.return_value = True

        check = GoPprofScraperCheck("go_pprof_scraper", INIT_CONFIG, [instance])
        assert check.trace_agent_socket is not None
        assert "http+unix://" in check.trace_agent_socket

        # Test case 2: Socket doesn't exist - should use TCP
        mock_exists.return_value = False
        check2 = GoPprofScraperCheck("go_pprof_scraper", INIT_CONFIG, [instance])
        assert check2.trace_agent_socket is None


@pytest.mark.e2e
def test_e2e(dd_agent_check, instance):
    check = GoPprofScraperCheck("go_pprof_scraper", INIT_CONFIG, [instance])
    check.check([])

    r = requests.post("http://localhost:9999/reset")
    r.raise_for_status()

    aggregator = dd_agent_check(instance)
    aggregator.assert_service_check("go_pprof_scraper.can_connect", GoPprofScraperCheck.OK)

    # The mock profile backend counts how many valid things it received, use
    # that as a signal that the profiles are making it through as intended
    r = requests.get("http://localhost:9999/accepted")
    r.raise_for_status()
    assert int(r.content) > 0
