from collections import defaultdict
from contextlib import closing, contextmanager

import pymysql
import pymysql.cursors

from datadog_checks.base import AgentCheck
from datadog_checks.errors import ConfigurationError

GAUGE = "gauge"
RATE = "rate"
COUNT = "count"
MONOTONIC = "monotonic_count"

STATS_MYSQL_GLOBAL = {
    "Active_Transactions": ("proxysql.active_transactions", GAUGE),
    "Query_Processor_time_nsec": ("proxysql.query_processor_time_nsec", RATE),
    "Questions": ("proxysql.questions", RATE),
    "Slow_queries": ("proxysql.slow_queries", RATE),
    "SQLite3_memory_bytes": ("proxysql.sqlite3_memory_bytes", GAUGE),
    "Client_Connections_aborted": ("proxysql.client.connections_aborted", RATE),
    "Client_Connections_connected": ("proxysql.client.connections_connected", GAUGE),
    "Client_Connections_created": ("proxysql.client.connections_created", RATE),
    "Client_Connections_non_idle": ("proxysql.client.connections_non_idle", GAUGE),
    "Server_Connections_aborted": ("proxysql.server.connections_aborted", RATE),
    "Server_Connections_connected": ("proxysql.server.connections_connected", GAUGE),
    "Server_Connections_created": ("proxysql.server.connections_created", RATE),
    "Backend_query_time_nsec": ("proxysql.backend.query_time_nsec", RATE),
    "mysql_backend_buffers_bytes": ("proxysql.mysql.backend_buffers_bytes", GAUGE),
    "mysql_frontend_buffers_bytes": ("proxysql.mysql.frontend_buffers_bytes", GAUGE),
    "mysql_session_internal_bytes": ("proxysql.mysql.session_internal_bytes", GAUGE),
    "MySQL_Thread_Workers": ("proxysql.mysql.thread_workers", GAUGE),
    "MySQL_Monitor_Workers": ("proxysql.mysql.monitor_workers", GAUGE),
    "ConnPool_get_conn_success": ("proxysql.pool.conn_success", RATE),
    "ConnPool_get_conn_failure": ("proxysql.pool.conn_failure", RATE),
    "ConnPool_get_conn_immediate": ("proxysql.pool.conn_immediate", RATE),
    "ConnPool_memory_bytes": ("proxysql.pool.memory_bytes", GAUGE),
    "Stmt_Client_Active_Total": ("proxysql.client.statements.active_total", GAUGE),
    "Stmt_Client_Active_Unique": ("proxysql.client.statements.active_unique", GAUGE),
    "Stmt_Server_Active_Total": ("proxysql.server.statements.active_total", GAUGE),
    "Stmt_Server_Active_Unique": ("proxysql.server.statements.active_unique", GAUGE),
    "Stmt_Cached": ("proxysql.statements.cached", GAUGE),
    "Query_Cache_Entries": ("proxysql.query_cache.entries", GAUGE),
    "Query_Cache_Memory_bytes": ("proxysql.query_cache.memory_bytes", GAUGE),
    "Query_Cache_Purged": ("proxysql.query_cache.purged", RATE),
    "Query_Cache_bytes_IN": ("proxysql.query_cache.bytes_in", GAUGE),
    "Query_Cache_bytes_OUT": ("proxysql.query_cache.bytes_out", GAUGE),
    "Query_Cache_count_GET": ("proxysql.query_cache.get.count", GAUGE),
    "Query_Cache_count_GET_OK": ("proxysql.query_cache.get_ok.count", GAUGE),
    "Query_Cache_count_SET": ("proxysql.query_cache.set.count", GAUGE),
}

STATS_COMMAND_COUNTERS = {
    "Total_Time_ms": ("proxysql.performance.command.total_time_ms", RATE),
    "Total_cnt": ("proxysql.performance.command.total_count", MONOTONIC),
    "cnt_100us": ("proxysql.performance.command.cnt_100us", MONOTONIC),
    "cnt_500us": ("proxysql.performance.command.cnt_500us", MONOTONIC),
    "cnt_1ms": ("proxysql.performance.command.cnt_1ms", MONOTONIC),
    "cnt_5ms": ("proxysql.performance.command.cnt_5ms", MONOTONIC),
    "cnt_10ms": ("proxysql.performance.command.cnt_10ms", MONOTONIC),
    "cnt_50ms": ("proxysql.performance.command.cnt_50ms", MONOTONIC),
    "cnt_100ms": ("proxysql.performance.command.cnt_100ms", MONOTONIC),
    "cnt_500ms": ("proxysql.performance.command.cnt_500ms", MONOTONIC),
    "cnt_1s": ("proxysql.performance.command.cnt_1s", MONOTONIC),
    "cnt_5s": ("proxysql.performance.command.cnt_5s", MONOTONIC),
    "cnt_10s": ("proxysql.performance.command.cnt_10s", MONOTONIC),
    "cnt_INFs": ("proxysql.performance.command.cnt_INFs", MONOTONIC),
}

STATS_MYSQL_CONNECTION_POOL = {
    "Connections_used": ("proxysql.pool.connections_used", GAUGE),
    "Connections_free": ("proxysql.pool.connections_free", GAUGE),
    "Connections_ok": ("proxysql.pool.connections_ok", RATE),
    "Connections_error": ("proxysql.pool.connections_error", RATE),
    "Queries": ("proxysql.pool.queries", RATE),
    "Bytes_data_sent": ("proxysql.pool.bytes_data_sent", RATE),
    "Bytes_data_recv": ("proxysql.pool.bytes_data_recv", RATE),
    "Latency_us": ("proxysql.pool.latency_ms", GAUGE),
}

STATS_MEMORY_METRICS = {
    "SQLite3_memory_bytes": ("proxysql.memory.sqlite3_memory", GAUGE),
    "jemalloc_resident": ("proxysql.memory.jemalloc_resident", GAUGE),
    "jemalloc_active": ("proxysql.memory.jemalloc_active", GAUGE),
    "jemalloc_allocated": ("proxysql.memory.jemalloc_allocated", GAUGE),
    "jemalloc_mapped": ("proxysql.memory.jemalloc_mapped", GAUGE),
    "jemalloc_metadata": ("proxysql.memory.jemalloc_metadata", GAUGE),
    "jemalloc_retained": ("proxysql.memory.jemalloc_retained", GAUGE),
    "Auth_memory": ("proxysql.memory.auth_memory", GAUGE),
    "query_digest_memory": ("proxysql.memory.query_digest_memory", GAUGE),
    "stack_memory_mysql_threads": ("proxysql.memory.stack_memory_mysql_threads", GAUGE),
    "stack_memory_admin_threads": ("proxysql.memory.stack_memory_admin_threads", GAUGE),
    "stack_memory_cluster_threads": ("proxysql.memory.stack_memory_cluster_threads", GAUGE),
}

STATS_MYSQL_USERS = {
    "User_Frontend_Connections": ("proxysql.frontend.user_connections", GAUGE),
    "User_Frontend_Max_Connections": ("proxysql.frontend.user_max_connections", GAUGE),
}


class ProxysqlCheck(AgentCheck):

    SERVICE_CHECK_NAME = "proxysql.can_connect"

    def check(self, instance):
        host, port, user, password, tags, options, connect_timeout, read_timeout = self._get_config(instance)

        if not host or not port or not user or not password:
            raise ConfigurationError("ProxySQL host, port, user and password are needed")

        with self._connect(host, port, user, password, tags, connect_timeout, read_timeout) as conn:
            self._collect_metrics(conn, tags, options)

    def _collect_metrics(self, conn, tags, options):
        """Collects all the different types of ProxySQL metrics and submits them to Datadog"""
        global_stats = self._get_global_stats(conn)
        for proxysql_metric_name, metric_details in STATS_MYSQL_GLOBAL.items():
            metric_name, metric_type = metric_details
            metric_tags = list(tags)
            value = global_stats.get(proxysql_metric_name)
            self._send_metric(metric_name, metric_type, float(global_stats.get(proxysql_metric_name)), metric_tags)

        if options.get("extra_command_counters_metrics", True):
            command_counters = self._get_command_counters(conn)
            for proxysql_metric_name, metric_details in STATS_COMMAND_COUNTERS.items():
                metric_name, metric_type = metric_details

                for metric in command_counters.get(proxysql_metric_name):
                    metric_tags = list(tags)
                    tag, value = metric
                    if tag:
                        metric_tags.append(tag)
                    self._send_metric(metric_name, metric_type, float(value), metric_tags)
                metric_tags = list(tags)

        if options.get("extra_connection_pool_metrics", True):
            conn_pool_stats = self._get_connection_pool_stats(conn)
            for proxysql_metric_name, metric_details in STATS_MYSQL_CONNECTION_POOL.items():
                metric_name, metric_type = metric_details

                for metric in conn_pool_stats.get(proxysql_metric_name):
                    metric_tags = list(tags)
                    tag, value = metric
                    if tag:
                        metric_tags.append(tag)
                    self._send_metric(metric_name, metric_type, float(value), metric_tags)

        if options.get("extra_memory_metrics", True):
            memory_stats = self._get_memory_stats(conn)
            for proxysql_metric_name, metric_details in STATS_MEMORY_METRICS.items():
                metric_name, metric_type = metric_details
                metric_tags = list(tags)
                self._send_metric(metric_name, metric_type, float(memory_stats.get(proxysql_metric_name)), metric_tags)

        if options.get("extra_user_metrics", True):
            user_stats = self._get_user_stats(conn)
            for proxysql_metric_name, metric_details in STATS_MYSQL_USERS.items():
                metric_name, metric_type = metric_details

                for metric in user_stats.get(proxysql_metric_name):
                    metric_tags = list(tags)
                    tag, value = metric
                    if tag:
                        metric_tags.append(tag)
                    self._send_metric(metric_name, metric_type, float(value), metric_tags)

    def _send_metric(self, metric_name, metric_type, metric_value, metric_tags):
        if metric_value is None:
            return

        if metric_type == RATE:
            self.rate(metric_name, metric_value, tags=metric_tags)
        elif metric_type == GAUGE:
            self.gauge(metric_name, metric_value, tags=metric_tags)
        elif metric_type == COUNT:
            self.count(metric_name, metric_value, tags=metric_tags)
        elif metric_type == MONOTONIC:
            self.monotonic_count(metric_name, metric_value, tags=metric_tags)

    def _get_global_stats(self, conn):
        """Fetch the global ProxySQL stats."""
        query = "SELECT * FROM stats.stats_mysql_global"

        try:
            with closing(conn.cursor()) as cursor:
                cursor.execute(query)

                if cursor.rowcount < 1:
                    self.warning("Failed to fetch records from the stats schema 'stats_mysql_global' table.")
                    return None

                return {row["Variable_Name"]: row["Variable_Value"] for row in cursor.fetchall()}
        except (pymysql.err.InternalError, pymysql.err.OperationalError) as e:
            self.warning("ProxySQL global stats unavailable at this time: {}".format(str(e)))
            return None

    def _get_command_counters(self, conn):
        """Fetch ProxySQL command counters stats"""
        query = "SELECT * FROM stats.stats_mysql_commands_counters"

        try:
            with closing(conn.cursor()) as cursor:
                cursor.execute(query)

                if cursor.rowcount < 1:
                    self.warning("Failed to fetch records from the stats schema 'stats_mysql_commands_counters' table.")
                    return None

                stats = defaultdict(list)
                for row in cursor.fetchall():
                    stats["Total_Time_ms"].append(
                        ("proxysql_command:%s" % row["Command"], str(float(row["Total_Time_us"]) / 1000))
                    )
                    stats["Total_cnt"].append(("proxysql_command:%s" % row["Command"], row["Total_cnt"]))
                    stats["cnt_100us"].append(("proxysql_command:%s" % row["Command"], row["cnt_100us"]))
                    stats["cnt_500us"].append(("proxysql_command:%s" % row["Command"], row["cnt_500us"]))
                    stats["cnt_1ms"].append(("proxysql_command:%s" % row["Command"], row["cnt_1ms"]))
                    stats["cnt_5ms"].append(("proxysql_command:%s" % row["Command"], row["cnt_5ms"]))
                    stats["cnt_10ms"].append(("proxysql_command:%s" % row["Command"], row["cnt_10ms"]))
                    stats["cnt_50ms"].append(("proxysql_command:%s" % row["Command"], row["cnt_50ms"]))
                    stats["cnt_100ms"].append(("proxysql_command:%s" % row["Command"], row["cnt_100ms"]))
                    stats["cnt_500ms"].append(("proxysql_command:%s" % row["Command"], row["cnt_500ms"]))
                    stats["cnt_1s"].append(("proxysql_command:%s" % row["Command"], row["cnt_1s"]))
                    stats["cnt_5s"].append(("proxysql_command:%s" % row["Command"], row["cnt_5s"]))
                    stats["cnt_10s"].append(("proxysql_command:%s" % row["Command"], row["cnt_10s"]))
                    stats["cnt_INFs"].append(("proxysql_command:%s" % row["Command"], row["cnt_INFs"]))

                return stats
        except (pymysql.err.InternalError, pymysql.err.OperationalError) as e:
            self.warning("ProxySQL commands counters stats unavailable at this time: {}".format(str(e)))
            return None

    def _get_connection_pool_stats(self, conn):
        """Fetch ProxySQL connection pool stats"""
        query = "SELECT * FROM stats.stats_mysql_connection_pool"

        try:
            with closing(conn.cursor()) as cursor:
                cursor.execute(query)

                if cursor.rowcount < 1:
                    self.warning("Failed to fetch records from the stats schema 'stats_mysql_connection_pool' table.")
                    return None

                stats = defaultdict(list)
                for row in cursor.fetchall():
                    stats["Connections_used"].append(("proxysql_db_node:%s" % row["srv_host"], row["ConnUsed"]))
                    stats["Connections_free"].append(("proxysql_db_node:%s" % row["srv_host"], row["ConnFree"]))
                    stats["Connections_ok"].append(("proxysql_db_node:%s" % row["srv_host"], row["ConnOK"]))
                    stats["Connections_error"].append(("proxysql_db_node:%s" % row["srv_host"], row["ConnERR"]))
                    stats["Queries"].append(("proxysql_db_node:%s" % row["srv_host"], row["Queries"]))
                    stats["Bytes_data_sent"].append(("proxysql_db_node:%s" % row["srv_host"], row["Bytes_data_sent"]))
                    stats["Bytes_data_recv"].append(("proxysql_db_node:%s" % row["srv_host"], row["Bytes_data_recv"]))
                    stats["Latency_us"].append(
                        ("proxysql_db_node:%s" % row["srv_host"], str(float(row["Latency_us"]) / 1000))
                    )

                return stats
        except (pymysql.err.InternalError, pymysql.err.OperationalError) as e:
            self.warning("ProxySQL connection_pool stats unavailable at this time: {}".format(str(e)))
            return None

    def _get_memory_stats(self, conn):
        """Fetch ProxySQL mmemory stats"""
        query = "SELECT * FROM stats.stats_memory_metrics"

        try:
            with closing(conn.cursor()) as cursor:
                cursor.execute(query)

                if cursor.rowcount < 1:
                    self.warning("Failed to fetch records from the stats schema 'stats_memory_metrics' table.")
                    return None

                return {row["Variable_Name"]: row["Variable_Value"] for row in cursor.fetchall()}
        except (pymysql.err.InternalError, pymysql.err.OperationalError) as e:
            self.warning("ProxySQL memory stats unavailable at this time: {}".format(str(e)))
            return None

    def _get_user_stats(self, conn):
        """Fetch ProxySQL Users Frontend connections stats"""
        query = "SELECT * FROM stats.stats_mysql_users"

        try:
            with closing(conn.cursor()) as cursor:
                cursor.execute(query)

                if cursor.rowcount < 1:
                    self.warning("Failed to fetch records from the stats schema 'stats_mysql_users' table.")
                    return None

                stats = defaultdict(list)
                for row in cursor.fetchall():
                    stats["User_Frontend_Connections"].append(
                        ("proxysql_mysql_user:%s" % row["username"], row["frontend_connections"])
                    )
                    stats["User_Frontend_Max_Connections"].append(
                        ("proxysql_mysql_user:%s" % row["username"], row["frontend_max_connections"])
                    )

                return stats
        except (pymysql.err.InternalError, pymysql.err.OperationalError) as e:
            self.warning("ProxySQL users stats unavailable at this time: {}".format(str(e)))
            return None

    def _get_config(self, instance):
        host = instance.get("server", "")
        port = int(instance.get("port", 0))

        user = instance.get("user", "")
        password = str(instance.get("pass", ""))
        tags = instance.get("tags", [])
        options = instance.get("options", {})
        connect_timeout = instance.get("connect_timeout", 10)
        read_timeout = instance.get("read_timeout", None)
        return host, port, user, password, tags, options, connect_timeout, read_timeout

    @contextmanager
    def _connect(self, host, port, user, password, tags, connect_timeout, read_timeout):
        self.service_check_tags = ["server:{}".format(host), "port:{}".format(str(port))].extend(tags)

        db = None
        try:
            db = pymysql.connect(
                host=host,
                user=user,
                port=port,
                passwd=password,
                connect_timeout=connect_timeout,
                read_timeout=read_timeout,
                cursorclass=pymysql.cursors.DictCursor,
            )
            self.log.debug("Connected to ProxySQL")
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.OK, tags=self.service_check_tags)
            yield db
        except Exception as e:
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.CRITICAL, tags=self.service_check_tags)
            self.log.exception(e)
            raise
        finally:
            if db:
                db.close()
