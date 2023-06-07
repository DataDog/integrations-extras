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
        self.api_url = self.instance.get("mergify_api_url", "https://api.mergify.com")
        self.token = self.instance["token"]
        self.repositories = self.instance.get("repositories", {})
        self.tags = self.instance.get("tags", [])
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def check(self, _):
        # type: (Any) -> None

        self.send_queues_metrics()
        self.send_time_to_merge_metrics()
        self.send_queue_failure_metrics()

        self.service_check("can_connect", AgentCheck.OK)

    def get_request(self, url):
        try:
            response = self.http.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Timeout as e:
            self.service_check(
                "can_connect",
                AgentCheck.CRITICAL,
                message="Request timeout: {}, {}".format(url, e),
            )
            return

        except (HTTPError, InvalidURL, ConnectionError) as e:
            self.service_check(
                "can_connect",
                AgentCheck.CRITICAL,
                message="Request failed: {}, {}".format(url, e),
            )
            raise

        except JSONDecodeError as e:
            self.service_check(
                "can_connect",
                AgentCheck.CRITICAL,
                message="JSON Parse failed: {}, {}".format(url, e),
            )
            raise

        except ValueError as e:
            self.service_check("can_connect", AgentCheck.CRITICAL, message=str(e))
            raise

    def send_queues_metrics(self):
        for repository, branches in self.repositories.items():
            queue_url = f"{self.api_url}/v1/repos/{repository}/queues"
            response_json = self.get_request(queue_url)

            values = {}
            for queue in response_json["queues"]:
                values[queue["branch"]["name"]] = len(queue["pull_requests"])

            for branch in branches:
                queue_tags = self.tags.copy()
                queue_tags.append(f"branch:{branch}")
                queue_tags.append(f"repository:{repository}")
                value = values.get(branch, 0)
                self.gauge("merge_queue_length", value, tags=queue_tags)

    def send_time_to_merge_metrics(self):
        for repository, branches in self.repositories.items():
            for branch in branches:
                default_tags = self.tags.copy()
                default_tags.append(f"repository:{repository}")
                default_tags.append(f"branch:{branch}")

                url = f"{self.api_url}/v1/repos/{repository}/stats/time_to_merge?branch={branch}"
                response_json = self.get_request(url)

                for partition_data in response_json:
                    partition_tags = default_tags.copy()
                    partition_tags.append(f"partition:{partition_data['partition_name']}")

                    for queue_data in partition_data["queues"]:
                        queue_tags = partition_tags.copy()
                        queue_tags.append(f"queue:{queue_data['queue_name']}")

                        for stat_name, stat_value in queue_data["time_to_merge"].items():
                            if stat_value is None:
                                continue

                            self.gauge(
                                f"time_to_merge.{stat_name}",
                                stat_value,
                                tags=queue_tags,
                            )

    def send_queue_failure_metrics(self):
        for repository, branches in self.repositories.items():
            for branch in branches:
                default_tags = self.tags.copy()
                default_tags.append(f"repository:{repository}")
                default_tags.append(f"branch:{branch}")

                url = f"{self.api_url}/v1/repos/{repository}/stats/queue_checks_outcome?branch={branch}"
                response_json = self.get_request(url)

                for partition_data in response_json:
                    partition_tags = default_tags.copy()
                    partition_tags.append(f"partition:{partition_data['partition_name']}")

                    for queue_data in partition_data["queues"]:
                        queue_tags = partition_tags.copy()
                        queue_tags.append(f"queue:{queue_data['queue_name']}")

                        for outcome_type, number_of_outcome in queue_data["queue_checks_outcome"].items():
                            if outcome_type == "SUCCESS":
                                continue

                            self.gauge(
                                "queue_checks_outcome",
                                number_of_outcome,
                                tags=queue_tags + [f"outcome_type:{outcome_type}"],
                            )
