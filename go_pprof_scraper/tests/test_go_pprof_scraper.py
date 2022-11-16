# (C) Datadog, Inc. 2022-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

from typing import Any, Callable, Dict

import pytest
import requests

from datadog_checks.base import AgentCheck, ConfigurationError
from datadog_checks.base.stubs.aggregator import AggregatorStub
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

    # Duration too long
    with pytest.raises(ConfigurationError):
        GoPprofScraperCheck(
            "go_pprof_scraper",
            INIT_CONFIG,
            [{"pprof_url": "http://localhost:1234/debug/pprof", "duration": 1000, "service": "testing"}],
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


@pytest.mark.e2e
def test_e2e(dd_agent_check, instance):
    check = GoPprofScraperCheck("go_pprof_scraper", INIT_CONFIG, [instance])
    check.check([])

    aggregator = dd_agent_check(instance)
    aggregator.assert_service_check("go_pprof_scraper.can_connect", GoPprofScraperCheck.OK)

    # The mock profile backend counts how many valid things it received, use
    # that as a signal that the profiles are making it through as intended
    r = requests.get("http://localhost:9999/accepted")
    r.raise_for_status()
    assert int(r.content) > 0
