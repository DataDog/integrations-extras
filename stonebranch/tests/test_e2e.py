import pytest


@pytest.mark.e2e
def test_e2e(dd_agent_check):
    aggregator = dd_agent_check()

    # UC core gauges
    aggregator.assert_metric("stonebranch.uc_agent.status")
    aggregator.assert_metric("stonebranch.uc_build.info")
    aggregator.assert_metric("stonebranch.uc_task_instance.active")

    # UC counters (OpenMetrics V2 appends .count to counter families)
    aggregator.assert_metric("stonebranch.uc_history.total.count")
    aggregator.assert_metric("stonebranch.uc_task_instance.launch.total.count")
    aggregator.assert_metric("stonebranch.uc_task_instance.late_finish.total.count")
    aggregator.assert_metric("stonebranch.uc_task_instance.early_finish.total.count")
    aggregator.assert_metric("stonebranch.uc_universal_event.total.count")

    # OMS server status
    aggregator.assert_metric("stonebranch.uc_oms_server.status")
    aggregator.assert_metric("stonebranch.uc_oms_server.session_status")

    # License metrics
    aggregator.assert_metric("stonebranch.uc_license.agents_distributed_max")
    aggregator.assert_metric("stonebranch.uc_license.agents_distributed_used")
    aggregator.assert_metric("stonebranch.uc_license.monthly_executions_max")
    aggregator.assert_metric("stonebranch.uc_license.monthly_executions_used")

    # Database connection pool
    aggregator.assert_metric("stonebranch.uc_database_connection_pool.allocated")

    # JVM metrics
    aggregator.assert_metric("stonebranch.jvm_threads_current")
    aggregator.assert_metric("stonebranch.jvm_memory_used_bytes")
    aggregator.assert_metric("stonebranch.jvm_classes_loaded_total.count")
    aggregator.assert_metric("stonebranch.process_cpu_seconds_total.count")

    # Service check
    aggregator.assert_service_check("stonebranch.openmetrics.health", status=0)
