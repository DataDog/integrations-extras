# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib
import collections
import errno
import json
import numbers
import os
import re
import sre_constants

import requests
from six import iteritems

from datadog_checks.base import AgentCheck
from datadog_checks.utils.containers import hash_mutable

EVENT_TYPE = SOURCE_TYPE_NAME = "filebeat"


class FilebeatCheckHttpProfiler:
    """
    Filebeat's HTTP profiler gives a bunch of counter variables; their value holds little interest,
    what we really want is the delta in between runs. This class is responsible for caching the
    values from the previous run
    """

    INCREMENT_METRIC_NAMES = [
        'beat.info.uptime.ms',
        'beat.memstats.rss',
        'beat.memstats.gc_next',
        'beat.memstats.memory_total',
        'beat.memstats.memory_alloc',
        'beat.handles.open',
        'beat.handles.limit.hard',
        'beat.handles.limit.soft',
        'beat.cpu.total.ticks',
        'beat.cpu.total.value',
        'beat.cpu.total.time.ms',
        'beat.cpu.system.ticks',
        'beat.cpu.system.time.ms',
        'beat.cpu.user.ticks',
        'beat.cpu.user.time.ms',
        'filebeat.input.log.files.renamed',
        'filebeat.input.log.files.truncated',
        'filebeat.events.active',
        'filebeat.events.added',
        'filebeat.events.done',
        'registrar.states.current',
        'registrar.states.cleanup',
        'registrar.states.update',
        'registrar.writes.fail',
        'registrar.writes.total',
        'registrar.writes.success',
        'system.load.1',
        'system.load.5',
        'system.load.15',
        'system.load.norm.1',
        'system.load.norm.5',
        'system.load.norm.15',
        'system.cpu.cores',
        'libbeat.output.read.errors',
        'libbeat.output.read.bytes',
        'libbeat.output.write.errors',
        'libbeat.output.write.bytes',
        'libbeat.output.events.batches',
        'libbeat.output.events.duplicates',
        'libbeat.output.events.acked',
        'libbeat.output.events.failed',
        'libbeat.output.events.dropped',
        'libbeat.output.events.active',
        'libbeat.output.events.total',
        'libbeat.pipeline.queue.acked',
        'libbeat.pipeline.clients',
        'libbeat.pipeline.events.retry',
        'libbeat.pipeline.events.failed',
        'libbeat.pipeline.events.dropped',
        'libbeat.pipeline.events.published',
        'libbeat.pipeline.events.active',
        'libbeat.pipeline.events.filtered',
        'libbeat.pipeline.events.total',
        'libbeat.config.reloads',
        'libbeat.config.module.starts',
        'libbeat.config.module.running',
        'libbeat.config.module.stops'
   ]

    GAUGE_METRIC_NAMES = [
        'filebeat.harvester.started',
        'filebeat.harvester.open_files',
        'filebeat.harvester.skipped',
        'filebeat.harvester.running',
        'filebeat.harvester.closed',
        'filebeat.harvester.running'
    ]

    VARS_ROUTE = "debug/vars"

    def __init__(self, config):
        self._config = config
        self._previous_increment_values = {}
        # regex matching ain't free, let's cache this
        self._should_keep_metrics = {}

    def gather_metrics(self):
        if not self._config.stats_endpoint:
            return {}

        response = self._make_request()

        return {"count": self._gather_increment_metrics(response), "gauge": self._gather_gauge_metrics(response)}

    def _make_request(self):

        response = requests.get(self._config.stats_endpoint, timeout=self._config.timeout)
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
            if isinstance(v, collections.MutableMapping):
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
        if not isinstance(self._only_metrics, list):
            raise Exception(
                "If given, filebeat's only_metrics must be a list of regexes, got %s" % (self._only_metrics,)
            )

        self._timeout = instance.get("timeout", 2)
        if not isinstance(self._timeout, numbers.Real) or self._timeout <= 0:
            raise Exception("If given, filebeats timeout must be a positive number, got %s" % (self._timeout,))

    @property
    def registry_file_path(self):
        return self._registry_file_path

    @property
    def stats_endpoint(self):
        return self._stats_endpoint

    @property
    def timeout(self):
        return self._timeout

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
    def __init__(self, *args, **kwargs):
        AgentCheck.__init__(self, *args, **kwargs)
        self._previous_offset = {}
        self.instance_cache = {}

    def check(self, instance):
        instance_key = hash_mutable(instance)
        if instance_key in self.instance_cache:
            config = self.instance_cache[instance_key]["config"]
            profiler = self.instance_cache[instance_key]["profiler"]
        else:
            config = FilebeatCheckInstanceConfig(instance)
            profiler = FilebeatCheckHttpProfiler(config)
            self.instance_cache[instance_key] = {"config": config, "profiler": profiler}

        self._process_registry(config)
        self._gather_http_profiler_metrics(config, profiler)

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
            self.log.error("Cannot read the registry log file at %s: %s" % (registry_file_path, ex))

            if ex.errno == errno.EACCES:
                self.log.error(
                    "You might be interesting in having a look at " "https://github.com/elastic/beats/pull/6455"
                )

            return []

    def _check_offset(self, source, offset):
        if source not in self._previous_offset or self._previous_offset[source] >= offset:
                return {}
        new_offset = offset - self._previous_offset[source]
        return new_offset

    def _process_registry_item(self, item):
        source = item["source"]
        offset = item["offset"]

        try:
            stats = os.stat(source)
            if self._is_same_file(stats, item["FileStateOS"]):
                delta = self._check_offset(source, offset)
                self._previous_offset[source] = offset
                unprocessed_bytes = stats.st_size - offset
                self.gauge("filebeat.registry.unprocessed_bytes", unprocessed_bytes, tags=["source:{0}".format(source)])
                if delta:
                        self.count("filebeat.registry.offset", delta, tags=["source:{0}".format(source)])
            else:
                self.log.debug("Filebeat source %s appears to have changed" % (source,))
        except OSError:
            self.log.debug("Unable to get stats on filebeat source %s" % (source,))

    def _is_same_file(self, stats, file_state_os):
        return stats.st_dev == file_state_os["device"] and stats.st_ino == file_state_os["inode"]

    def _gather_http_profiler_metrics(self, config, profiler):
        try:
            all_metrics = profiler.gather_metrics()
        except Exception as ex:
            self.log.error("Error when fetching metrics from %s: %s" % (config.stats_endpoint, ex))
            return

        tags = ["stats_endpoint:{0}".format(config.stats_endpoint)]

        for action, metrics in iteritems(all_metrics):
            method = getattr(self, action)

            for name, value in iteritems(metrics):
                method(name, value, tags)
