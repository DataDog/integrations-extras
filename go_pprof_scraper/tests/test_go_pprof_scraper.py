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
def test_upload_tcp_fallback(dd_run_check, instance, aggregator):
    """Test that the check falls back to TCP if Unix socket fails"""
    from unittest.mock import MagicMock

    from requests.exceptions import ConnectionError

    with (
        patch('datadog_checks.go_pprof_scraper.check.datadog_agent') as mock_agent,
        patch('os.path.exists') as mock_exists,
        patch('requests_unixsocket.Session') as mock_session_class,
        patch('datadog_checks.base.utils.http.RequestsWrapper.get') as mock_http_get,
        patch('datadog_checks.base.utils.http.RequestsWrapper.post') as mock_http_post,
    ):
        # Mock APM config with Unix socket that exists
        apm_config = {
            "apm_config.enabled": True,
            "apm_config.receiver_port": 8126,
            "apm_config.receiver_socket": "/var/run/datadog/apm.socket",
            "env": "test",
        }
        mock_agent.get_config.side_effect = apm_config.get

        # Socket exists
        mock_exists.return_value = True

        # Mock the pprof HTTP GET responses (for fetching profiles)
        mock_pprof_response = MagicMock()
        mock_pprof_response.raw = MagicMock()
        mock_pprof_response.raise_for_status = MagicMock()
        mock_http_get.return_value = mock_pprof_response

        # Mock Unix socket POST to fail (simulating socket connection failure)
        mock_session = MagicMock()
        mock_session.post.side_effect = ConnectionError("Socket connection failed")
        mock_session_class.return_value = mock_session

        # Mock TCP POST to succeed (simulating successful fallback)
        mock_tcp_response = MagicMock()
        mock_tcp_response.raise_for_status = MagicMock()
        mock_http_post.return_value = mock_tcp_response

        # Create check instance
        check = GoPprofScraperCheck("go_pprof_scraper", INIT_CONFIG, [instance])

        # Initially, no preference is set
        assert check._preferred_upload_method is None
        assert check.trace_agent_socket is not None

        # Run the check - Unix socket should fail, TCP should succeed
        dd_run_check(check)

        # After check runs, preference should be cached as "tcp" because Unix socket failed
        assert check._preferred_upload_method == "tcp"
        aggregator.assert_service_check("go_pprof_scraper.can_connect", GoPprofScraperCheck.OK)


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
