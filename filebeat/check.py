# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib
import collections
import errno
import numbers
import os
import re
import sre_constants

# 3rd party
import requests
import simplejson

# project
from datadog_checks.checks import AgentCheck
from datadog_checks.utils.containers import hash_mutable


EVENT_TYPE = SOURCE_TYPE_NAME = 'filebeat'


class FilebeatCheckHttpProfiler(object):
    '''
    Filebeat's HTTP profiler gives a bunch of counter variables; their value holds little interest,
    what we really want is the delta in between runs. This class is responsible for caching the
    values from the previous run
    '''

    INCREMENT_METRIC_NAMES = [
        'filebeat.harvester.closed',
        'filebeat.harvester.files.truncated',
        'filebeat.harvester.open_files',
        'filebeat.harvester.skipped',
        'filebeat.harvester.started',
        'filebeat.prospector.log.files.renamed',
        'filebeat.prospector.log.files.truncated',
        'libbeat.config.module.running',
        'libbeat.config.module.starts',
        'libbeat.config.module.stops',
        'libbeat.config.reloads',
        'libbeat.es.call_count.PublishEvents',
        'libbeat.es.publish.read_bytes',
        'libbeat.es.publish.read_errors',
        'libbeat.es.publish.write_bytes',
        'libbeat.es.publish.write_errors',
        'libbeat.es.published_and_acked_events',
        'libbeat.es.published_but_not_acked_events',
        'libbeat.kafka.call_count.PublishEvents',
        'libbeat.kafka.published_and_acked_events',
        'libbeat.kafka.published_but_not_acked_events',
        'libbeat.logstash.call_count.PublishEvents',
        'libbeat.logstash.publish.read_bytes',
        'libbeat.logstash.publish.read_errors',
        'libbeat.logstash.publish.write_bytes',
        'libbeat.logstash.publish.write_errors',
        'libbeat.logstash.published_and_acked_events',
        'libbeat.logstash.published_but_not_acked_events',
        'libbeat.output.events.dropped',
        'libbeat.output.events.failed',
        'libbeat.pipeline.events.dropped',
        'libbeat.pipeline.events.failed',
        'libbeat.publisher.messages_in_worker_queues',
        'libbeat.publisher.published_events',
        'libbeat.redis.publish.read_bytes',
        'libbeat.redis.publish.read_errors',
        'libbeat.redis.publish.write_bytes',
        'libbeat.redis.publish.write_errors',
        'publish.events',
        'registrar.states.cleanup',
        'registrar.states.current',
        'registrar.states.update',
        'registrar.writes'
    ]

    GAUGE_METRIC_NAMES = [
        'filebeat.harvester.running'
    ]

    VARS_ROUTE = 'debug/vars'

    def __init__(self, config):
        self._config = config
        self._previous_increment_values = {}
        # regex matching ain't free, let's cache this
        self._should_keep_metrics = {}

    def gather_metrics(self):
        response = self._make_request()

        return {
            'increment': self._gather_increment_metrics(response),
            'gauge': self._gather_gauge_metrics(response)
        }

    def _make_request(self):

        response = requests.get(self._config.stats_endpoint, timeout=self._config.timeout)
        response.raise_for_status()

        return self.flatten(response.json())

    def _gather_increment_metrics(self, response):
        new_values = {name: response[name] for name in self.INCREMENT_METRIC_NAMES
                      if self._should_keep_metric(name) and name in response}

        deltas = self._compute_increment_deltas(new_values)

        self._previous_increment_values = new_values

        return deltas

    def _compute_increment_deltas(self, new_values):
        deltas = {}

        for name, new_value in new_values.iteritems():
            if name not in self._previous_increment_values \
                    or self._previous_increment_values[name] > new_value:
                # either the agent or filebeat got restarted, we're not
                # reporting anything this time around
                return {}
            deltas[name] = new_value - self._previous_increment_values[name]

        return deltas

    def _gather_gauge_metrics(self, response):
        return {name: response[name] for name in self.GAUGE_METRIC_NAMES
                if self._should_keep_metric(name) and name in response}

    def _should_keep_metric(self, name):
        if name not in self._should_keep_metrics:
            self._should_keep_metrics[name] = self._config.should_keep_metric(name)
        return self._should_keep_metrics[name]

    def flatten(self, d, parent_key='', sep='.'):
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, collections.MutableMapping):
                items.extend(self.flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)


class FilebeatCheckInstanceConfig(object):

    def __init__(self, instance):
        self._registry_file_path = instance.get('registry_file_path')
        if self._registry_file_path is None:
            raise Exception('An absolute path to a filebeat registry path must be specified')

        self._stats_endpoint = instance.get('stats_endpoint')

        self._only_metrics = instance.get('only_metrics', [])
        if not isinstance(self._only_metrics, list):
            raise Exception("If given, filebeat's only_metrics must be a list of regexes, got %s" % (
                self._only_metrics, ))

        self._timeout = instance.get('timeout', 2)
        if not isinstance(self._timeout, numbers.Real) or self._timeout <= 0:
            raise Exception("If given, filebeats timeout must be a positive number, got %s" % (self._timeout, ))

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
        try:
            return self._only_metrics_regexes
        except AttributeError:
            self._only_metrics_regexes = self._compile_regexes()
            return self._compiled_regexes()

    def _compile_regexes(self):
        compiled_regexes = []

        for regex in self._only_metrics:
            try:
                compiled_regexes.append(re.compile(regex))
            except sre_constants.error as ex:
                raise Exception(
                    'Invalid only_metric regex for filebeat: "%s", error: %s' % (regex, ex))

        return compiled_regexes


class FilebeatCheck(AgentCheck):

    def __init__(self, *args, **kwargs):
        AgentCheck.__init__(self, *args, **kwargs)
        self.instance_cache = {}

    def check(self, instance):
        instance_key = hash_mutable(instance)
        if instance_key in self.instance_cache:
            config = self.instance_cache['config']
            profiler = self.instance_cache['profiler']
        else:
            self.instance_cache['config'] = config = FilebeatCheckInstanceConfig(instance)
            self.instance_cache['profiler'] = profiler = FilebeatCheckHttpProfiler(config)

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
                return simplejson.load(registry_file)
        except IOError as ex:
            self.log.error('Cannot read the registry log file at %s: %s' % (registry_file_path, ex))

            if ex.errno == errno.EACCES:
                self.log.error('You might be interesting in having a look at https://github.com/elastic/beats/pull/6455')

            return []

    def _process_registry_item(self, item):
        source = item['source']
        offset = item['offset']

        try:
            stats = os.stat(source)

            if self._is_same_file(stats, item['FileStateOS']):
                unprocessed_bytes = stats.st_size - offset

                self.gauge('filebeat.registry.unprocessed_bytes', unprocessed_bytes,
                           tags=['source:{0}'.format(source)])
            else:
                self.log.debug("Filebeat source %s appears to have changed" % (source, ))
        except OSError:
            self.log.debug("Unable to get stats on filebeat source %s" % (source, ))

    def _is_same_file(self, stats, file_state_os):
        return stats.st_dev == file_state_os['device'] and stats.st_ino == file_state_os['inode']

    def _gather_http_profiler_metrics(self, config, profiler):
        try:
            all_metrics = profiler.gather_metrics()
        except StandardError as ex:
            self.log.error('Error when fetching metrics from %s: %s' % (config.stats_endpoint, ex))
            return

        tags = ['stats_endpoint:{0}'.format(config.stats_endpoint)]

        for action, metrics in all_metrics.iteritems():
            method = getattr(self, action)

            for name, value in metrics.iteritems():
                method(name, value, tags)
