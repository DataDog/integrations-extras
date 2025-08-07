from typing import Any  # noqa: F401

from datadog_checks.base import AgentCheck  # noqa: F401
from requests.exceptions import ConnectionError, HTTPError, InvalidURL, Timeout


class StonebranchCheck(AgentCheck):

    # This will be the prefix of every metric the integration sends
    __NAMESPACE__ = 'stonebranch'

    def __init__(self, name, init_config, instances):
        super(StonebranchCheck, self).__init__(name, init_config, instances)

        # Use self.instance to read the check configuration
        self.url = self.instance.get("url")
        self.username = self.instance.get("username") 
        self.password = self.instance.get("password")

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
        # type: (Any) -> None
        if not self.url:
            self.service_check('stonebranch.can_connect', AgentCheck.CRITICAL, message="URL not configured")
            return

        metrics_url = self.url.rstrip('/') + '/resources/metrics'
        
        try:
            response = self.http.get(
                metrics_url,
                auth=(self.username, self.password) if self.username and self.password else None
            )
            response.raise_for_status()
            
            # Parse Prometheus format metrics
            self._parse_prometheus_metrics(response.text)
            self.service_check('stonebranch.can_connect', AgentCheck.OK)

        except (HTTPError, InvalidURL, ConnectionError, Timeout) as e:
            self.log.error("Could not connect to Stonebranch: %s", str(e))
            self.service_check('stonebranch.can_connect', AgentCheck.CRITICAL, message=str(e))

        except Exception as e:
            self.log.error("Unexpected error: %s", str(e))
            self.service_check('stonebranch.can_connect', AgentCheck.CRITICAL, message=str(e))

    def _parse_prometheus_metrics(self, metrics_text):
        """Parse Prometheus format metrics and submit to Datadog"""
        for line in metrics_text.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            parts = line.split(' ')
            if len(parts) >= 2:
                metric_name = parts[0]
                try:
                    metric_value = float(parts[1])
                    self.gauge(metric_name, metric_value)
                except ValueError:
                    continue
