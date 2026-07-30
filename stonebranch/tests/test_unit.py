import io

import pytest
import requests

from datadog_checks.base import AgentCheck
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.stonebranch import StonebranchCheck

PROM_TEXT = """\
# HELP uc_agent_status Agent status. (0=Offline, 1=Active, -1=Unknown)
# TYPE uc_agent_status gauge
uc_agent_status{agent_id="AGNT0006"} 1.0
uc_agent_status{agent_id="AGNT0007"} 0.0

# HELP uc_build_info Universal Controller build information.
# TYPE uc_build_info gauge
uc_build_info{build="build.108",build_date="09-26-2025_0545",release="7.9.0.0"} 1

# HELP uc_database_connection_pool_allocated Number of connections currently allocated by a given pool.
# TYPE uc_database_connection_pool_allocated gauge
uc_database_connection_pool_allocated{db_type="MySQL",pool="Client"} 5.0
"""

PROM_TEXT_JVM = """\
# HELP jvm_threads_current Current thread count of a JVM
# TYPE jvm_threads_current gauge
jvm_threads_current 42.0

# HELP jvm_threads_peak Peak thread count of a JVM
# TYPE jvm_threads_peak gauge
jvm_threads_peak 60.0

# HELP jvm_memory_used_bytes Used bytes of a given JVM memory area.
# TYPE jvm_memory_used_bytes gauge
jvm_memory_used_bytes{area="heap"} 123456789.0

# HELP jvm_memory_committed_bytes Committed (bytes) of a given JVM memory area.
# TYPE jvm_memory_committed_bytes gauge
jvm_memory_committed_bytes{area="heap"} 256000000.0

# HELP jvm_gc_collection_seconds Time spent in a given JVM garbage collector in seconds.
# TYPE jvm_gc_collection_seconds gauge
jvm_gc_collection_seconds{gc="G1 Young Generation"} 0.123
"""


def make_streaming_response(url: str, text: str) -> requests.Response:
    r = requests.Response()
    r.status_code = 200
    r.url = url
    r.headers["Content-Type"] = "text/plain; version=0.0.4; charset=utf-8"
    r.encoding = "utf-8"

    r.raw = io.BytesIO(text.encode("utf-8"))

    r.request = requests.Request("GET", url).prepare()
    return r


def test_openmetrics_basic_auth_and_labels(aggregator, dd_run_check, mocker):
    url = "http://test.local/metrics"
    instance = {
        "openmetrics_endpoint": url,
        "metrics": [
            {"uc_agent_status": "uc_agent.status"},
            {"uc_build_info": "uc_build.info"},
            {"uc_database_connection_pool_allocated": "uc_database_connection_pool.allocated"},
        ],
        "auth_type": "basic",
        "username": "user1",
        "password": "pass1",
        "tags": ["environment:test"],
    }

    mocked_request = mocker.patch(
        "requests.sessions.Session.request",
        autospec=True,
        return_value=make_streaming_response(url, PROM_TEXT),
    )

    check = StonebranchCheck("stonebranch", {}, [instance])
    dd_run_check(check)

    endpoint_tag = f"endpoint:{url}"
    base_tags = ["environment:test", endpoint_tag]

    aggregator.assert_metric(
        "stonebranch.uc_agent.status",
        value=1.0,
        tags=base_tags + ["agent_id:AGNT0006"],
    )
    aggregator.assert_metric(
        "stonebranch.uc_agent.status",
        value=0.0,
        tags=base_tags + ["agent_id:AGNT0007"],
    )
    aggregator.assert_metric(
        "stonebranch.uc_build.info",
        value=1.0,
        tags=base_tags + ["build:build.108", "build_date:09-26-2025_0545", "release:7.9.0.0"],
    )
    aggregator.assert_metric(
        "stonebranch.uc_database_connection_pool.allocated",
        value=5.0,
        tags=base_tags + ["db_type:MySQL", "pool:Client"],
    )

    _, kwargs = mocked_request.call_args
    assert kwargs.get("auth") is not None

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_metric_groups_jvm(aggregator, dd_run_check, mocker):
    url = "http://test.local/metrics"
    instance = {
        "openmetrics_endpoint": url,
        "metric_groups": ["jvm"],
        "tags": ["environment:test"],
    }

    mocker.patch(
        "requests.sessions.Session.request",
        autospec=True,
        return_value=make_streaming_response(url, PROM_TEXT_JVM),
    )

    check = StonebranchCheck("stonebranch", {}, [instance])
    dd_run_check(check)

    endpoint_tag = f"endpoint:{url}"
    base_tags = ["environment:test", endpoint_tag]

    aggregator.assert_metric("stonebranch.jvm_threads_current", value=42.0, tags=base_tags)
    aggregator.assert_metric("stonebranch.jvm_threads_peak", value=60.0, tags=base_tags)
    aggregator.assert_metric(
        "stonebranch.jvm_memory_used_bytes",
        value=123456789.0,
        tags=base_tags + ["area:heap"],
    )
    aggregator.assert_metric(
        "stonebranch.jvm_memory_committed_bytes",
        value=256000000.0,
        tags=base_tags + ["area:heap"],
    )
    aggregator.assert_metric(
        "stonebranch.jvm_gc_collection_seconds",
        tags=base_tags + ["gc:G1 Young Generation"],
    )


def test_can_connect_ok(aggregator, dd_run_check, mocker):
    url = "http://test.local/metrics"
    instance = {
        "openmetrics_endpoint": url,
        "metrics": [{"uc_build_info": "uc_build.info"}],
    }

    mocker.patch(
        "requests.sessions.Session.request",
        autospec=True,
        return_value=make_streaming_response(
            url, "# HELP uc_build_info info\n# TYPE uc_build_info gauge\nuc_build_info{release=\"7.9\"} 1\n"
        ),
    )

    check = StonebranchCheck("stonebranch", {}, [instance])
    dd_run_check(check)

    aggregator.assert_service_check(
        "stonebranch.openmetrics.health",
        status=AgentCheck.OK,
        tags=[f"endpoint:{url}"],
    )


def test_can_connect_critical(aggregator, dd_run_check, mocker):
    url = "http://unreachable.local/metrics"
    instance = {
        "openmetrics_endpoint": url,
        "metrics": [{"uc_build_info": "uc_build.info"}],
    }

    mocker.patch(
        "requests.sessions.Session.request",
        autospec=True,
        side_effect=requests.exceptions.ConnectionError("Connection refused"),
    )

    check = StonebranchCheck("stonebranch", {}, [instance])
    with pytest.raises(Exception):
        dd_run_check(check)

    aggregator.assert_service_check(
        "stonebranch.openmetrics.health",
        status=AgentCheck.CRITICAL,
        tags=[f"endpoint:{url}"],
    )
