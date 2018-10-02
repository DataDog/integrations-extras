# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib
import errno
import numbers
import os
import re
import sre_constants

# 3rd party
import requests
import simplejson

# project
from checks import AgentCheck


EVENT_TYPE = SOURCE_TYPE_NAME = 'filebeat'


class FilebeatCheckHttpProfilerInstanceConfig(object):
    def __init__(self, http_profiler):
        if not isinstance(http_profiler, dict):
            raise Exception("If given, filebeat's http_profiler config must be a dict, got %s" % (http_profiler, ))

        self._port = http_profiler.get('port')
        if not isinstance(self._port, int):
            raise Exception("Filebeat's http_profiler's port must be an integer, got %s" % (self._port, ))

        self._host = http_profiler.get('host', 'localhost')

        self._only_metrics = http_profiler.get('only_metrics', [])
        if not isinstance(self._only_metrics, list):
            raise Exception("If given, filebeat's http_profiler only_metrics must be a list of regexes, got %s" % (self._only_metrics, ))

        self._timeout = http_profiler.get('timeout', 2)
        if not isinstance(self._timeout, numbers.Real) or self._timeout <= 0:
            raise Exception("If given, filebeat's http_profiler's timeout must be a positive number, got %s" % (self._timeout, ))

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def timeout(self):
        return self._timeout

    @property
    def socket_address(self):
        return '%s:%s' % (self._host, self._port)

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
                raise Exception('Invalid only_metric regex for filebeat: "%s", error: %s' % (regex, ex))

        return compiled_regexes


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
        'libbeat.outputs.messages_dropped',
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

    def __init__(self, http_profiler_config):
        self._config = http_profiler_config
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
        url = 'http://%s/%s' % (self._config.socket_address, self.VARS_ROUTE)

        response = requests.get(url, timeout=self._config.timeout)
        response.raise_for_status()

        return response.json()

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


class FilebeatCheckInstanceConfig(object):

    def __init__(self, instance):
        self._registry_file_path = instance.get('registry_file_path')
        if self._registry_file_path is None:
            raise Exception('An absolute path to a filebeat registry path must be specified')

        self._http_profiler = instance.get('http_profiler')
        if self._http_profiler is not None:
            self._http_profiler = FilebeatCheckHttpProfilerInstanceConfig(self._http_profiler)

    @property
    def registry_file_path(self):
        return self._registry_file_path

    @property
    def http_profiler(self):
        return self._http_profiler


class FilebeatCheck(AgentCheck):

    def __init__(self, *args, **kwargs):
        AgentCheck.__init__(self, *args, **kwargs)
        self._http_profilers = {}

    def check(self, instance):
        config = FilebeatCheckInstanceConfig(instance)
        self._process_registry(config)
        self._process_http_profiler(config)

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

    def _process_http_profiler(self, config):
        profiler_config = config.http_profiler
        if profiler_config is None:
            return

        socket_addresss = profiler_config.socket_address
        if socket_addresss not in self._http_profilers:
            self._http_profilers[socket_addresss] = FilebeatCheckHttpProfiler(profiler_config)
        profiler = self._http_profilers[socket_addresss]

        self._gather_http_profiler_metrics(profiler, profiler_config)

    def _gather_http_profiler_metrics(self, profiler, profiler_config):
        try:
            all_metrics = profiler.gather_metrics()
        except StandardError as ex:
            self.log.error('Error when fetching metrics from %s: %s' % (profiler_config.socket_address, ex))
            return

        tags = ['host:{0}'.format(profiler_config.host), 'port:{0}'.format(profiler_config.port)]

        for action, metrics in all_metrics.iteritems():
            method = getattr(self, action)

            for name, value in metrics.iteritems():
                method(name, value, tags)
