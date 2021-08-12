from typing import Any

from datadog_checks.base import ConfigurationError, OpenMetricsBaseCheck

# from datadog_checks.base.utils.db import QueryManager
# from requests.exceptions import ConnectionError, HTTPError, InvalidURL, Timeout
# from json import JSONDecodeError


class CalicoCheck(OpenMetricsBaseCheck):
    def __init__(self, name, init_config, instances=None):
        METRICS_MAP = {'felix_active_local_endpoints': 'felix_active_local_endpoints'}

        super(CalicoCheck, self).__init__(
            name,
            init_config,
            instances,
            default_instances={
                'calico-felix': {
                    'prometheus_url': 'http://localhost:9091/metrics',
                    'namespace': 'kube-system',
                    'metrics': [METRICS_MAP],
                }
            },
            default_namespace='kube-system',
        )

    def check(self, instance):
        endpoint = instance.get('prometheus_url')
        if endpoint is None:
            raise ConfigurationError("Unable to find prometheus_url in config file.")
        config = self.create_scraper_configuration(instance)
        self.process(config)
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
        #         "calico.can_connect",
        #         AgentCheck.CRITICAL,
        #         message="Request timeout: {}, {}".format(url, e),
        #     )
        #     raise

        # except (HTTPError, InvalidURL, ConnectionError) as e:
        #     self.service_check(
        #         "calico.can_connect",
        #         AgentCheck.CRITICAL,
        #         message="Request failed: {}, {}".format(url, e),
        #     )
        #     raise

        # except JSONDecodeError as e:
        #     self.service_check(
        #         "calico.can_connect",
        #         AgentCheck.CRITICAL,
        #         message="JSON Parse failed: {}, {}".format(url, e),
        #     )
        #     raise

        # except ValueError as e:
        #     self.service_check(
        #         "calico.can_connect", AgentCheck.CRITICAL, message=str(e)
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
        # self.service_check("calico.can_connect", AgentCheck.OK)

        pass
