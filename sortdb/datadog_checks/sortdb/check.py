# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
import time
from hashlib import md5

import requests
from requests.exceptions import ConnectionError, HTTPError, InvalidURL, Timeout
from simplejson import JSONDecodeError
from six import iteritems

from datadog_checks.base import AgentCheck

# Metric types
GAUGE = 'gauge'
COUNTER = 'counter'
SORTDB_METRICS = {
    'total_requests': ('sortdb.stats.total_requests', GAUGE),
    'total_seeks': ('sortdb.stats.total_seeks', GAUGE),
    'get_requests': ('sortdb.stats.get_requests', GAUGE),
    'get_hits': ('sortdb.stats.get_hits', GAUGE),
    'get_misses': ('sortdb.stats.get_misses', GAUGE),
    'get_average_request': ('sortdb.stats.get_requests.avg', GAUGE),
    'get_95': ('sortdb.stats.get_requests.95percentile', GAUGE),
    'get_99': ('sortdb.stats.get_requests.99percentile', GAUGE),
    'mget_requests': ('sortdb.stats.mget_requests', GAUGE),
    'mget_hits': ('sortdb.stats.mget_hits', GAUGE),
    'mget_misses': ('sortdb.stats.mget_misses', GAUGE),
    'mget_average_request': ('sortdb.stats.mget_requests.avg', GAUGE),
    'mget_95': ('sortdb.stats.mget_requests.95percentile', GAUGE),
    'mget_99': ('sortdb.stats.mget_requests.99percentile', GAUGE),
    'fwmatch_requests': ('sortdb.stats.fwmatch_requests', GAUGE),
    'fwmatch_hits': ('sortdb.stats.fwmatch_hits', GAUGE),
    'fwmatch_misses': ('sortdb.stats.fwmatch_misses', GAUGE),
    'fwmatch_average_request': ('sortdb.stats.fwmatch_requests.avg', GAUGE),
    'fwmatch_95': ('sortdb.stats.fwmatch_requests.95percentile', GAUGE),
    'fwmatch_99': ('sortdb.stats.fwmatch_requests.99percentile', GAUGE),
    'range_requests': ('sortdb.stats.range_requests', GAUGE),
    'range_hits': ('sortdb.stats.range_hits', GAUGE),
    'range_misses': ('sortdb.stats.range_misses', GAUGE),
    'range_average_request': ('sortdb.stats.range_requests.avg', GAUGE),
    'range_95': ('sortdb.stats.range_requests.95percentile', GAUGE),
    'range_99': ('sortdb.stats.range_requests.99percentile', GAUGE),
    'db_size': ('sortdb.stats.db_size.bytes', GAUGE),
    'db_mtime': ('sortdb.stats.db_mtime', GAUGE),
}


class SortdbCheck(AgentCheck):
    SORTDB_SERVICE_CHECK = 'sortdb.http.can_connect'
    EVENT_TYPE = SOURCE_TYPE_NAME = 'sortdb'

    def check(self, instance):
        sortdb_url = instance.get('url')
        if sortdb_url is None:
            raise Exception('The Sortdb http api stats url must be specified in the configuration')
        # get tags for instances to differentiate multiple instances
        instance_tags = instance.get('tags', [])
        # deduplicating the tags
        instance_tags = list(set(instance_tags))
        # service check
        self.service_check(
            self.SORTDB_SERVICE_CHECK,
            AgentCheck.OK,
            tags=instance_tags,
        )

        # get and set metrics
        self._get_sortdb_metrics(sortdb_url, SORTDB_METRICS, instance_tags)

    def _get_response_from_url(self, url, timeout, aggregation_key, instance_tags):
        """
        Send rest request to address and return the response as JSON
        """
        response = None
        self.log.debug('Sending request to "%s"', url)

        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            response = response.json()

        except Timeout as e:
            self.service_check(
                self.SORTDB_SERVICE_CHECK,
                AgentCheck.CRITICAL,
                tags=instance_tags,
                message="Request timeout: {}, {}".format(url, e),
            )
            self.timeout_event(url, timeout, aggregation_key)
            raise

        except (HTTPError, InvalidURL, ConnectionError) as e:
            self.service_check(
                self.SORTDB_SERVICE_CHECK,
                AgentCheck.CRITICAL,
                tags=instance_tags,
                message="Request failed: {0}, {1}".format(url, e),
            )
            raise

        except JSONDecodeError as e:
            self.service_check(
                self.SORTDB_SERVICE_CHECK,
                AgentCheck.CRITICAL,
                tags=instance_tags,
                message='JSON Parse failed: {0}, {1}'.format(url, e),
            )
            raise

        except ValueError as e:
            self.service_check(self.SORTDB_SERVICE_CHECK, AgentCheck.CRITICAL, tags=instance_tags, message=str(e))
            raise

        return response

    def _get_sortdb_metrics(self, sortdb_url, metrics, instance_tags):
        """
        Get SortDB metrics
        """
        timeout = float(self.init_config.get('timeout', 10))
        # Use a hash of the URL as an aggregation key
        aggregation_key = md5(sortdb_url.encode('utf-8')).hexdigest()

        response = self._get_response_from_url(sortdb_url, timeout, aggregation_key, instance_tags)
        for metric, (metric_name, metric_type) in iteritems(metrics):
            value = response.get(metric)

            if value is not None:
                self._set_metric(metric_name, metric_type, value, instance_tags)

            else:
                self.log.debug('Value not returned for metric: "%s" ', metric)

    def _set_metric(self, metric_name, metric_type, value, instance_tags):
        """
        Set a metric
        """
        if metric_type == GAUGE:
            self.gauge(metric_name, value, tags=instance_tags)

        elif metric_type == COUNTER:
            self.count(metric_name, value, tags=instance_tags)

        else:
            self.log.error('Unknown Metric Type: "%s"', metric_type)

    def timeout_event(self, url, timeout, aggregation_key):
        self.event(
            {
                'timestamp': int(time.time()),
                'event_type': 'http_check',
                'msg_title': 'URL timeout',
                'msg_text': '%s timed out after %s seconds.' % (url, timeout),
                'aggregation_key': aggregation_key,
            }
        )
