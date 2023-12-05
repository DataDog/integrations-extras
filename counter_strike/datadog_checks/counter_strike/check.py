
from typing import Any  # noqa: F401

from datadog_checks.base import AgentCheck  # noqa: F401

from server import GSIServer
from uuid import uuid1

# from datadog_checks.base.utils.db import QueryManager
# from requests.exceptions import ConnectionError, HTTPError, InvalidURL, Timeout
# from json import JSONDecodeError


class CounterStrikeCheck(AgentCheck):

    # This will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = 'counter_strike'

    def __init__(self, name, init_config, instances):
        super(CounterStrikeCheck, self).__init__(name, init_config, instances)

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
        self.server = GSIServer(("127.0.0.1", 3000), "S8RL9Z6Y22TYQK45JB4V8PHRJJMD9DS9")
        self.gamestate = self.server.gamestate
        self.current_match = None

    def match_over(self):
        if self.gamestate.map.round <= 24: # regulation
            return self.gamestate.map.team_ct.score == 13 or self.gamestate.map.team_t.score == 13
        elif self.gamestate.map.round % 6 == 0 or self.gamestate.map.round % 6 >= 4:
            return abs(self.gamestate.map.team_ct.score - self.gamestate.map.team_t.score) == 2
        return False
                
    def send_end_match_stats(self):
        return
    
    def send_current_stats(self):
        self.gauge("counter_strike.current.kills", self.gamestate.player.match_stats.kills, [])
        self.gauge("counter_strike.current.assists", self.gamestate.player.match_stats.assists, [])
        self.gauge("counter_strike.current.deaths", self.gamestate.player.match_stats.deaths, [])
        return

    def check(self, _):
        # type: (Any) -> None
        # The following are useful bits of code to help new users get started.

        # Perform HTTP Requests with our HTTP wrapper.
        # More info at https://datadoghq.dev/integrations-core/base/http/
        # try:
        #     response = self.http.get(self.url)
        #     response.raise_for_status()
        #     response_json = response.json()

        # except Timeout as e:
        #     self.service_check(
        #         "can_connect",
        #         AgentCheck.CRITICAL,
        #         message="Request timeout: {}, {}".format(self.url, e),
        #     )
        #     raise

        # except (HTTPError, InvalidURL, ConnectionError) as e:
        #     self.service_check(
        #         "can_connect",
        #         AgentCheck.CRITICAL,
        #         message="Request failed: {}, {}".format(self.url, e),
        #     )
        #     raise

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
        print(self.server.get_info("player", "map", "round"))
        if self.current_match == None:
            self.current_match = uuid1()
        elif self.match_over():
            self.current_match = None
            self.send_end_match_stats()
        else:
            self.send_current_stats()


        self.service_check("can_connect", AgentCheck.OK)
