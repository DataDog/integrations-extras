# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib
import BaseHTTPServer
from nose.plugins.attrib import attr
from collections import namedtuple
import json
import os
import re
import requests
import time
import threading

# 3p
from mock import patch

# project
from tests.checks.common import AgentCheckTest, Fixtures


mocked_file_stats = namedtuple('mocked_file_stats', ['st_size', 'st_ino', 'st_dev'])


# allows mocking `os.stat` only for certain paths; for all others it will call
# the actual function - needed as a number of test helpers do make calls to it
def with_mocked_os_stat(mocked_paths_and_stats):
    vanilla_os_stat = os.stat

    def internal_mock(path):
        if path in mocked_paths_and_stats:
            return mocked_paths_and_stats[path]
        return vanilla_os_stat(path)

    def external_wrapper(function):
        # silly, but this _must_ start with `test_` for nose to pick it up as a
        # test when used below
        def test_wrapper(*args, **kwargs):
            with patch.object(os, 'stat') as patched_os_stat:
                patched_os_stat.side_effect = internal_mock
                return function(*args, **kwargs)
        return test_wrapper

    return external_wrapper


@attr(requires='filebeat')
class TestFilebeatBase(AgentCheckTest):
    '''Basic Test for filebeat integration.'''

    CHECK_NAME = 'filebeat'
    FIXTURE_DIR = os.path.join(os.path.dirname(__file__), 'ci')

    def _build_config(self, name, http_profiler=None):
        instance = {
            'registry_file_path': self.registry_file_path(name)
        }

        if http_profiler is not None:
            instance['http_profiler'] = http_profiler

        return {
            'init_config': None,
            'instances': [instance]
        }

    def registry_file_path(self, name):
        return Fixtures.file(name + '_registry.json', sdk_dir=self.FIXTURE_DIR)

    def assert_raises_with_message(self, config, expected_substring):
        with self.assertRaises(Exception) as context_manager:
            self.run_check(config)
        self.assertTrue(expected_substring in context_manager.exception.message)


class TestFilebeatRegistry(TestFilebeatBase):
    '''Tests the part parsing the registry file'''

    @with_mocked_os_stat({'/test_dd_agent/var/log/nginx/access.log': mocked_file_stats(394154, 277025, 51713),
                          '/test_dd_agent/var/log/syslog': mocked_file_stats(1024917, 152172, 51713)})
    def test_registry_happy_path(self):
        self.run_check(self._build_config('happy_path'))

        self.assertMetric('filebeat.registry.unprocessed_bytes', value=2407, tags=['source:/test_dd_agent/var/log/nginx/access.log'])
        self.assertMetric('filebeat.registry.unprocessed_bytes', value=0, tags=['source:/test_dd_agent/var/log/syslog'])

    # tests that we still support the format from filebeat < 5
    @with_mocked_os_stat({'/test_dd_agent/var/log/nginx/access.log': mocked_file_stats(394154, 277025, 51713),
                          '/test_dd_agent/var/log/syslog': mocked_file_stats(1024917, 152172, 51713)})
    def test_registry_happy_path_with_legacy_format(self):
        self.run_check(self._build_config('happy_path_legacy_format'))

        self.assertMetric('filebeat.registry.unprocessed_bytes', value=2407, tags=['source:/test_dd_agent/var/log/nginx/access.log'])
        self.assertMetric('filebeat.registry.unprocessed_bytes', value=0, tags=['source:/test_dd_agent/var/log/syslog'])

    def test_bad_config(self):
        bad_config = {
            'init_config': None,
            'instances': [{}]
        }
        self.assert_raises_with_message(bad_config, 'An absolute path to a filebeat registry path must be specified')

    def test_missing_registry_file(self):
        # tests that it simply silently ignores it
        self.run_check(self._build_config('i_dont_exist'))
        self.assertMetric('filebeat.registry.unprocessed_bytes', count=0)

    def test_missing_source_file(self):
        self.run_check(self._build_config('missing_source_file'))
        self.assertMetric('filebeat.registry.unprocessed_bytes', count=0)

    @with_mocked_os_stat({'/test_dd_agent/var/log/syslog': mocked_file_stats(1024917, 152171, 51713)})
    def test_source_file_inode_has_changed(self):
        self.run_check(self._build_config('single_source'))
        self.assertMetric('filebeat.registry.unprocessed_bytes', count=0)

    @with_mocked_os_stat({'/test_dd_agent/var/log/syslog': mocked_file_stats(1024917, 152172, 51714)})
    def test_source_file_device_has_changed(self):
        self.run_check(self._build_config('single_source'))
        self.assertMetric('filebeat.registry.unprocessed_bytes', count=0)


def generate_http_profiler_body(**kwargs):
    base_body = {
        'cmdline': ['/usr/share/filebeat/bin/filebeat', '-c', '/etc/filebeat/filebeat.yml', '-path.home', '/usr/share/filebeat', '-path.config', '/etc/filebeat', '-path.data', '/var/lib/filebeat', '-path.logs', '/var/log/filebeat', '-httpprof', ':2828'],
        'filebeat.harvester.closed': 108,
        'filebeat.harvester.files.truncated': 0,
        'filebeat.harvester.open_files': 10,
        'filebeat.harvester.running': 10,
        'filebeat.harvester.skipped': 0,
        'filebeat.harvester.started': 118,
        'filebeat.prospector.log.files.renamed': 0,
        'filebeat.prospector.log.files.truncated': 104,
        'libbeat.config.module.running': 0,
        'libbeat.config.module.starts': 0,
        'libbeat.config.module.stops': 0,
        'libbeat.config.reloads': 0,
        'libbeat.es.call_count.PublishEvents': 0,
        'libbeat.es.publish.read_bytes': 0,
        'libbeat.es.publish.read_errors': 0,
        'libbeat.es.publish.write_bytes': 0,
        'libbeat.es.publish.write_errors': 0,
        'libbeat.es.published_and_acked_events': 0,
        'libbeat.es.published_but_not_acked_events': 0,
        'libbeat.kafka.call_count.PublishEvents': 0,
        'libbeat.kafka.published_and_acked_events': 0,
        'libbeat.kafka.published_but_not_acked_events': 0,
        'libbeat.logstash.call_count.PublishEvents': 8691,
        'libbeat.logstash.publish.read_bytes': 52146,
        'libbeat.logstash.publish.read_errors': 0,
        'libbeat.logstash.publish.write_bytes': 161035867,
        'libbeat.logstash.publish.write_errors': 0,
        'libbeat.logstash.published_and_acked_events': 1138928,
        'libbeat.logstash.published_but_not_acked_events': 0,
        'libbeat.outputs.messages_dropped': 0,
        'libbeat.publisher.messages_in_worker_queues': 0,
        'libbeat.publisher.published_events': 1138928,
        'libbeat.redis.publish.read_bytes': 0,
        'libbeat.redis.publish.read_errors': 0,
        'libbeat.redis.publish.write_bytes': 0,
        'libbeat.redis.publish.write_errors': 0,
        'memstats': {'Alloc': 6561080, 'TotalAlloc': 24661290312, 'Sys': 25938232, 'Lookups': 35143, 'Mallocs': 86545328, 'Frees': 86527266, 'HeapAlloc': 6561080, 'HeapSys': 17006592, 'HeapIdle': 7553024, 'HeapInuse': 9453568, 'HeapReleased': 0, 'HeapObjects': 18062, 'StackInuse': 819200, 'StackSys': 819200, 'MSpanInuse': 129920, 'MSpanSys': 229376, 'MCacheInuse': 2400, 'MCacheSys': 16384, 'BuckHashSys': 1556137, 'GCSys': 2643968, 'OtherSys': 3666575, 'NextGC': 9491669, 'LastGC': 1520619692758256437, 'PauseTotalNs': 14387932504, 'PauseNs': [354477, 126296, 93752, 303703, 156045, 6939651, 107696, 115597, 110226, 87639]},
        'publish.events': 1139450,
        'registrar.states.cleanup': 0,
        'registrar.states.current': 151,
        'registrar.states.update': 1139450,
        'registrar.writes': 8690
    }

    base_body.update(kwargs)

    return base_body


class TestFilebeatHttpServerThread(threading.Thread):
    HOSTNAME = 'localhost'

    def __init__(self, profiler_body_kwargs, status_code=200, sleep_until_done=False):
        super(TestFilebeatHttpServerThread, self).__init__()
        self._should_stop = False
        self._stopped = False
        self._sleep_until_done = sleep_until_done

        thread = self
        profiler_body_kwargs_iterator = iter(profiler_body_kwargs)

        class MockFilebatHttpProfiler(BaseHTTPServer.BaseHTTPRequestHandler):
            def do_GET(self):
                if sleep_until_done:
                    while not thread._should_stop:
                        pass
                    return

                if self.path != '/debug/vars':
                    self.send_response(404)
                    return

                body = generate_http_profiler_body(**profiler_body_kwargs_iterator.next())

                self.send_response(status_code)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(body))
                self.wfile.close()

        self._http_server = BaseHTTPServer.HTTPServer((self.HOSTNAME, 0), MockFilebatHttpProfiler)

    @property
    def port(self):
        return self._http_server.server_port

    def run(self):
        while not self._should_stop:
            self._http_server.handle_request()
        self._stopped = True

    def stop(self):
        self._should_stop = True

        while not self._sleep_until_done and not self._stopped:
            try:
                # just a dummy get to wake it up
                requests.get('http://%s:%d' % (self.HOSTNAME, self.port), timeout=0.25)
            except Exception:
                pass


class TestFilebeatHttpProfilerBase(TestFilebeatBase):
    '''Base class for testing hitting Filebeat's HTTP profiler'''

    WITH_HTTP_SERVER = True
    HTTP_HOST = None
    DEFAULT_PORT = 9999
    ONLY_METRICS = None
    STATUS_CODE = 200
    HTTP_CLIENT_TIMEOUT = 0.01
    HTTP_SERVER_TIMING_OUT = False
    PROFILER_BODY_KWARGS = [{}]
    REGISTRY_NAME = 'empty'

    def _build_config(self, **extra_config):
        profiler_config = {
            'port': self.port,
            'timeout': self.HTTP_CLIENT_TIMEOUT
        }

        if self.HTTP_HOST:
            profiler_config['host'] = self.HTTP_HOST

        if self.ONLY_METRICS:
            profiler_config['only_metrics'] = self.ONLY_METRICS

        profiler_config.update(extra_config)

        return super(TestFilebeatHttpProfilerBase, self)._build_config(self.REGISTRY_NAME, profiler_config)

    def _expected_tags(self, port=None):
        if port is None:
            port = self.port

        return ['host:localhost', 'port:%s' % (port, )]

    @property
    def port(self):
        return self._http_server.port if self.WITH_HTTP_SERVER else self.DEFAULT_PORT

    def setUp(self):
        if self.WITH_HTTP_SERVER:
            self._http_server = TestFilebeatHttpServerThread(self.PROFILER_BODY_KWARGS, self.STATUS_CODE, self.HTTP_SERVER_TIMING_OUT)
            self._http_server.start()

    def tearDown(self):
        if self.WITH_HTTP_SERVER:
            self._http_server.stop()
            self._http_server.join()


class TestFilebeatHttpProfilerHappyPath(TestFilebeatHttpProfilerBase):

    PROFILER_BODY_KWARGS = [
        {},
        {'libbeat.logstash.published_and_acked_events': 1138956, 'filebeat.harvester.running': 9}
    ]

    def test_happy_path(self):
        config = self._build_config()

        # the first run shouldn't yield any increment metric, but it should
        # still report the gauge metrics
        self.run_check(config)
        self.assertMetric('libbeat.logstash.published_and_acked_events', count=0)
        self.assertMetric('filebeat.harvester.running', metric_type='gauge', value=10, tags=self._expected_tags())

        # now the second run should have all the increment metrics as well
        self.run_check(config)
        self.assertMetric('libbeat.logstash.published_and_acked_events', metric_type='rate', value=28, tags=self._expected_tags())
        self.assertMetric('libbeat.kafka.published_and_acked_events', metric_type='rate', value=0, tags=self._expected_tags())
        self.assertMetric('filebeat.harvester.running', metric_type='gauge', value=9, tags=self._expected_tags())


class TestFilebeatHttpProfilerWithAnOnlyMetricsList(TestFilebeatHttpProfilerBase):

    ONLY_METRICS = [r'^libbeat.kafka', r'truncated$']

    PROFILER_BODY_KWARGS = [
        {},
        {'libbeat.logstash.published_and_acked_events': 1138956, 'libbeat.kafka.published_and_acked_events': 12}
    ]

    def test_happy_path_with_an_only_metrics_list(self):
        self.run_check_twice(self._build_config())

        # these metrics shouldn't have been reported, because they don't match
        # any regex in the "only_metrics" list
        self.assertMetric('libbeat.logstash.published_and_acked_events', count=0)
        self.assertMetric('filebeat.harvester.running', count=0)

        # but these 4 should have
        self.assertMetric('libbeat.kafka.published_and_acked_events', metric_type='rate', value=12, tags=self._expected_tags())
        self.assertMetric('libbeat.kafka.published_but_not_acked_events', metric_type='rate', value=0, tags=self._expected_tags())
        self.assertMetric('libbeat.kafka.call_count.PublishEvents', metric_type='rate', value=0, tags=self._expected_tags())
        self.assertMetric('filebeat.harvester.files.truncated', metric_type='rate', value=0, tags=self._expected_tags())

    def test_with_an_invalid_regex_in_the_only_metrics_list(self):
        config_with_invalid_regex = self._build_config(only_metrics=['invalid regex ['])

        expected_message = 'Invalid only_metric regex for filebeat: "invalid regex [", error: unexpected end of regular expression'
        self.assert_raises_with_message(config_with_invalid_regex, expected_message)

    def test_regexes_only_get_compiled_and_run_once(self):
        regex = r'^libbeat.kafka'
        config = self._build_config(only_metrics=[regex])

        # the 1st run should compile regexes & run regexes
        with patch.object(re, 'compile') as re_compile:
            with patch.object(re, 'search') as re_search:
                self.run_check(config)

                re_compile.assert_called_once_with(regex)
                # once per metric name
                self.assertEqual(re_search.call_count, 41)

        # then let's run the check another 10 times
        with patch.object(re, 'compile') as re_compile:
            with patch.object(re, 'search') as re_search:
                for _ in range(10):
                    self.run_check(config)

                # no further regex compiling nor searching should have happened
                self.assertEqual(re_compile.call_count, 0)
                self.assertEqual(re_search.call_count, 0)


class TestFilebeatHttpProfilerWhenFilebeatRestarts(TestFilebeatHttpProfilerBase):

    PROFILER_BODY_KWARGS = [
        {},
        # Filebeat restarts here, so all counters go back to 0; but by the time
        # DD runs again, a dozen kafka events have been published & acked
        {'libbeat.logstash.published_and_acked_events': 0, 'libbeat.kafka.published_and_acked_events': 12},
        {'libbeat.logstash.published_and_acked_events': 28, 'libbeat.kafka.published_and_acked_events': 23}
    ]

    def test_when_filebeat_restarts(self):
        config = self._build_config()

        self.run_check_twice(config)

        # none of these metrics should have been reported, because of the restart
        self.assertMetric('libbeat.logstash.published_and_acked_events', count=0)
        self.assertMetric('libbeat.kafka.published_and_acked_events', count=0)

        # at the next run though, we should get normal increment from in between
        # the 2nd & 3rd runs
        self.run_check(config)
        self.assertMetric('libbeat.logstash.published_and_acked_events', metric_type='rate', value=28, tags=self._expected_tags())
        self.assertMetric('libbeat.kafka.published_and_acked_events', metric_type='rate', value=11, tags=self._expected_tags())


class TestFilebeatHttpProfilerWhenTheHttpCallErrorsOut(TestFilebeatHttpProfilerBase):

    STATUS_CODE = 500

    def test_when_the_http_call_times_out(self):
        self.run_check(self._build_config())
        self.assertMetric('filebeat.harvester.running', count=0)


class TestFilebeatHttpProfilerWhenTheHttpCallTimesOut(TestFilebeatHttpProfilerBase):

    HTTP_SERVER_TIMING_OUT = True

    def test_when_the_http_call_times_out(self):
        # it handles it gracefully, but does heed the timeout
        start_time = time.time()
        self.run_check(self._build_config())
        elapsed_time = time.time() - start_time

        self.assertTrue(elapsed_time < 10 * self.HTTP_CLIENT_TIMEOUT)
        self.assertMetric('filebeat.harvester.running', count=0)


class TestFilebeatHttpProfilerWhenTheHttpConnectionIsRefused(TestFilebeatHttpProfilerBase):

    WITH_HTTP_SERVER = False
    # an invalid IP
    HTTP_HOST = '0.28.28.28'

    def test_when_the_http_connection_is_refused(self):
        self.run_check(self._build_config())
        self.assertMetric('filebeat.harvester.running', count=0)


class TestFilebeatHttpProfilerWithTwoDifferentInstances(TestFilebeatHttpProfilerBase):

    PROFILER_BODY_KWARGS = [
        {},
        {'libbeat.logstash.published_and_acked_events': 1138956, 'filebeat.harvester.running': 9}
    ]

    SECOND_PROFILER_BODY_KWARGS = [
        {},
        {'libbeat.logstash.published_and_acked_events': 1238956, 'filebeat.harvester.running': 29}
    ]

    def _build_config(self):
        return {
            'init_config': None,
            'instances': [
                {
                    'registry_file_path': self.registry_file_path(self.REGISTRY_NAME),
                    'http_profiler': {
                        'port': self.port
                    }
                },
                {
                    'registry_file_path': self.registry_file_path(self.REGISTRY_NAME),
                    'http_profiler': {
                        'port': self._second_http_server.port,
                        'only_metrics': [r'events']
                    }
                }
            ]
        }

    def setUp(self):
        self._second_http_server = TestFilebeatHttpServerThread(self.SECOND_PROFILER_BODY_KWARGS)
        self._second_http_server.start()

        super(TestFilebeatHttpProfilerWithTwoDifferentInstances, self).setUp()

    def tearDown(self):
        self._second_http_server.stop()
        self._second_http_server.join()

        super(TestFilebeatHttpProfilerWithTwoDifferentInstances, self).tearDown()

    def test_with_two_different_instances(self):
        self.run_check_twice(self._build_config())

        # metrics for the first instance
        self.assertMetric('libbeat.logstash.published_and_acked_events', metric_type='rate', value=28, tags=self._expected_tags())
        self.assertMetric('libbeat.kafka.published_and_acked_events', metric_type='rate', value=0, tags=self._expected_tags())
        self.assertMetric('filebeat.harvester.running', metric_type='gauge', value=9, tags=self._expected_tags())

        # and for the second
        second_instance_tags = self._expected_tags(self._second_http_server.port)
        self.assertMetric('libbeat.logstash.published_and_acked_events', metric_type='rate', value=100028, tags=second_instance_tags)
        self.assertMetric('libbeat.kafka.published_and_acked_events', metric_type='rate', value=0, tags=second_instance_tags)
        self.assertMetric('filebeat.harvester.running', count=0, tags=second_instance_tags)


class TestFilebeatHttpProfilerWithInvalidConfigs(TestFilebeatBase):

    def _build_config(self, profiler_config):
        return super(TestFilebeatHttpProfilerWithInvalidConfigs, self)._build_config('empty', profiler_config)

    def _assert_config_raises(self, profiler_config, expected_substring):
        bad_config = self._build_config(profiler_config)
        self.assert_raises_with_message(bad_config, expected_substring)

    def test_http_profiler_not_a_dict(self):
        self._assert_config_raises(['port', 82], 'must be a dict')

    def test_port_absent(self):
        self._assert_config_raises({}, 'must be an integer')

    def test_port_not_an_int(self):
        self._assert_config_raises({'port': 'foo'}, 'must be an integer')

    def test_only_metrics_not_a_list(self):
        self._assert_config_raises({'port': 82, 'only_metrics': r'truncated$'}, 'must be a list of regexes')

    def test_timeout_not_a_number(self):
        self._assert_config_raises({'port': 82, 'timeout': '0.02'}, 'must be a positive number')

    def test_negative_timeout(self):
        self._assert_config_raises({'port': 82, 'timeout': 0}, 'must be a positive number')
        self._assert_config_raises({'port': 82, 'timeout': -0.5}, 'must be a positive number')
