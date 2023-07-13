#!python3

# Upbound Universal Crossplane DataDog Integration

# This integration monitors Upbound Universal Crossplane
# and provider Kubernetes pods.

import json
import logging
import os
import re
import subprocess
import sys

import requests
from kubernetes import client, config
from prometheus_client.parser import text_string_to_metric_families

from datadog_checks.base import AgentCheck, ConfigurationError

from .__about__ import __version__

# Agent Behavior
#
# When no metrics are specified, a predefined min set is used and
# there are no pod annotations required for the Crossplane and Provider
# pods.
#
# None, Min and More metrics sets can receive additions from the
# metrics section in the DataDog configurations yaml file.
#
# When pod annotations are not ignored, they will be preferred and
# overwrite any other metrics selections.

# Prometheus parser indexes
NAME_IDX = 0
LABEL_IDX = 1
VALUE_IDX = 2

# Upbound predefined metric set categories
METRICS_DEFAULTS = ['none', 'min', 'more', 'max']

# Upbound minimum default recommended set of metrics
# This will be used if no metrics are defined in the
# DataDog config yaml file and if there are no pod
# annotations for the Universal Crossplane and provider
# pods.
METRICS_DEFAULT_MIN_SET = [
    # Upjet provider Terraform CLI invocations
    'upjet_terraform_active_cli_invocations',
    # Upjet provider Terraform running processes
    'upjet_terraform_running_processes',
    # Total number of reconciliations per controller
    'controller_runtime_reconcile_total',
    # Number of goroutines that currently exist.
    'go_goroutines',
    # Number of bytes allocated and still in use.
    'go_memstats_alloc_bytes',
    # Number of bytes allocated and still in use.
    'go_memstats_alloc_bytes_total',
    # Total user and system CPU time spent in seconds.
    'process_cpu_seconds_total',
    # Resident memory size in bytes.
    'process_resident_memory_bytes',
    # Start time of the process since unix epoch in seconds.
    'process_start_time_seconds',
    # Number of HTTP requests,
    # partitioned by status code, method, and host.
    'rest_client_requests_total',
    # Total number of adds handled by workqueue.
    'workqueue_adds_total',
    # Current depth of workqueue.
    'workqueue_depth',
    # How long in seconds processing
    # an item from workqueue takes
    'workqueue_work_duration_seconds_bucket',
    'workqueue_work_duration_seconds_count',
    'workqueue_work_duration_seconds_sum',
]

# Upbound recommended set of metrics
METRICS_DEFAULT_MORE_SET = [
    # Upjet provider Terraform CLI duration
    'upjet_terraform_cli_duration',
    # Upjet provider Terraform resource time to reconcile
    'upjet_resource_ttr',
    # Total number of certificate read errors
    'certwatcher_read_certificate_errors_total',
    # Total number of certificate reads
    'certwatcher_read_certificate_total',
    # Number of currently used workers per controller
    'controller_runtime_active_workers',
    # Maximum number of concurrent reconciles per controller
    'controller_runtime_max_concurrent_reconciles',
    # Total number of reconciliation errors per controller
    'controller_runtime_reconcile_errors_total',
    # Length of time per reconciliation per controller
    'controller_runtime_reconcile_time_seconds_bucket',
    'controller_runtime_reconcile_time_seconds_count',
    'controller_runtime_reconcile_time_seconds_sum',
    'controller_runtime_active_workers',
    'controller_runtime_max_concurrent_reconciles',
    'controller_runtime_reconcile_errors_total',
    'controller_runtime_reconcile_time_seconds_bucket',
    'controller_runtime_reconcile_time_seconds_count',
    'controller_runtime_reconcile_time_seconds_sum',
    'controller_runtime_reconcile_total',
    # A summary of the pause duration of garbage collection cycles.
    'go_gc_duration_seconds',
    'go_gc_duration_seconds_count',
    'go_gc_duration_seconds_sum',
    # Information about the Go environment.
    'go_info',
    # Number of bytes used by the profiling bucket hash table.
    'go_memstats_buck_hash_sys_bytes',
    # Total number of frees.
    'go_memstats_frees_total',
    # Number of bytes used for garbage collection system metadata.
    'go_memstats_gc_sys_bytes',
    # Number of heap bytes allocated and still in use.
    'go_memstats_heap_alloc_bytes',
    # Number of heap bytes waiting to be used.
    'go_memstats_heap_idle_bytes',
    # Number of heap bytes that are in use.
    'go_memstats_heap_inuse_bytes',
    # Number of allocated objects.
    'go_memstats_heap_objects',
    # Number of heap bytes released to OS.
    'go_memstats_heap_released_bytes',
    # Number of heap bytes obtained from system.
    'go_memstats_heap_sys_bytes',
    # Number of seconds since 1970 of last garbage collection.
    'go_memstats_last_gc_time_seconds',
    # Total number of pointer lookups.
    'go_memstats_lookups',
    # Total number of mallocs.
    'go_memstats_mallocs',
    # Number of bytes in use by mcache structures.
    'go_memstats_mcache_inuse_bytes',
    # Number of bytes used for mcache structures obtained from system.
    'go_memstats_mcache_sys_bytes',
    # Number of bytes in use by mspan structures.
    'go_memstats_mspan_inuse_bytes',
    # Number of bytes used for mspan structures obtained from system.
    'go_memstats_mspan_sys_bytes',
    # Number of heap bytes when next garbage collection will take place.
    'go_memstats_next_gc_bytes',
    # Number of bytes used for other system allocations.
    'go_memstats_other_sys_bytes',
    # Number of bytes in use by the stack allocator.
    'go_memstats_stack_inuse_bytes',
    # Number of bytes obtained from system for stack allocator.
    'go_memstats_stack_sys_bytes',
    # Number of bytes obtained from system.
    'go_memstats_sys_bytes',
    # Number of OS threads created.
    'go_threads',
    # Gauge of if the reporting system is master
    # of the relevant lease, 0 indicates backup,
    # 1 indicates master. 'name' is the string used
    # to identify the lease. Please make sure to group by name
    'leader_election_master_status',
    # Maximum number of open file descriptors.
    'process_max_fds',
    # Number of open file descriptors.
    'process_open_fds',
    # Virtual memory size in bytes.
    'process_virtual_memory_bytes',
    # Maximum amount of virtual memory available in bytes.
    'process_virtual_memory_max_bytes',
    # How many seconds has the longest running
    # processor for workqueue been running.
    'workqueue_longest_running_processor_seconds',
    # How long in seconds an item stays
    # in workqueue before being requested.
    'workqueue_queue_duration_seconds_bucket',
    'workqueue_queue_duration_seconds_count',
    'workqueue_queue_duration_seconds_sum',
    # Total number of retries handled by workqueue.
    'workqueue_retries_total',
    # How many seconds of work has been done
    # that is in progress and hasn't been observed
    # by work_duration. Large values indicate stuck
    # threads. One can deduce the number of stuck
    # threads by observing the rate at which this increases.
    'workqueue_unfinished_work_seconds',
]


class UpboundUxpCheck(AgentCheck):
    """
    UpboundUXPCheck is a class to scrape Upbound's
    Universal Crossplane and its Provider Kubernetes Pods

    Minimal example configuration:

    ```
    init_config:

    instances: |
        [
            {
                "uxp_url": "/metrics",
                "uxp_port": "8080",
                # print useful info when verbose is true
                "verbose": true,
                # kubernetes namespace to check for
                # uxp and provider containers
                "namespace": "upbound-system",
                # metric could be collected as often
                # as min_collection_interval
                "min_collection_interval": 30,
                # default is unlimited
                "metrics_limit": 60000,
                # select from a predefined set of metrics:
                # none, min, more, max
                "metrics_default": "min",
                # conf file flag to ignore otherwise
                # superseding pod annotations
                "metrics_ignore_pod_annotations": false
                # prefix that will be inserted between uxp.
                # and (mapped) metric name
                "metrics_prefix":
                # metrics examples below will be added to default,
                # but pod annotations overwrite
                "metrics": [
                    {"go_goroutines": "company_prefix_go_goroutines"},
                    # only one value needed without
                    # name mapping requirements
                    {"go_memstats_heap_alloc_bytes"},
                ]
            }
        ]
    ```
    """

    SERVICE_CHECK_CONNECT_NAME = 'upbound_uxp.can_connect'

    # Prefix of every metric and service check that
    # the upbound-uxp integration sends
    __NAMESPACE__ = 'uxp'
    DEFAULT_METRIC_LIMIT = 0

    # Read agent configuration and initialize it
    def __init__(self, name, init_config, instances):
        self.log = logging.getLogger("Upbound UXP")
        self.log.info("DataDog Upbound Universal Crossplane Integration")

        if instances is not None:
            for instance in instances:
                self.verbose = instance.get('verbose')
                if self.verbose is None:
                    self.verbose = False
                else:
                    self._raise_if_type_err(self.verbose, 'verbose', 'bool')

                self.uxp_url = instance.get('uxp_url')
                if self.uxp_url is None:
                    self.uxp_url = '/metrics'
                else:
                    self._raise_if_type_err(self.uxp_url, 'uxp_url', 'str')
                if not self.uxp_url.startswith('/'):
                    self._raise_format_err('uxp_url', 'Expected it to start with /.')

                self.uxp_port = instance.get('uxp_port')
                if self.uxp_port is None:
                    self.uxp_port = '8080'
                else:
                    self._raise_if_type_err(self.uxp_port, 'uxp_port', 'str')

                self.namespace = instance.get('namespace')
                if self.namespace is None:
                    self.namespace = 'upbound-system'
                else:
                    self._raise_if_type_err(self.namespace, 'namespace', 'str')

                self.check_count = 0

                if instance.get('metrics_limit') is not None:
                    DEFAULT_METRIC_LIMIT = instance.get('metrics_limit')
                    self._raise_if_type_err(DEFAULT_METRIC_LIMIT, 'DEFAULT_METRIC_LIMIT', 'int')

                self.metrics_conf = instance.get('metrics')
                if self.metrics_conf is None:
                    self.metrics_conf = []
                else:
                    self._raise_if_type_err(self.metrics_conf, 'metrics', 'list')

                self.metrics_prefix = instance.get('metrics_prefix')
                if self.metrics_prefix is None:
                    self.metrics_prefix = ''
                else:
                    self._raise_if_type_err(self.metrics_prefix, 'metrics_prefix', 'str')

                self.metrics_ignore_pod_annotations = instance.get('metrics_ignore_pod_annotations')
                if self.metrics_ignore_pod_annotations is None:
                    self.metrics_ignore_pod_annotations = True
                else:
                    self._raise_if_type_err(
                        self.metrics_ignore_pod_annotations, 'metrics_ignore_pod_annotations', 'bool'
                    )

                self.metrics_default = instance.get('metrics_default')
                if self.metrics_default is None:
                    self.metrics_default = 'min'

                if self.metrics_default not in METRICS_DEFAULTS:
                    self.metrics_default = 'min'

                # Determine which exposed metrics to observe and
                # feed into DataDog. Note, this will work without
                # pod annotations.

                self.metrics_set = []
                self.metrics_map = {}
                if self.metrics_default == 'min':
                    self.metrics_set = METRICS_DEFAULT_MIN_SET
                elif self.metrics_default == 'more':
                    self.metrics_set = METRICS_DEFAULT_MIN_SET
                    self.metrics_set.extend(METRICS_DEFAULT_MORE_SET)

                # No metrics set is needed to compare against
                # when collecting the max or none.

                self.metrics_set = self._merge_conf()
                if self.verbose:
                    self.log.debug(self.metrics_set)

        super(UpboundUxpCheck, self).__init__(name, init_config, instances)

    def _raise_format_err(self, n, msg):
        raise ConfigurationError(
            'Configuration error, ' + 'Please fix format for ' + n + ' in auto_conf.yaml and/or conf.yaml. ' + msg
        )

    def _raise_if_type_err(self, v, n, t):
        str_type = re.sub('<class \'', '', str(type(v)))
        str_type = re.sub('\'>$', '', str_type)
        if str_type != t:
            raise ConfigurationError(
                'Configuration error, '
                + 'Please fix type error for '
                + n
                + ' key value in auto_conf.yaml and/or conf.yaml. '
                + 'Expected '
                + t
                + ' and received '
                + str_type
                + ' in auto_conf and/or conf.yaml.'
            )

    # Convert Prometheus labels to DataDog tags
    # and add a tag for the pod name where the
    # metrics originate from.

    def _labels_to_tags(self, labels, pod_name):
        tags = []
        for k in labels:
            v = labels[k]
            if '=' in v:
                v = re.sub('=', ":", v)
                new_kv = re.sub('.+?(, )', '', v)
                tags.append(new_kv)
                v = re.sub(', .*$', '', v)
            tags.append(k + ":" + v)
        tags.append("pod:" + pod_name)
        return tags

    # Merge metrics from DataDog agent config
    # to a selected default set.

    def _merge_conf(self):
        m = []
        if self.metrics_conf is not None:
            for metric in self.metrics_conf:
                for k in metric:
                    if k not in m:
                        m.append(k)
                        if type(k) == 'int':
                            if metric[k] is not None:
                                self.metrics_map[k] = metric[k]

        for metric in self.metrics_set:
            if metric not in m:
                m.append(metric)

        return m

    def _merge_annotations(self, annotations, pod_name):
        if self.metrics_ignore_pod_annotations:
            return self.metrics_set

        key_match_start = 'ad.datadoghq.com/uxp.' + pod_name
        m = []
        if annotations is not None:
            for key in annotations:
                if key.endswith('.instances'):
                    match_key = re.sub('.instances$', '', key)
                    if key_match_start.startswith(match_key):
                        # Don't crash the agent when the pod
                        # annotation is invalid
                        try:
                            annotations_json = json.loads(annotations[key])
                            for annotation in annotations_json:
                                for metric in annotation["metrics"]:
                                    for k in metric:
                                        if k not in m:
                                            m.append(k)
                                            if metric[k] is not None:
                                                self.metrics_map[k] = metric[k]
                        except Exception as e:
                            self.log.exception(e)
                            continue

        # When there are no pod annotations, use the default metrics set
        if len(m) == 0:
            return self.metrics_set

        # Pod annotation supersede defaults unless explicitly ignored
        # through DataDog conf.yaml metrics_ignore_pod_annotations
        return m

    def check(self, instance):
        incluster = True

        self.count('datadog_agent_checks', self.check_count, ['agent_integration_version=' + __version__])
        self.check_count = self.check_count + 1

        # Get Pods in upbound-system or another namespace
        # is overwritten in the upbound_uxp (auth_conf.yaml)
        # config file
        try:
            if 'KUBERNETES_SERVICE_HOST' not in os.environ and 'KUBERNETES_SERVICE_PORT' not in os.environ:
                incluster = False
                config.load_kube_config("/tmp/uxp.kubeconfig")
            else:
                config.load_incluster_config()
        except Exception as e:
            # Without the config, we will not be
            # able to get pods and their metrics

            self.service_check(
                self.SERVICE_CHECK_CONNECT_NAME, self.CRITICAL, message="Error {0}".format(e), tags=None, hostname=None
            )
            raise

            return

        self.service_check(self.SERVICE_CHECK_CONNECT_NAME, self.OK, message=None, tags=None, hostname=None)

        v1 = client.CoreV1Api()
        pods = []
        try:
            pods = v1.list_namespaced_pod(self.namespace)
        except Exception as e:
            # There can be an exception if the agent is not
            # allowed to list the pods. Verify that the
            # apiserver-cluster-role, and a role binding
            # for the agent service have been configured.

            self.log.error("\nUnable to list pods. Please check the apiserver cluster role configuration.\n")
            self.log.exception(e)
            sys.stdout.flush()
            return

        port_forward_target = 8080
        for pod in pods.items:
            # Get Pod annotations to overwrite config file and
            # default metric set. If no pod annotations are present
            # then the upbound_uxp (auto_conf.yaml) config file
            # determines the metrics to scrape. If no metrics
            # selection is included in the config file, then
            # the minimum default is selected automatically.

            self.metrics_set = self._merge_annotations(pod.metadata.annotations, pod.metadata.name)
            metrics_map_keys = self.metrics_map.keys()
            metrics_prefix = ''
            if self.metrics_prefix is not None:
                if len(self.metrics_prefix) > 0:
                    metrics_prefix = self.metrics_prefix + '.'
            if self.verbose:
                self.log.debug("Observing metrics set")
                self.log.debug(self.metrics_set)
                self.log.debug("Mapping metrics names")
                self.log.debug(self.metrics_map)

            metrics = ''
            try:
                if not incluster:
                    port_forward_target_str = str(port_forward_target)
                    cmd1 = 'kubectl --kubeconfig /tmp/uxp.kubeconfig '
                    cmd2 = '-n upbound-system port-forward '
                    cmd3 = 'pods/' + pod.metadata.name + ' '
                    cmd4 = port_forward_target_str + ':' + self.uxp_port
                    cmd = cmd1 + cmd2 + cmd3 + cmd4
                    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
                    port_forward_info = p.stdout.readline()
                    if self.verbose:
                        self.log.debug(port_forward_info)
                    response = requests.get('http://localhost:' + port_forward_target_str + self.uxp_url)
                    metrics = response.text
                    p.terminate()
                else:
                    response = requests.get('http://' + pod.status.pod_ip + ':' + self.uxp_port + self.uxp_url)
                    metrics = response.text
            except Exception as e:
                # We were unable to get metrics for this pod.
                # Let's continue with the next one.

                self.log.exception(e)
                sys.stdout.flush()
                self.service_check(
                    self.SERVICE_CHECK_CONNECT_NAME,
                    self.CRITICAL,
                    message="Error {0}".format(e),
                    tags=None,
                    hostname=pod.status.pod_ip,
                )
                continue

            metric_type = ''
            for line in metrics.split('\n'):
                if line.startswith('#'):
                    # Determine metrics type based on info
                    # in the metrics feed, example format is
                    # TYPE workqueue_work_duration_seconds histogram
                    if line.startswith('# TYPE'):
                        try:
                            metric_type = line.split(' ')[3]
                        except Exception as e:
                            self.log.exception(e)
                            metric_type = ''

                    # Continue to metrics line
                    continue

                for family in text_string_to_metric_families(line):
                    for sample in family.samples:
                        name = sample[NAME_IDX]
                        tags = self._labels_to_tags(sample[LABEL_IDX], pod.metadata.name)
                        value = sample[VALUE_IDX]

                        if self.metrics_default != 'max' and name not in self.metrics_set:
                            continue

                        if name in metrics_map_keys:
                            if self.verbose:
                                self.log.debug("Sending metric: %s as: %s", name, self.metrics_map[name])
                            name = self.metrics_map[name]
                        name = metrics_prefix + name

                        if name.endswith('sum'):
                            metric_type = 'summary'
                        if name.endswith('count'):
                            metric_type = 'counter'
                        if name.endswith('bucket'):
                            metric_type = 'histogram'

                        # counter: _total
                        if metric_type == 'counter':
                            if self.verbose:
                                self.log.debug("%s: Name: %s, Tags: %s, Value: %s", metric_type, name, tags, str(value))
                            try:
                                self.count(name, value, tags=tags)
                            except Exception as e:
                                self.log.exception(e)
                        # histogram: _bucket
                        elif metric_type == 'histogram':
                            if self.verbose:
                                self.log.debug("%s: Name: %s, Tags: %s, Value: %s", metric_type, name, tags, str(value))
                            try:
                                self.histogram(name, value, tags=tags)
                            except Exception as e:
                                self.log.exception(e)
                        # summary: _sum
                        elif metric_type == 'summary':
                            if self.verbose:
                                self.log.debug(
                                    "%s: Name: %s, Labels: %s, Value: %s", metric_type, name, tags, str(value)
                                )
                            try:
                                self.count(name, value, tags=tags)
                            except Exception as e:
                                self.log.exception(e)
                        # gauge: no _bucket, _sum, _total postfix
                        elif metric_type == 'gauge':
                            if self.verbose:
                                self.log.debug("%s: Name: %s, Tags: %s, Value: %s", metric_type, name, tags, str(value))
                            try:
                                self.gauge(name, value, tags=tags)
                            except Exception as e:
                                self.log.exception(e)
                        else:
                            self.log.warning("WARNING: metric type %s unknown for %s", metric_type, name)
