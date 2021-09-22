# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib
import errno
import json
import os
import re
import sre_constants

import six
from six import iteritems

from datadog_checks.base import AgentCheck, is_affirmative
from datadog_checks.base.utils.containers import hash_mutable

if six.PY3:
    from collections.abc import MutableMapping
else:
    from collections import MutableMapping

EVENT_TYPE = SOURCE_TYPE_NAME = "filebeat"


class FilebeatCheckHttpProfiler:
    """
    Filebeat's HTTP profiler gives a bunch of counter variables; their value holds little interest,
    what we really want is the delta in between runs. This class is responsible for caching the
    values from the previous run
    """

    INCREMENT_METRIC_NAMES = [
        "filebeat.events.done",
        "filebeat.harvester.closed",
        "filebeat.harvester.files.truncated",
        "filebeat.harvester.open_files",
        "filebeat.harvester.skipped",
        "filebeat.harvester.started",
        "filebeat.prospector.log.files.renamed",
        "filebeat.prospector.log.files.truncated",
        "libbeat.config.module.running",
        "libbeat.config.module.starts",
        "libbeat.config.module.stops",
        "libbeat.config.reloads",
        "libbeat.es.call_count.PublishEvents",
        "libbeat.es.publish.read_bytes",
        "libbeat.es.publish.read_errors",
        "libbeat.es.publish.write_bytes",
        "libbeat.es.publish.write_errors",
        "libbeat.es.published_and_acked_events",
        "libbeat.es.published_but_not_acked_events",
        "libbeat.kafka.call_count.PublishEvents",
        "libbeat.kafka.published_and_acked_events",
        "libbeat.kafka.published_but_not_acked_events",
        "libbeat.logstash.call_count.PublishEvents",
        "libbeat.logstash.publish.read_bytes",
        "libbeat.logstash.publish.read_errors",
        "libbeat.logstash.publish.write_bytes",
        "libbeat.logstash.publish.write_errors",
        "libbeat.logstash.published_and_acked_events",
        "libbeat.logstash.published_but_not_acked_events",
        "libbeat.output.events.acked",
        "libbeat.output.events.dropped",
        "libbeat.output.events.failed",
        "libbeat.output.events.total",
        "libbeat.pipeline.events.dropped",
        "libbeat.pipeline.events.failed",
        "libbeat.pipeline.events.filtered",
        "libbeat.pipeline.events.published",
        "libbeat.pipeline.events.total",
        "libbeat.publisher.messages_in_worker_queues",
        "libbeat.publisher.published_events",
        "libbeat.redis.publish.read_bytes",
        "libbeat.redis.publish.read_errors",
        "libbeat.redis.publish.write_bytes",
        "libbeat.redis.publish.write_errors",
        "publish.events",
        "registrar.states.cleanup",
        "registrar.states.current",
        "registrar.states.update",
        "registrar.writes",
    ]

    GAUGE_METRIC_NAMES = ["filebeat.harvester.running"]

    VARS_ROUTE = "debug/vars"

    def __init__(self, config, http):
        self._config = config
        self._http = http
        self._previous_increment_values = {}
        # regex matching ain't free, let's cache this
        self._should_keep_metrics = {}

    def gather_metrics(self):
        if not self._config.stats_endpoint:
            return {}

        response = self._make_request()

        return {"increment": self._gather_increment_metrics(response), "gauge": self._gather_gauge_metrics(response)}

    def _make_request(self):

        response = self._http.get(self._config.stats_endpoint)
        response.raise_for_status()

        return self.flatten(response.json())

    def _gather_increment_metrics(self, response):
        new_values = {
            name: response[name]
            for name in self.INCREMENT_METRIC_NAMES
            if self._should_keep_metric(name) and name in response
        }

        deltas = self._compute_increment_deltas(new_values)

        self._previous_increment_values = new_values

        return deltas

    def _compute_increment_deltas(self, new_values):
        deltas = {}

        for name, new_value in iteritems(new_values):
            if name not in self._previous_increment_values or self._previous_increment_values[name] > new_value:
                # either the agent or filebeat got restarted, we're not
                # reporting anything this time around
                return {}
            deltas[name] = new_value - self._previous_increment_values[name]

        return deltas

    def _gather_gauge_metrics(self, response):
        return {
            name: response[name]
            for name in self.GAUGE_METRIC_NAMES
            if self._should_keep_metric(name) and name in response
        }

    def _should_keep_metric(self, name):
        if name not in self._should_keep_metrics:
            self._should_keep_metrics[name] = self._config.should_keep_metric(name)
        return self._should_keep_metrics[name]

    def flatten(self, d, parent_key="", sep="."):
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, MutableMapping):
                items.extend(self.flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)


class FilebeatCheckInstanceConfig:

    _only_metrics_regexes = None

    def __init__(self, instance):
        self._registry_file_path = instance.get("registry_file_path")
        if self._registry_file_path is None:
            raise Exception("An absolute path to a filebeat registry path must be specified")

        self._stats_endpoint = instance.get("stats_endpoint")

        self._only_metrics = instance.get("only_metrics", [])

        self._ignore_registry = instance.get("ignore_registry", False)

        if not isinstance(self._only_metrics, list):
            raise Exception(
                "If given, filebeat's only_metrics must be a list of regexes, got %s" % (self._only_metrics,)
            )

    @property
    def registry_file_path(self):
        return self._registry_file_path

    @property
    def stats_endpoint(self):
        return self._stats_endpoint

    @property
    def ignore_registry(self):
        return self._ignore_registry

    def should_keep_metric(self, metric_name):

        if not self._only_metrics:
            return True

        return any(re.search(regex, metric_name) for regex in self._compiled_regexes())

    def _compiled_regexes(self):
        if self._only_metrics_regexes is None:
            self._only_metrics_regexes = self._compile_regexes()
        return self._only_metrics_regexes

    def _compile_regexes(self):
        compiled_regexes = []

        for regex in self._only_metrics:
            try:
                compiled_regexes.append(re.compile(regex))
            except sre_constants.error as ex:
                raise Exception('Invalid only_metric regex for filebeat: "%s", error: %s' % (regex, ex))

        return compiled_regexes


class FilebeatCheck(AgentCheck):

    SERVICE_CHECK_NAME = 'can_connect'

    __NAMESPACE__ = "filebeat"

    def __init__(self, *args, **kwargs):
        AgentCheck.__init__(self, *args, **kwargs)
        self.instance_cache = {}
        self.tags = []

        if self.instance:
            self.tags = self.instance.get('tags', [])
            # preserve backwards compatible default timeouts
            if self.instance.get('timeout') is None:
                if self.init_config.get('timeout') is None:
                    self.instance['timeout'] = 2

    def check(self, instance):
        normalize_metrics = is_affirmative(instance.get("normalize_metrics", False))

        instance_key = hash_mutable(instance)
        if instance_key in self.instance_cache:
            config = self.instance_cache[instance_key]["config"]
            profiler = self.instance_cache[instance_key]["profiler"]
        else:
            config = FilebeatCheckInstanceConfig(instance)
            profiler = FilebeatCheckHttpProfiler(config, self.http)
            self.instance_cache[instance_key] = {"config": config, "profiler": profiler}

        if not config.ignore_registry:
            self._process_registry(config)

        self._gather_http_profiler_metrics(config, profiler, normalize_metrics)

    def _process_registry(self, config):
        registry_contents = self._parse_registry_file(config.registry_file_path)

        if isinstance(registry_contents, dict):
            # filebeat version < 5
            registry_contents = registry_contents.values()

        for item in registry_contents:
            self._process_registry_item(item)

    def _parse_registry_file(self, registry_file_path):
        try:
            with open(registry_file_path) as registry_file:
                return json.load(registry_file)
        except IOError as ex:
            self.log.error("Cannot read the registry log file at %s: %s", registry_file_path, ex)

            if ex.errno == errno.EACCES:
                self.log.error(
                    "You might be interesting in having a look at " "https://github.com/elastic/beats/pull/6455"
                )

            return []

    def _process_registry_item(self, item):
        source = item["source"]
        offset = item["offset"]
        tags = self.tags + ["source:{0}".format(source)]

        try:
            stats = os.stat(source)

            if self._is_same_file(stats, item["FileStateOS"]):
                unprocessed_bytes = stats.st_size - offset

                self.gauge("registry.unprocessed_bytes", unprocessed_bytes, tags=tags)
            else:
                self.log.debug("Filebeat source %s appears to have changed", source)
        except OSError:
            self.log.debug("Unable to get stats on filebeat source %s", source)

    def _is_same_file(self, stats, file_state_os):
        return stats.st_dev == file_state_os["device"] and stats.st_ino == file_state_os["inode"]

    def _gather_http_profiler_metrics(self, config, profiler, normalize_metrics):
        tags = self.tags + ["stats_endpoint:{0}".format(config.stats_endpoint)]
        try:
            all_metrics = profiler.gather_metrics()
        except Exception as ex:
            self.log.error("Error when fetching metrics from %s: %s", config.stats_endpoint, ex)
            self.service_check(
                self.SERVICE_CHECK_NAME,
                AgentCheck.CRITICAL,
                message="Error {0} when hitting {1}".format(ex, config.stats_endpoint),
            )
            return

        for action, metrics in iteritems(all_metrics):
            method = getattr(self, action)

            for name, value in iteritems(metrics):
                if not name.startswith(self.__NAMESPACE__) and normalize_metrics:
                    method(name, value, tags)
                else:
                    method(name, value, tags, raw=True)
        self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.OK, tags=tags)
