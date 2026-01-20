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


def test_openmetrics_basic_auth_and_labels(aggregator, dd_run_check, mock_http_response):
    instance = {
        "openmetrics_endpoint": "http://test.local/metrics",
        "metrics": [
            "uc_agent_status",
            "uc_build_info",
            "uc_database_connection_pool_allocated",
        ],
        "auth_type": "basic",
        "username": "user1",
        "password": "pass1",
        "tags": ["environment:test"],
    }

    mock_http_response(
        status_code=200,
        content=PROM_TEXT,
        headers={"Content-Type": "text/plain; version=0.0.4"},
    )

    check = StonebranchCheck("stonebranch", {}, [instance])
    dd_run_check(check)

    # Show what was scraped/emitted (pytest will display this with `-s`)
    metric_names = sorted(aggregator.metric_names)
    print("\nEmitted metric names:")
    for name in metric_names:
        print(f"  - {name}")

    print("\nSeries count by metric:")
    for name in metric_names:
        print(f"  - {name}: {len(aggregator.metrics(name))}")

    endpoint_tag = f"endpoint:{instance['openmetrics_endpoint']}"
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

    aggregator.assert_all_metrics_covered()
