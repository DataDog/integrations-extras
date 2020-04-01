from datadog_checks.base import AgentCheck
from . import burrow_urls

import requests

CONFIG_BURROW_URL = "url"
CONFIG_TIMEOUT = "timeout"
CONFIG_CLUSTERS = "clusters"
CONFIG_TAGS = "tags"

TIMEOUT_DEFAULT = 20

HEALTH_CHECK_NAME = "burrow.can_connect"


class BurrowCheck(AgentCheck):
    def check(self, instance):
        burrow_url = instance.get(CONFIG_BURROW_URL, "http://localhost:8000")
        burrow_clusters = instance.get(CONFIG_CLUSTERS, [])
        extra_tags = instance.get(CONFIG_TAGS, [])
        timeout = instance.get(CONFIG_TIMEOUT, TIMEOUT_DEFAULT)

        self.log.debug("Starting check on burrow %s", burrow_url)
        self._health_check(burrow_url, timeout, extra_tags)

        clusters = self._find_clusters(burrow_url, burrow_clusters, timeout)

        self.log.debug("Collecting Consumer Group Offsets")
        self._consumer_groups_offsets(
            burrow_url, clusters, timeout, extra_tags)

        self.log.debug("Collecting Topic Offsets")
        self._topic_offsets(burrow_url, clusters, timeout, extra_tags)

        self.log.debug("Collecting Consumer Group lags")
        self._consumer_groups_lags(
            burrow_url, clusters, timeout, extra_tags)

    def _health_check(self, burrow_url, timeout, extra_tags):
        """
        Check the Burrow health check endpoint
        """
        burrow_admin = burrow_urls.burrow_admin(burrow_url)
        try:
            tags = ["instance:%s" % self.hostname]
            tags.append(extra_tags)
            response = requests.get(burrow_admin, timeout=timeout)
            response.raise_for_status()
        except Exception as e:
            self.service_check(HEALTH_CHECK_NAME,
                               AgentCheck.CRITICAL,
                               tags=tags,
                               message=str(e))
        else:
            self.service_check(HEALTH_CHECK_NAME,
                               AgentCheck.OK,
                               tags=tags,
                               message="Connection to %s was successful" % burrow_admin)

    def _submit_lag_status(self, metric_namespace, status, tags):
        burrow_status = {
            "UNKNOWN": 0,
            "OK": 0,
            "WARN": 0,
            "ERR": 0,
            "STOP": 0,
            "STALL": 0,
            "REWIND": 0
        }

        if status not in burrow_status.keys():
            self.log.error("Invalid lag status: '%s' for '%s'" %
                           (status, tags))
            return

        burrow_status[status] = 1

        for metric_name, value in burrow_status.iteritems():
            self.gauge(
                "%s.%s" % (metric_namespace, metric_name.lower()), value, tags=tags)

    def _submit_partition_lags(self, partition, tags):
        end = partition.get("end")
        if end is not None:
            lag = end.get("lag")
            self.gauge("burrow.kafka.consumer.partition_lag", lag, tags=tags)

    def _do_get(self, url, timeout=TIMEOUT_DEFAULT):
        response_json = None
        try:
            response = requests.get(url, timeout=timeout)
            try:
                response_json = response.json()

                if response_json["error"]:
                    self.log.error(
                        "Burrow Request failed: %s: %s", url, response_json["message"])
                    return {}
                
            except Exception as e:
                response.raise_for_status()
                raise e

        except requests.exceptions.Timeout as e:
            self.log.error("Request timeout: %s, %s", url, e)
            raise

        except (requests.exceptions.HTTPError,
                requests.exceptions.InvalidURL,
                requests.exceptions.ConnectionError) as e:
            self.log.error("Request failed:  %s, %s", url, e)
            raise

        except ValueError as e:
            self.log.error(str(e))
            raise

        else:
            self.log.debug("Connection to %s was successful", url)

        return response_json

    def _submit_offsets_from_json(self, offsets_type, offsets_list, tags):
        offsets = []
        for partition_number, offset_info in enumerate(offsets_list):
            new_tags = tags + ["partition:%s" % partition_number]
            latest_offset = None
            offset_timestamp = 0
            for offset in offset_info["offsets"]:
                if not offset:
                    continue
                if offset["timestamp"] > offset_timestamp:
                    latest_offset = offset["offset"]
                    offsets.append(latest_offset)

            self.gauge(
                "burrow.kafka.%s.offsets" % offsets_type, latest_offset, tags=new_tags)
        offsets = [max(offset, 0) for offset in offsets]
        self.gauge("burrow.kafka.%s.offsets.total" % offsets_type, sum(
            offsets), tags=tags)

    def _find_clusters(self, burrow_url, target, timeout):
        available_clusters = self._do_get(
            burrow_urls.clusters(burrow_url), timeout=timeout).get("clusters")

        if not available_clusters:
            raise Exception("There are no clusters in Burrow")

        if not target:
            return available_clusters
        else:
            clusters = []
            for name in target:
                if name in available_clusters:
                    clusters.append(name)
                else:
                    self.log.error("Cluster '%s' does not exist", name)
            return clusters

    def _topic_offsets(self, burrow_url, burrow_clusters, timeout, extra_tags):
        """
        Retrieve the offsets for all topics in the clusters
        """
        for cluster in burrow_clusters:
            topics_path = burrow_urls.topics(burrow_url, cluster)
            topics_list = self._do_get(topics_path, timeout=timeout).get("topics", [])

            for topic in topics_list:
                topic_path = burrow_urls.topic(burrow_url, cluster, topic)
                response = self._do_get(topic_path, timeout=timeout)
                tags = ["topic:%s" % topic,
                        "cluster:%s" % cluster] + extra_tags

                offsets_list = []
                for offset in response["offsets"]:
                    offsets_list.append(
                        {"offsets": [{"offset": offset, "timestamp": 1}]})
                self._submit_offsets_from_json(
                    offsets_type="topic", offsets_list=offsets_list, tags=tags)

    def _consumer_groups_offsets(self, burrow_url, burrow_clusters, timeout, extra_tags):
        for cluster in burrow_clusters:
            consumers_path = burrow_urls.consumers(burrow_url, cluster)
            consumers_list = self._do_get(consumers_path, timeout=timeout).get("consumers", [])

            for consumer in consumers_list:
                consumer_path = burrow_urls.consumer(
                    burrow_url, cluster, consumer)
                topics = self._do_get(consumer_path, timeout=timeout).get("topics", [])
                for topic in topics:
                    topic_path = burrow_urls.topic(burrow_url, cluster, topic)
                    response = self._do_get(topic_path, timeout=timeout)
                    if not response:
                        continue
                    tags = ["topic:%s" % topic,
                            "cluster:%s" % cluster,
                            "consumer:%s" % consumer] + extra_tags
                    self._submit_offsets_from_json(
                        offsets_type="consumer", offsets_list=topics[topic], tags=tags)

    def _consumer_groups_lags(self, burrow_url, burrow_clusters, timeout, extra_tags):
        for cluster in burrow_clusters:
            consumers_path = burrow_urls.consumers(burrow_url, cluster)
            consumers_list = self._do_get(consumers_path, timeout=timeout).get("consumers", [])
            for consumer in consumers_list:
                lags_path = burrow_urls.consumer_lag(
                    burrow_url, cluster, consumer)
                lag_json = self._do_get(lags_path, timeout=timeout)
                if not lag_json:
                    continue
                status = lag_json["status"]
                consumer_tags = ["cluster:%s" % cluster,
                                 "consumer:%s" % consumer] + extra_tags

                self.gauge("burrow.kafka.consumer.maxlag",
                           status["maxlag"]["end"]["lag"], tags=consumer_tags)
                self.gauge("burrow.kafka.consumer.totallag",
                           status["totallag"], tags=consumer_tags)
                self._submit_lag_status(
                    "burrow.kafka.consumer.lag_status", status["status"], tags=consumer_tags)

                for partition in status.get("partitions", []):
                    partition_tags = consumer_tags + \
                        ["topic:%s" % partition["topic"],
                         "partition:%s" % partition["partition"]]
                    self._submit_partition_lags(partition, partition_tags)
                    self._submit_lag_status(
                        "burrow.kafka.consumer.partition_lag_status", partition["status"], tags=partition_tags)
