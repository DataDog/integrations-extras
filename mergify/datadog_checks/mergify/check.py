# (C) Datadog, Inc. 2023-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from json import JSONDecodeError

from requests.exceptions import ConnectionError, HTTPError, InvalidURL, Timeout

from datadog_checks.base import AgentCheck


class MergifyCheck(AgentCheck):
    # This will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = "mergify"

    def __init__(self, name, init_config, instances):
        super(MergifyCheck, self).__init__(name, init_config, instances)
        self.api_url = self.instance["mergify_api_url"]
        self.token = self.instance["token"]
        self.repositories = self.instance.get("repositories", {})
        self.tags = self.instance.get("tags", [])

    def check(self, _):
        # type: (Any) -> None
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        for repository, branches in self.repositories.items():
            queue_url = f"{self.api_url}/v1/repos/{repository}/queues"
            try:
                response = self.http.get(queue_url, headers=headers)
                response.raise_for_status()
                response_json = response.json()
            except Timeout as e:
                self.service_check(
                    "can_connect",
                    AgentCheck.CRITICAL,
                    message="Request timeout: {}, {}".format(queue_url, e),
                )
                return

            except (HTTPError, InvalidURL, ConnectionError) as e:
                self.service_check(
                    "can_connect",
                    AgentCheck.CRITICAL,
                    message="Request failed: {}, {}".format(queue_url, e),
                )
                raise

            except JSONDecodeError as e:
                self.service_check(
                    "can_connect",
                    AgentCheck.CRITICAL,
                    message="JSON Parse failed: {}, {}".format(queue_url, e),
                )
                raise

            except ValueError as e:
                self.service_check("can_connect", AgentCheck.CRITICAL, message=str(e))
                raise

            values = {}
            for queue in response_json["queues"]:
                values[queue["branch"]["name"]] = len(queue["pull_requests"])

            for branch in branches:
                queue_tags = self.tags.copy()
                queue_tags.append(f"branch:{branch}")
                queue_tags.append(f"repository:{repository}")
                value = values.get(branch, 0)
                self.gauge("merge_queue_length", value, tags=queue_tags)

        self.service_check("can_connect", AgentCheck.OK)
