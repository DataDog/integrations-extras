import io

import requests

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
        "metrics": ["uc_agent_status", "uc_build_info", "uc_database_connection_pool_allocated"],
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
        "stonebranch.uc_agent_status",
        value=1.0,
        tags=base_tags + ["agent_id:AGNT0006"],
    )
    aggregator.assert_metric(
        "stonebranch.uc_agent_status",
        value=0.0,
        tags=base_tags + ["agent_id:AGNT0007"],
    )
    aggregator.assert_metric(
        "stonebranch.uc_build_info",
        value=1.0,
        tags=base_tags + ["build:build.108", "build_date:09-26-2025_0545", "release:7.9.0.0"],
    )
    aggregator.assert_metric(
        "stonebranch.uc_database_connection_pool_allocated",
        value=5.0,
        tags=base_tags + ["db_type:MySQL", "pool:Client"],
    )

    _, kwargs = mocked_request.call_args
    assert kwargs.get("auth") is not None

    aggregator.assert_all_metrics_covered()
