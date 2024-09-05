
from typing import Any  # noqa: F401

from datadog_checks.base import AgentCheck  # noqa: F401
from datadog_checks.base import OpenMetricsBaseCheckV2
from datadog_checks.base import ConfigurationError

# from datadog_checks.base.utils.db import QueryManager
# from requests.exceptions import ConnectionError, HTTPError, InvalidURL, Timeout
# from json import JSONDecodeError


# class MaurisourceMagentoCheck(AgentCheck):

#     # This will be the prefix of every metric and service check the integration sends
#     __NAMESPACE__ = 'maurisource_magento'

#     def __init__(self, name, init_config, instances):
#         super(MaurisourceMagentoCheck, self).__init__(name, init_config, instances)

#         # Use self.instance to read the check configuration
#         # self.url = self.instance.get("url")

#         # If the check is going to perform SQL queries you should define a query manager here.
#         # More info at
#         # https://datadoghq.dev/integrations-core/base/databases/#datadog_checks.base.utils.db.core.QueryManager
#         # sample_query = {
#         #     "name": "sample",
#         #     "query": "SELECT * FROM sample_table",
#         #     "columns": [
#         #         {"name": "metric", "type": "gauge"}
#         #     ],
#         # }
#         # self._query_manager = QueryManager(self, self.execute_query, queries=[sample_query])
#         # self.check_initializations.append(self._query_manager.compile_queries)

#     def check(self, _):
#         # type: (Any) -> None
#         # The following are useful bits of code to help new users get started.

#         # Perform HTTP Requests with our HTTP wrapper.
#         # More info at https://datadoghq.dev/integrations-core/base/http/
#         # try:
#         #     response = self.http.get(self.url)
#         #     response.raise_for_status()
#         #     response_json = response.json()

#         # except Timeout as e:
#         #     self.service_check(
#         #         "can_connect",
#         #         AgentCheck.CRITICAL,
#         #         message="Request timeout: {}, {}".format(self.url, e),
#         #     )
#         #     raise

#         # except (HTTPError, InvalidURL, ConnectionError) as e:
#         #     self.service_check(
#         #         "can_connect",
#         #         AgentCheck.CRITICAL,
#         #         message="Request failed: {}, {}".format(self.url, e),
#         #     )
#         #     raise

#         # except JSONDecodeError as e:
#         #     self.service_check(
#         #         "can_connect",
#         #         AgentCheck.CRITICAL,
#         #         message="JSON Parse failed: {}, {}".format(self.url, e),
#         #     )
#         #     raise

#         # except ValueError as e:
#         #     self.service_check(
#         #         "can_connect", AgentCheck.CRITICAL, message=str(e)
#         #     )
#         #     raise

#         # This is how you submit metrics
#         # There are different types of metrics that you can submit (gauge, event).
#         # More info at https://datadoghq.dev/integrations-core/base/api/#datadog_checks.base.checks.base.AgentCheck
#         # self.gauge("test", 1.23, tags=['foo:bar'])

#         # Perform database queries using the Query Manager
#         # self._query_manager.execute()

#         # This is how you use the persistent cache. This cache file based and persists across agent restarts.
#         # If you need an in-memory cache that is persisted across runs
#         # You can define a dictionary in the __init__ method.
#         # self.write_persistent_cache("key", "value")
#         # value = self.read_persistent_cache("key")

#         # If your check ran successfully, you can send the status.
#         # More info at
#         # https://datadoghq.dev/integrations-core/base/api/#datadog_checks.base.checks.base.AgentCheck.service_check
#         # self.service_check("can_connect", AgentCheck.OK)

#         # If it didn't then it should send a critical service check
#         # self.service_check("can_connect", AgentCheck.CRITICAL)
#         self.service_check("can_connect", AgentCheck.OK)



class MaurisourceMagentoCheck(OpenMetricsBaseCheckV2):
    __NAMESPACE__ = "maurisource_magento"

    def __init__(self, name, init_config, instances):
        super(MaurisourceMagentoCheck, self).__init__(name, init_config, instances)

        self.metrics_map =  {
            "magento_orders_count_total": "magento_orders_count",
            "magento_orders_amount_total": "magento_orders_amount",
            "magento_order_items_count_total": "magento_order_items_count",
            "magento_cms_block_count_total": "magento_cms_block_count",
            "magento_cms_page_count_total": "magento_cms_page_count",
            "magento_customer_count_total": "magento_customer_count",
            "magento_cronjob_broken_count_total": "magento_cronjob_broken_count",
            "magento_cronjob_count_total": "magento_cronjob_count",
            "magento_indexer_backlog_count_total": "magento_indexer_backlog_count",
            "magento_shipments_count_total": "magento_shipments_count",
            "magento_catalog_category_count_total": "magento_catalog_category_count",
            "magento_store_count_total": "magento_store_count",
            "magento_website_count_total": "magento_website_count",
            "magento_products_by_type_count_toal": "magento_products_by_type_count "

        }

    def get_default_config(self):
        return {'metrics': self.metrics_map}
    
    def check(self, instance):
          endpoint = instance.get('openmetrics_endpoint')
          if endpoint is None:
              raise ConfigurationError("Unable to find openmetrics_endpoint in config file.")

          super().check(instance)