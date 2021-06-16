
from typing import Any

from datadog_checks.base import AgentCheck

# from datadog_checks.base.utils.db import QueryManager
# from requests.exceptions import ConnectionError, HTTPError, InvalidURL, Timeout
import json

from datadog_checks.base.utils.subprocess_output import get_subprocess_output, SubprocessOutputEmptyError


class FoundationdbCheck(AgentCheck):
    def __init__(self, name, init_config, instances):
        super(FoundationdbCheck, self).__init__(name, init_config, instances)
        self.fdb_status = init_config.get('fdbstatus_path')

    def fdb_status_data(self):
        fdb_args = self.fdb_status[:] # do a copy not to pollute original list
        fdb_args.append('status json')
        return get_subprocess_output(fdb_args, self.log)

        # If the check is going to perform SQL queries you should define a query manager here.
        # More info at
        # https://datadoghq.dev/integrations-core/base/databases/#datadog_checks.base.utils.db.core.QueryManager
        # sample_query = {
        #     "name": "sample",
        #     "query": "SELECT * FROM sample_table",
        #     "columns": [
        #         {"name": "metric", "type": "gauge"}
        #     ],
        # }
        # self._query_manager = QueryManager(self, self.execute_query, queries=[sample_query])
        # self.check_initializations.append(self._query_manager.compile_queries)

    def check(self, _):
        try:
            status = self.fdb_status_data()
        except SubprocessOutputEmptyError as e:
            self.service_check("foundationdb.can_connect", AgentCheck.CRITICAL, message="Did not receive a response from `status json`")
            raise

        if status[2] != 0:
            self.service_check("foundationdb.can_connect", AgentCheck.CRITICAL, message="`fdbcli` returned non-zero error code")
            raise ValueError("`fdbcli --exec 'status json'` failed")

        try:
            data = json.loads(status[0])
        except Exception as e:
            self.service_check("foundationdb.can_connect", AgentCheck.CRITICAL, message="Could not parse `status json`")
            raise

        self.check_metrics(data)

    def check_metrics(self, status):
        if not "cluster" in status:
            raise ValueError("JSON Status data doesn't include cluster data")

        cluster = status["cluster"]
        if "degraded_processes" in cluster:
            self.gauge("foundationdb.degraded_processes", cluster["degraded_processes"])
        if "machines" in cluster:
            self.gauge("foundationdb.machines", len(cluster["machines"]))
        if "processes" in cluster:
            self.gauge("foundationdb.processes", len(cluster["processes"]))

            self.count("foundationdb.instances", sum(map(lambda p: len(p["roles"]) if "roles" in p else 0, cluster["processes"].values())))

        if "data" in cluster:
            data = cluster["data"]
            self.maybe_gauge("foundationdb.data.system_kv_size_bytes", data, "system_kv_size_bytes")
            self.maybe_gauge("foundationdb.data.total_disk_used_bytes", data, "total_disk_used_bytes")
            self.maybe_gauge("foundationdb.data.total_kv_size_bytes", data, "total_kv_size_bytes")
            self.maybe_gauge("foundationdb.data.least_operating_space_bytes_log_server", data, "least_operating_space_bytes_log_server")

            if "moving_data" in data:
                self.maybe_gauge("foundationdb.data.moving_data.in_flight_bytes", data["moving_data"], "in_flight_bytes")
                self.maybe_gauge("foundationdb.data.moving_data.in_queue_bytes", data["moving_data"], "in_queue_bytes")
                self.maybe_gauge("foundationdb.data.moving_data.total_written_bytes", data["moving_data"], "total_written_bytes")

        if "datacenter_lag" in cluster:
            self.gauge("foundationdb.datacenter_lag.seconds", cluster["datacenter_lag"]["seconds"])

        if "workload" in cluster:
            workload = cluster["workload"]
            if "transactions" in workload:
                for k, v in workload["transactions"].items():
                    self.maybe_gauge("foundationdb.workload.transactions." + k + ".hz", v, "hz")
                    self.maybe_count("foundationdb.workload.transactions." + k + ".counter", v, "counter")

            if "operations" in workload:
                for k, v in workload["operations"].items():
                    self.maybe_gauge("foundationdb.workload.operations." + k + ".hz", v, "hz")
                    self.maybe_count("foundationdb.workload.operations." + k + ".counter", v, "counter")

        if "latency_probe" in cluster:
            for k, v in cluster["latency_probe"].items():
                self.gauge("foundationdb.latency_probe." + k, v)

        self.service_check("foundationdb.can_connect", AgentCheck.OK)

    def maybe_gauge(self, metric, obj, key):
        if key in obj:
            self.gauge(metric, obj[key])

    def maybe_count(self, metric, obj, key):
        if key in obj:
            self.count(metric, obj[key])

        # type: (Any) -> None
        # The following are useful bits of code to help new users get started.

        # Use self.instance to read the check configuration
        # url = self.instance.get("url")

        # Perform HTTP Requests with our HTTP wrapper.
        # More info at https://datadoghq.dev/integrations-core/base/http/
        # try:
        #     response = self.http.get(url)
        #     response.raise_for_status()
        #     response_json = response.json()

        # except Timeout as e:
        #     self.service_check(
        #         "foundationdb.can_connect",
        #         AgentCheck.CRITICAL,
        #         message="Request timeout: {}, {}".format(url, e),
        #     )
        #     raise

        # except (HTTPError, InvalidURL, ConnectionError) as e:
        #     self.service_check(
        #         "foundationdb.can_connect",
        #         AgentCheck.CRITICAL,
        #         message="Request failed: {}, {}".format(url, e),
        #     )
        #     raise

        # except JSONDecodeError as e:
        #     self.service_check(
        #         "foundationdb.can_connect",
        #         AgentCheck.CRITICAL,
        #         message="JSON Parse failed: {}, {}".format(url, e),
        #     )
        #     raise

        # except ValueError as e:
        #     self.service_check(
        #         "foundationdb.can_connect", AgentCheck.CRITICAL, message=str(e)
        #     )
        #     raise

        # This is how you submit metrics
        # There are different types of metrics that you can submit (gauge, event).
        # More info at https://datadoghq.dev/integrations-core/base/api/#datadog_checks.base.checks.base.AgentCheck
        # self.gauge("test", 1.23, tags=['foo:bar'])

        # Perform database queries using the Query Manager
        # self._query_manager.execute()

        # This is how you use the persistent cache. This cache file based and persists across agent restarts.
        # If you need an in-memory cache that is persisted across runs
        # You can define a dictionary in the __init__ method.
        # self.write_persistent_cache("key", "value")
        # value = self.read_persistent_cache("key")

        # If your check ran successfully, you can send the status.
        # More info at
        # https://datadoghq.dev/integrations-core/base/api/#datadog_checks.base.checks.base.AgentCheck.service_check
        # self.service_check("foundationdb.can_connect", AgentCheck.OK)
