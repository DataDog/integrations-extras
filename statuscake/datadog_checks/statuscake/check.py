import json

from typing import Any  # noqa: F401
from datadog_checks.base import AgentCheck  # noqa: F401

# from datadog_checks.base.utils.db import QueryManager
# from requests.exceptions import ConnectionError, HTTPError, InvalidURL, Timeout
# from json import JSONDecodeError


class StatuscakeCheck(AgentCheck):

    # This will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = 'statuscake'

    def __init__(self, name, init_config, instances):
        super(StatuscakeCheck, self).__init__(name, init_config, instances)

        # Use self.instance to read the check configuration
        # self.url = self.instance.get("url")

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

    def loadUptimePage(self, api_key, pageNum):
        try:
                response = self.http.get("https://api.statuscake.com/v1/uptime?page="+pageNum,headers = "Authorization: Bearer " + api_key)
                response.raise_for_status()
                response_json = response.json()

                data_list = response_json['data']

                ## Create a lsit to hold our values.
                filtered_data_list = []

                for data_entry in data_list:
                   if data_entry['paused'] is not True:
                       filtered_data_entry = [data_entry['id'],data_entry['name'],data_entry['website_url'],data_entry['check_rate'],data_entry['tags']]
                       filtered_data_list.append(filtered_data_entry)

        except Timeout as e:
                self.service_check("statuscake.can_connect",AgentCheck.CRITICAL,message="Request timeout: {}, {}".format(self.url, e))
                raise

        except (HTTPError, InvalidURL, ConnectionError) as e:
                self.service_check("statuscake.can_connect",AgentCheck.CRITICAL,message="Request failed: {}, {}".format(self.url, e))
                raise

        return filtered_data_list

    def check(self, _):
        # type: (Any) -> None


    ### READ VARIABLES

        check_type = instance.get('check_type')
        valid_check_types = ["ssl","uptime","pagespeed"]
        api_key = instance.get('statuscake_api_key')


    ### BASIC SANITY CHECK
        if not check_type:
            raise ConfigurationError('Configuration error. No check_type detected. Please fix statuscake.yaml')

        if check_type not in valid_check_types:
            raise ConfigurationError('Configuration error. The entered check_type failed to validate. Please fix statuscake.yaml')

        if not api_key:
            raise ConfigurationError('Configuration error. No api_key detected. Please fix statuscake.yaml')

    ### GET LIST OF STATUSCAKE CHECKS.

        # The following are useful bits of code to help new users get started.
        # Perform HTTP Requests with our HTTP wrapper.
        # More info at https://datadoghq.dev/integrations-core/base/http/

        if check_type is "uptime":
            try:
                response = self.http.get("https://api.statuscake.com/v1/uptime",headers = "Authorization: Bearer " + api_key)
                response.raise_for_status()
                response_json = response.json()

                if response_json is not None:
                ## Check how many pages there are.
                    metadata = response_json['metadata']
                    page_count = metadata['page_count']
                    filtered_data_list = []
                    page = 1                 
                    ## For each page, let's pull back our list of tests.
                    while page <= page_count:
                        filtered_data_list.append(self.loadUptimePage(api_key,page))
                        page += 1

                    ## Now we have our list, time to iterate.

                    self.service_check("statuscake.can_connect",AgentCheck.OK,message="Integration ran successfully.")

                else:
                    self.log.debug("No JSON response detected.")
            except Timeout as e:
                self.service_check("statuscake.can_connect",AgentCheck.CRITICAL,message="Request timeout: {}, {}".format(self.url, e))
                raise

            except (HTTPError, InvalidURL, ConnectionError) as e:
                self.service_check("statuscake.can_connect",AgentCheck.CRITICAL,message="Request failed: {}, {}".format(self.url, e))
                raise

        # except JSONDecodeError as e:
        #     self.service_check(
        #         "can_connect",
        #         AgentCheck.CRITICAL,
        #         message="JSON Parse failed: {}, {}".format(self.url, e),
        #     )
        #     raise

        # except ValueError as e:
        #     self.service_check(
        #         "can_connect", AgentCheck.CRITICAL, message=str(e)
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
        # self.service_check("can_connect", AgentCheck.OK)

        # If it didn't then it should send a critical service check
        self.service_check("statuscake.can_connect", AgentCheck.CRITICAL)
