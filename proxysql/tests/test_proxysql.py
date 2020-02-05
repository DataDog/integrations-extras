import mock
import pymysql
import pytest

from datadog_checks.base import AgentCheck
from datadog_checks.errors import ConfigurationError
from datadog_checks.proxysql import ProxysqlCheck


@pytest.mark.unit
def test_wrong_config():
    check = ProxysqlCheck('proxysql', {}, {})

    # Empty instance
    with pytest.raises(ConfigurationError, match='ProxySQL host, port, user and password are needed'):
        check.check({})

    # Only host
    with pytest.raises(ConfigurationError, match='ProxySQL host, port, user and password are needed'):
        check.check({'server': 'localhost'})

    # Missing password
    with pytest.raises(ConfigurationError, match='ProxySQL host, port, user and password are needed'):
        check.check({'server': 'localhost', 'port': 6032, 'user': 'admin'})


@pytest.mark.unit
def test_config_ok():
    check = ProxysqlCheck('proxysql', {}, {})

    connection_mock = mock.Mock()
    connection_mock.__enter__ = mock.Mock()
    connection_mock.__exit__ = mock.Mock()
    check._connect = mock.Mock(return_value=connection_mock)
    check._collect_metrics = mock.Mock()

    check.check({'server': 'localhost', 'port': 6032, 'user': 'admin', 'pass': 'admin'})

    check._connect.assert_called_once_with('localhost', 6032, 'admin', 'admin', [], 10, None)
    check._collect_metrics.assert_called_once_with(connection_mock.__enter__(), [], {})


@pytest.mark.unit
def test_fetch_stats_no_result():
    check = ProxysqlCheck('proxysql', {}, {})

    cursor_mock = mock.Mock()
    cursor_mock.execute = mock.Mock()
    cursor_mock.rowcount = 0
    connection_mock = mock.Mock()
    connection_mock.cursor = mock.Mock(return_value=cursor_mock)

    check.warning = mock.Mock()
    stats = check._fetch_stats(connection_mock, 'query', 'test_stats')

    cursor_mock.execute.assert_called_once_with('query')
    check.warning.assert_called_once_with("Failed to fetch records from %s.", 'test_stats')

    assert len(stats) == 0


@pytest.mark.unit
def test_fetch_stats_exception():
    check = ProxysqlCheck('proxysql', {}, {})

    cursor_mock = mock.Mock()
    cursor_mock.execute = mock.Mock(side_effect=pymysql.err.InternalError('Internal Error'))
    cursor_mock.rowcount = 0
    connection_mock = mock.Mock()
    connection_mock.cursor = mock.Mock(return_value=cursor_mock)

    check.warning = mock.Mock()
    stats = check._fetch_stats(connection_mock, 'query', 'test_stats')

    cursor_mock.execute.assert_called_once_with('query')
    check.warning.assert_called_once_with("ProxySQL %s unavailable at this time: %s", 'test_stats', 'Internal Error')

    assert len(stats) == 0


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_service_check(aggregator, dd_environment):
    c = ProxysqlCheck('proxysql', {}, {})

    # the check should send OK
    c.check(dd_environment)
    aggregator.assert_service_check('proxysql.can_connect', AgentCheck.OK)

    # the check should send CRITICAL
    instance = dd_environment.copy()
    instance['port'] = 1111
    with pytest.raises(pymysql.OperationalError, match="Can't connect to MySQL server"):
        c.check(instance)

    aggregator.assert_service_check('proxysql.can_connect', AgentCheck.CRITICAL)

    all_metrics = (
        'proxysql.active_transactions',
        'proxysql.query_processor_time_nsec',
        'proxysql.questions',
        'proxysql.slow_queries',
        'proxysql.sqlite3_memory_bytes',
        'proxysql.client.connections_aborted',
        'proxysql.client.connections_connected',
        'proxysql.client.connections_created',
        'proxysql.client.connections_non_idle',
        'proxysql.server.connections_aborted',
        'proxysql.server.connections_connected',
        'proxysql.server.connections_created',
        'proxysql.backend.query_time_nsec',
        'proxysql.mysql.backend_buffers_bytes',
        'proxysql.mysql.frontend_buffers_bytes',
        'proxysql.mysql.session_internal_bytes',
        'proxysql.mysql.thread_workers',
        'proxysql.mysql.monitor_workers',
        'proxysql.pool.conn_success',
        'proxysql.pool.conn_failure',
        'proxysql.pool.conn_immediate',
        'proxysql.pool.memory_bytes',
        'proxysql.client.statements.active_total',
        'proxysql.client.statements.active_unique',
        'proxysql.server.statements.active_total',
        'proxysql.server.statements.active_unique',
        'proxysql.statements.cached',
        'proxysql.query_cache.entries',
        'proxysql.query_cache.memory_bytes',
        'proxysql.query_cache.purged',
        'proxysql.query_cache.bytes_in',
        'proxysql.query_cache.bytes_out',
        'proxysql.query_cache.get.count',
        'proxysql.query_cache.get_ok.count',
        'proxysql.query_cache.set.count',
        'proxysql.performance.command.total_time_ms',
        'proxysql.performance.command.total_count',
        'proxysql.performance.command.cnt_100us',
        'proxysql.performance.command.cnt_500us',
        'proxysql.performance.command.cnt_1ms',
        'proxysql.performance.command.cnt_5ms',
        'proxysql.performance.command.cnt_10ms',
        'proxysql.performance.command.cnt_50ms',
        'proxysql.performance.command.cnt_100ms',
        'proxysql.performance.command.cnt_500ms',
        'proxysql.performance.command.cnt_1s',
        'proxysql.performance.command.cnt_5s',
        'proxysql.performance.command.cnt_10s',
        'proxysql.performance.command.cnt_INFs',
        'proxysql.pool.connections_used',
        'proxysql.pool.connections_free',
        'proxysql.pool.connections_ok',
        'proxysql.pool.connections_error',
        'proxysql.pool.queries',
        'proxysql.pool.bytes_data_sent',
        'proxysql.pool.bytes_data_recv',
        'proxysql.pool.latency_ms',
        'proxysql.memory.sqlite3_memory',
        'proxysql.memory.jemalloc_resident',
        'proxysql.memory.jemalloc_active',
        'proxysql.memory.jemalloc_allocated',
        'proxysql.memory.jemalloc_mapped',
        'proxysql.memory.jemalloc_metadata',
        'proxysql.memory.jemalloc_retained',
        'proxysql.memory.auth_memory',
        'proxysql.memory.query_digest_memory',
        'proxysql.memory.stack_memory_mysql_threads',
        'proxysql.memory.stack_memory_admin_threads',
        'proxysql.memory.stack_memory_cluster_threads',
        'proxysql.frontend.user_connections',
        'proxysql.frontend.user_max_connections',
        'proxysql.query_rules.rule_hits',
    )

    for metric in all_metrics:
        aggregator.assert_metric(metric, at_least=0)

    aggregator.assert_all_metrics_covered()


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_not_optional_metrics(aggregator, dd_environment):
    c = ProxysqlCheck('proxysql', {}, {})

    instance = dd_environment.copy()
    instance['options'] = {
        'extra_command_counters_metrics': False,
        'extra_connection_pool_metrics': False,
        'extra_user_metrics': False,
        'extra_memory_metrics': False,
        'extra_query_rules_metrics': False,
    }

    c.check(instance)

    global_metrics = (
        'proxysql.active_transactions',
        'proxysql.query_processor_time_nsec',
        'proxysql.questions',
        'proxysql.slow_queries',
        'proxysql.sqlite3_memory_bytes',
        'proxysql.client.connections_aborted',
        'proxysql.client.connections_connected',
        'proxysql.client.connections_created',
        'proxysql.client.connections_non_idle',
        'proxysql.server.connections_aborted',
        'proxysql.server.connections_connected',
        'proxysql.server.connections_created',
        'proxysql.backend.query_time_nsec',
        'proxysql.mysql.backend_buffers_bytes',
        'proxysql.mysql.frontend_buffers_bytes',
        'proxysql.mysql.session_internal_bytes',
        'proxysql.mysql.thread_workers',
        'proxysql.mysql.monitor_workers',
        'proxysql.pool.conn_success',
        'proxysql.pool.conn_failure',
        'proxysql.pool.conn_immediate',
        'proxysql.pool.memory_bytes',
        'proxysql.client.statements.active_total',
        'proxysql.client.statements.active_unique',
        'proxysql.server.statements.active_total',
        'proxysql.server.statements.active_unique',
        'proxysql.statements.cached',
        'proxysql.query_cache.entries',
        'proxysql.query_cache.memory_bytes',
        'proxysql.query_cache.purged',
        'proxysql.query_cache.bytes_in',
        'proxysql.query_cache.bytes_out',
        'proxysql.query_cache.get.count',
        'proxysql.query_cache.get_ok.count',
        'proxysql.query_cache.set.count',
    )

    for metric in global_metrics:
        aggregator.assert_metric(metric, at_least=0)

    aggregator.assert_all_metrics_covered()


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_metrics_tags(aggregator, dd_environment):
    c = ProxysqlCheck('proxysql', {}, {})

    c.check(dd_environment)
    aggregator.assert_service_check('proxysql.can_connect', AgentCheck.OK)

    simple_tag_metrics = (
        'proxysql.active_transactions',
        'proxysql.query_processor_time_nsec',
        'proxysql.questions',
        'proxysql.slow_queries',
        'proxysql.sqlite3_memory_bytes',
        'proxysql.client.connections_aborted',
        'proxysql.client.connections_connected',
        'proxysql.client.connections_created',
        'proxysql.client.connections_non_idle',
        'proxysql.server.connections_aborted',
        'proxysql.server.connections_connected',
        'proxysql.server.connections_created',
        'proxysql.backend.query_time_nsec',
        'proxysql.mysql.backend_buffers_bytes',
        'proxysql.mysql.frontend_buffers_bytes',
        'proxysql.mysql.session_internal_bytes',
        'proxysql.mysql.thread_workers',
        'proxysql.mysql.monitor_workers',
        'proxysql.pool.conn_success',
        'proxysql.pool.conn_failure',
        'proxysql.pool.conn_immediate',
        'proxysql.pool.memory_bytes',
        'proxysql.client.statements.active_total',
        'proxysql.client.statements.active_unique',
        'proxysql.server.statements.active_total',
        'proxysql.server.statements.active_unique',
        'proxysql.statements.cached',
        'proxysql.query_cache.entries',
        'proxysql.query_cache.memory_bytes',
        'proxysql.query_cache.purged',
        'proxysql.query_cache.bytes_in',
        'proxysql.query_cache.bytes_out',
        'proxysql.query_cache.get.count',
        'proxysql.query_cache.get_ok.count',
        'proxysql.query_cache.set.count',
        'proxysql.memory.sqlite3_memory',
        'proxysql.memory.jemalloc_resident',
        'proxysql.memory.jemalloc_active',
        'proxysql.memory.jemalloc_allocated',
        'proxysql.memory.jemalloc_mapped',
        'proxysql.memory.jemalloc_metadata',
        'proxysql.memory.jemalloc_retained',
        'proxysql.memory.auth_memory',
        'proxysql.memory.query_digest_memory',
        'proxysql.memory.stack_memory_mysql_threads',
        'proxysql.memory.stack_memory_admin_threads',
        'proxysql.memory.stack_memory_cluster_threads',
    )

    command_tags_metrics = (
        'proxysql.performance.command.total_time_ms',
        'proxysql.performance.command.total_count',
        'proxysql.performance.command.cnt_100us',
        'proxysql.performance.command.cnt_500us',
        'proxysql.performance.command.cnt_1ms',
        'proxysql.performance.command.cnt_5ms',
        'proxysql.performance.command.cnt_10ms',
        'proxysql.performance.command.cnt_50ms',
        'proxysql.performance.command.cnt_100ms',
        'proxysql.performance.command.cnt_500ms',
        'proxysql.performance.command.cnt_1s',
        'proxysql.performance.command.cnt_5s',
        'proxysql.performance.command.cnt_10s',
        'proxysql.performance.command.cnt_INFs',
    )

    pool_tags_metrics = (
        'proxysql.pool.connections_used',
        'proxysql.pool.connections_free',
        'proxysql.pool.connections_ok',
        'proxysql.pool.connections_error',
        'proxysql.pool.queries',
        'proxysql.pool.bytes_data_sent',
        'proxysql.pool.bytes_data_recv',
        'proxysql.pool.latency_ms',
    )

    user_tags_metrics = (
        'proxysql.frontend.user_connections',
        'proxysql.frontend.user_max_connections',
    )

    query_rules_tags_metrics = ('proxysql.query_rules.rule_hits',)

    for metric in simple_tag_metrics:
        aggregator.assert_metric_has_tag(metric, 'application:test', count=1)

    for metric in command_tags_metrics:
        aggregator.assert_metric_has_tag(metric, 'application:test')
        aggregator.assert_metric_has_tag_prefix(metric, 'proxysql_command')

    for metric in pool_tags_metrics:
        aggregator.assert_metric_has_tag(metric, 'application:test')
        aggregator.assert_metric_has_tag_prefix(metric, 'proxysql_db_node')

    for metric in user_tags_metrics:
        aggregator.assert_metric_has_tag(metric, 'application:test')
        aggregator.assert_metric_has_tag_prefix(metric, 'proxysql_mysql_user')

    for metric in query_rules_tags_metrics:
        aggregator.assert_metric_has_tag(metric, 'application:test')
        aggregator.assert_metric_has_tag_prefix(metric, 'proxysql_query_rule_id')

    aggregator.assert_all_metrics_covered()
