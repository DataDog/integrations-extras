import pytest

from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.upbound_uxp import UpboundUxpCheck


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_service_check(aggregator, instance):
    c = UpboundUxpCheck('uxp.can_connect', {}, [instance])

    c.check(instance)
    aggregator.assert_service_check('uxp.can_connect', UpboundUxpCheck.OK)


@pytest.mark.unit
@pytest.mark.usefixtures('dd_environment')
def test_check_min(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    instance = {"uxp_url": "/metrics", "uxp_port": "8080", "verbose": True}
    check = UpboundUxpCheck('upbound_uxp', {}, [instance])
    dd_run_check(check)

    aggregator.assert_metric('uxp.controller_runtime_reconcile_total')
    aggregator.assert_metric('uxp.datadog_agent_checks')
    aggregator.assert_metric('uxp.go_goroutines')
    aggregator.assert_metric('uxp.go_memstats_alloc_bytes')
    aggregator.assert_metric('uxp.go_memstats_alloc_bytes_total')
    aggregator.assert_metric('uxp.process_cpu_seconds_total')
    aggregator.assert_metric('uxp.process_resident_memory_bytes')
    aggregator.assert_metric('uxp.process_start_time_seconds')
    aggregator.assert_metric('uxp.rest_client_requests_total')
    aggregator.assert_metric('uxp.upjet_terraform_active_cli_invocations')
    aggregator.assert_metric('uxp.upjet_terraform_running_processes')
    aggregator.assert_metric('uxp.workqueue_adds_total')
    aggregator.assert_metric('uxp.workqueue_depth')
    aggregator.assert_metric('uxp.workqueue_work_duration_seconds_bucket')
    aggregator.assert_metric('uxp.workqueue_work_duration_seconds_count')
    aggregator.assert_metric('uxp.workqueue_work_duration_seconds_sum')
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


@pytest.mark.unit
@pytest.mark.usefixtures('dd_environment')
def test_check_more(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    instance = {"uxp_url": "/metrics", "uxp_port": "8080", "metrics_default": "more", "verbose": True}
    check = UpboundUxpCheck('uxp.upbound_uxp', {}, [instance])
    dd_run_check(check)

    aggregator.assert_metric('uxp.certwatcher_read_certificate_errors_total')  # count
    aggregator.assert_metric('uxp.certwatcher_read_certificate_total')  # count
    aggregator.assert_metric('uxp.controller_runtime_active_workers')  # gauge
    aggregator.assert_metric('uxp.controller_runtime_max_concurrent_reconciles')  # gauge
    aggregator.assert_metric('uxp.controller_runtime_reconcile_errors_total')  # count
    aggregator.assert_metric('uxp.controller_runtime_reconcile_time_seconds_bucket')  # histogram
    aggregator.assert_metric('uxp.controller_runtime_reconcile_time_seconds_count')  # count
    aggregator.assert_metric('uxp.controller_runtime_reconcile_time_seconds_sum')  # count
    aggregator.assert_metric('uxp.controller_runtime_reconcile_total')  # count
    aggregator.assert_metric('uxp.datadog_agent_checks')  # count
    aggregator.assert_metric('uxp.go_goroutines')  # gauge
    aggregator.assert_metric('uxp.go_memstats_alloc_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_alloc_bytes_total')  # count
    aggregator.assert_metric('uxp.go_memstats_buck_hash_sys_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_frees_total')  # count
    aggregator.assert_metric('uxp.go_memstats_gc_sys_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_heap_alloc_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_heap_idle_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_heap_inuse_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_heap_objects')  # gauge
    aggregator.assert_metric('uxp.go_memstats_heap_released_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_mcache_inuse_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_mspan_inuse_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_mspan_sys_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_next_gc_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_next_gc_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_other_sys_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_stack_inuse_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_stack_sys_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_sys_bytes')  # gauge
    aggregator.assert_metric('uxp.go_threads')  # gauge
    aggregator.assert_metric('uxp.leader_election_master_status')  # gauge
    aggregator.assert_metric('uxp.process_cpu_seconds_total')  # count
    aggregator.assert_metric('uxp.process_max_fds')  # gauge
    aggregator.assert_metric('uxp.process_resident_memory_bytes')  # gauge
    aggregator.assert_metric('uxp.process_start_time_seconds')  # gauge
    aggregator.assert_metric('uxp.process_virtual_memory_max_bytes')  # gauge
    aggregator.assert_metric('uxp.rest_client_requests_total')  # count
    aggregator.assert_metric('uxp.upjet_terraform_active_cli_invocations')  # gauge
    aggregator.assert_metric('uxp.upjet_terraform_running_processes')  # gauge
    aggregator.assert_metric('uxp.workqueue_adds_total')  # count
    aggregator.assert_metric('uxp.workqueue_depth')  # gauge
    aggregator.assert_metric('uxp.workqueue_work_duration_seconds_bucket')  # histogram
    aggregator.assert_metric('uxp.workqueue_work_duration_seconds_count')  # count
    aggregator.assert_metric('uxp.workqueue_work_duration_seconds_sum')  # count


@pytest.mark.unit
@pytest.mark.usefixtures('dd_environment')
def test_emits_ok_service_check_when_service_is_up(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    instance = {"uxp_url": "/metrics", "uxp_port": "8080", "metrics_default": "max", "verbose": True}
    check = UpboundUxpCheck('uxp.upbound_uxp', {}, [instance])
    dd_run_check(check)
    aggregator.assert_metric('uxp.certwatcher_read_certificate_errors_total')  # count
    aggregator.assert_metric('uxp.certwatcher_read_certificate_total')  # count
    aggregator.assert_metric('uxp.controller_runtime_active_workers')  # gauge
    aggregator.assert_metric('uxp.controller_runtime_max_concurrent_reconciles')  # gauge
    aggregator.assert_metric('uxp.controller_runtime_reconcile_errors_total')  # count
    aggregator.assert_metric('uxp.controller_runtime_reconcile_time_seconds_bucket')  # histogram
    aggregator.assert_metric('uxp.controller_runtime_reconcile_time_seconds_count')  # count
    aggregator.assert_metric('uxp.controller_runtime_reconcile_time_seconds_sum')  # count
    aggregator.assert_metric('uxp.controller_runtime_reconcile_total')  # count
    aggregator.assert_metric('uxp.controller_runtime_webhook_requests_in_flight')
    aggregator.assert_metric('uxp.controller_runtime_webhook_requests_total')
    aggregator.assert_metric('uxp.datadog_agent_checks')  # count
    aggregator.assert_metric('uxp.go_goroutines')  # gauge
    aggregator.assert_metric('uxp.go_memstats_alloc_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_alloc_bytes_total')  # count
    aggregator.assert_metric('uxp.go_memstats_buck_hash_sys_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_frees_total')  # count
    aggregator.assert_metric('uxp.go_memstats_gc_sys_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_heap_alloc_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_heap_idle_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_heap_inuse_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_heap_objects')  # gauge
    aggregator.assert_metric('uxp.go_memstats_heap_released_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_mcache_inuse_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_mspan_inuse_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_mspan_sys_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_next_gc_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_next_gc_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_other_sys_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_stack_inuse_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_stack_sys_bytes')  # gauge
    aggregator.assert_metric('uxp.go_memstats_sys_bytes')  # gauge
    aggregator.assert_metric('uxp.go_threads')  # gauge
    aggregator.assert_metric('uxp.leader_election_master_status')  # gauge
    aggregator.assert_metric('uxp.process_cpu_seconds_total')  # count
    aggregator.assert_metric('uxp.process_max_fds')  # gauge
    aggregator.assert_metric('uxp.process_resident_memory_bytes')  # gauge
    aggregator.assert_metric('uxp.process_start_time_seconds')  # gauge
    aggregator.assert_metric('uxp.process_virtual_memory_max_bytes')  # gauge
    aggregator.assert_metric('uxp.rest_client_requests_total')  # count
    aggregator.assert_metric('uxp.upjet_terraform_active_cli_invocations')  # gauge
    aggregator.assert_metric('uxp.upjet_terraform_running_processes')  # gauge
    aggregator.assert_metric('uxp.workqueue_adds_total')  # count
    aggregator.assert_metric('uxp.workqueue_depth')  # gauge
    aggregator.assert_metric('uxp.workqueue_work_duration_seconds_bucket')  # histogram
    aggregator.assert_metric('uxp.workqueue_work_duration_seconds_count')  # count
    aggregator.assert_metric('uxp.go_gc_duration_seconds')
    aggregator.assert_metric('uxp.go_gc_duration_seconds_count')
    aggregator.assert_metric('uxp.go_gc_duration_seconds_sum')
    aggregator.assert_metric('uxp.go_info')
    aggregator.assert_metric('uxp.go_memstats_heap_sys_bytes')
    aggregator.assert_metric('uxp.go_memstats_last_gc_time_seconds')
    aggregator.assert_metric('uxp.go_memstats_mcache_sys_bytes')
    aggregator.assert_metric('uxp.process_open_fds')
    aggregator.assert_metric('uxp.process_virtual_memory_bytes')
    aggregator.assert_metric('uxp.workqueue_longest_running_processor_seconds')
    aggregator.assert_metric('uxp.workqueue_queue_duration_seconds_bucket')
    aggregator.assert_metric('uxp.workqueue_queue_duration_seconds_count')
    aggregator.assert_metric('uxp.workqueue_queue_duration_seconds_sum')
    aggregator.assert_metric('uxp.workqueue_retries_total')
    aggregator.assert_metric('uxp.workqueue_unfinished_work_seconds')
    aggregator.assert_metric('uxp.workqueue_work_duration_seconds_sum')
    aggregator.assert_metric('uxp.go_memstats_lookups_total')
    aggregator.assert_metric('uxp.go_memstats_mallocs_total')
    aggregator.assert_metric('uxp.rest_client_request_duration_seconds_bucket')
    aggregator.assert_metric('uxp.rest_client_request_duration_seconds_count')
    aggregator.assert_metric('uxp.rest_client_request_duration_seconds_sum')
    aggregator.assert_metric('uxp.rest_client_request_size_bytes_bucket')
    aggregator.assert_metric('uxp.rest_client_request_size_bytes_count')
    aggregator.assert_metric('uxp.rest_client_request_size_bytes_sum')
    aggregator.assert_metric('uxp.rest_client_response_size_bytes_bucket')
    aggregator.assert_metric('uxp.rest_client_response_size_bytes_count')
    aggregator.assert_metric('uxp.rest_client_response_size_bytes_sum')
    # aggregator.assert_metric('uxp.upjet_resource_ttr_bucket')
    # aggregator.assert_metric('uxp.upjet_resource_ttr_count')
    # aggregator.assert_metric('uxp.upjet_resource_ttr_sum')
    # aggregator.assert_metric('uxp.upjet_terraform_cli_duration_bucket')
    # aggregator.assert_metric('uxp.upjet_terraform_cli_duration_count')
    # aggregator.assert_metric('uxp.upjet_terraform_cli_duration_sum')
    aggregator.assert_all_metrics_covered()
    aggregator.assert_service_check('uxp.can_connect', UpboundUxpCheck.OK)


@pytest.mark.unit
@pytest.mark.usefixtures('dd_environment')
def test_emits_critical_service_check_when_service_is_down(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    instance = {
        "uxp_url": "/metrics",
        "uxp_port": "999",  # Purposefully configuring wrong port to simulate error
    }
    check = UpboundUxpCheck('uxp.can_connect', {}, [instance])
    dd_run_check(check)
    aggregator.assert_metric('uxp.datadog_agent_checks')  # count
    aggregator.assert_service_check('uxp.can_connect', UpboundUxpCheck.CRITICAL)
    aggregator.assert_all_metrics_covered()
