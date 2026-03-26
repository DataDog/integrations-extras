from typing import Any, Callable, Dict  # noqa: F401

import pytest

from datadog_checks.base import AgentCheck  # noqa: F401
from datadog_checks.base.stubs.aggregator import AggregatorStub  # noqa: F401
from datadog_checks.chrony import ChronyCheck

SAMPLE_OUTPUT = """Reference ID    : 89BE0204 (time1.weber.edu)
Stratum         : 2
Ref time (UTC)  : Wed Jan 28 06:55:34 2026
System time     : 0.143763348 seconds slow of NTP time
Last offset     : -0.000308179 seconds
RMS offset      : 0.007722483 seconds
Frequency       : 9.733 ppm slow
Residual freq   : +0.086 ppm
Skew            : 19.531 ppm
Root delay      : 0.118516006 seconds
Root dispersion : 0.004484985 seconds
Update interval : 64.7 seconds
Leap status     : Normal
"""

EXPECTED_METRICS = {
    "stratum": 2.0,
    "systime": -0.143763348,
    "frequency": -9.733,
    "residualfreq": 0.086,
    "skew": 19.531,
    "rootdelay": 0.118516006,
    "rootdispersion": 0.004484985,
}

EXPECTED_TAGS = [
    "region:local",
    "reference_ip:89BE0204",
    "reference_server:time1.weber.edu",
]


@pytest.mark.unit
def test_parse_output_and_reference_info():
    check = ChronyCheck("chrony", {}, [{}])

    metrics = check._parse_chrony_output(SAMPLE_OUTPUT)
    reference_info = check._get_reference_info(SAMPLE_OUTPUT)

    assert metrics == EXPECTED_METRICS
    assert reference_info == {
        "reference_ip": "89BE0204",
        "reference_server": "time1.weber.edu",
    }


@pytest.mark.integration
@pytest.mark.usefixtures("dd_environment")
def test_emits_metrics_and_service_check(aggregator, instance, monkeypatch):
    check = ChronyCheck("chrony", {}, [instance])

    monkeypatch.setattr(check, "_get_chrony_tracking", lambda: SAMPLE_OUTPUT)

    check.check(instance)

    for metric_name, value in EXPECTED_METRICS.items():
        aggregator.assert_metric(f"chrony.{metric_name}", value=value, tags=EXPECTED_TAGS)

    aggregator.assert_service_check("chrony.can_connect", status=ChronyCheck.OK, tags=EXPECTED_TAGS)
    aggregator.assert_all_metrics_covered()
