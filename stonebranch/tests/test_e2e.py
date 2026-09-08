import pytest


@pytest.mark.e2e
def test_e2e(dd_agent_check):
    aggregator = dd_agent_check()

    # Service check — confirms the agent can reach the endpoint
    aggregator.assert_service_check("stonebranch.openmetrics.health", status=0)

    # Gauges from DEFAULT_METRICS — confirm the mapping and check are working end-to-end
    aggregator.assert_metric("stonebranch.uc_agent.status")
    aggregator.assert_metric("stonebranch.uc_build.info")
    aggregator.assert_metric("stonebranch.uc_task_instance.active")
    aggregator.assert_metric("stonebranch.uc_oms_server.status")
    aggregator.assert_metric("stonebranch.uc_database_connection_pool.allocated")
