# (C) Calastone Ltd. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

# system
import json
import fnmatch
import re
import datetime
import copy

# project
from datadog_checks.checks import AgentCheck
from datadog_checks.errors import CheckException
# 3rd Party
import requests


class EventStoreCheck(AgentCheck):
    def check(self, instance):
        """ Main method """
        url = instance.get('url', '')
        default_timeout = instance.get('default_timeout', 5)
        timeout = float(instance.get('timeout', default_timeout))
        tag_by_url = instance.get('tag_by_url', False)
        name_tag = instance.get('name', url)
        metric_def = copy.deepcopy(self.get_metric_definitions())
        try:
            r = requests.get(url, timeout=timeout)
        except requests.exceptions.Timeout as e:
            raise CheckException('URL: {0} timed out after {1} seconds.'.format(url, timeout))
        except requests.exceptions.MissingSchema as e:
            raise CheckException(e)
        except requests.exceptions.ConnectionError as e:
            raise CheckException(e)
        # Bad HTTP code
        if r.status_code != 200:
            raise CheckException('Invalid Status Code, {0} returned a status of {1}.'.format(url, r.status_code))
        # Unable to deserialize the returned data
        try:
            parsed_api = json.loads(r.text)
        except ValueError as e:
            raise CheckException('{0} returned an unserializable payload'.format(url))

        eventstore_paths = None
        eventstore_paths = self.walk(parsed_api)

        # Flaten the self.init_config definitions into valid metric definitions
        metric_definitions = {}
        for metric in metric_def:
            json_path = metric.get('json_path', '')
            tags = metric.get('tag_by', {})
            paths = self.get_json_path(json_path, eventstore_paths)
            for path in paths:
                # Deep copy needed else it will overwrite previous metric data
                metric_builder = copy.deepcopy(metric)
                metric_builder['json_path'] = path
                tag_builder = []
                if tag_by_url:
                    tag_builder.append('instance:{}'.format(url))
                tag_builder.append('name:{}'.format(name_tag))
                for tag in tags:
                    tag_path = self.get_tag_path(tag, path, eventstore_paths)
                    tag_name = self.format_tag(tag_path.split('.')[-1])
                    tag_value = self.get_value(parsed_api, tag_path)
                    tag_builder.append('{}:{}'.format(tag_name, tag_value))
                metric_builder['tag_by'] = tag_builder
                metric_definitions[path] = metric_builder

        # Find metrics to check:
        metrics_to_check = {}
        for metric in instance['json_path']:
            paths = self.get_json_path(metric, eventstore_paths)
            for path in paths:
                try:
                    metrics_to_check[path] = metric_definitions[path]
                except KeyError:
                    self.log.info("Skipping metric: {} as it is not defined".format(path))

        # Now we need to get the metrics from the endpoint
        # Get the value for a given key
        for key, metric in metrics_to_check.items():
            value = self.get_value(parsed_api, metric['json_path'])
            value = self.convert_value(value, metric)
            if value is not None:
                self.dispatch_metric(value, metric)
            else:
                print("Metric {} did not return a value, skipping".format(metric['json_path']))
                self.log.info("Metric {} did not return a value, skipping".format(metric['json_path']))

    def format_tag(self, name):
        "Converts the string to snake case from camel case"
        # https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def walk(self, json_obj, p=[], es_paths=[]):
        """ Walk a JSON tree and return the json paths in a list """
        for key, value in json_obj.items():
            if isinstance(value, dict):
                # We add the instance to the path global variable to build up a map
                p.append(key)
                self.walk(value)
                # Once we have finished with this path we remove it from the global variable
                p.pop()
            else:
                p.append(key)
                tmp = "{}".format(".".join(p))
                p.pop()
                # Add the full key name to the "flat" global variable
                if tmp not in es_paths:
                    es_paths.append(tmp)
        return es_paths

    def get_tag_path(self, tag, metric_json_path, eventstore_paths):
        """ Returns the paths for the given tags """
        # This function will return the tag as a validated path,
        # if the tag has a wildcard it will return
        try:
            # Wildcard
            tag_split = tag.split('.')
            wildcard_index = tag.split('.').index('*')
            json_path_split = metric_json_path.split('.')
            tag_split[wildcard_index] = json_path_split[wildcard_index]
            tag_path = '.'.join(tag_split)
            return self.get_json_path(tag_path, eventstore_paths)[0]
        except ValueError:
            # No wildcard
            return self.get_json_path(tag, eventstore_paths)[0]
        except IndexError:
            self.log.warn('No tag value found for {}, path {}'.format(tag, metric_json_path))

    def get_json_path(self, json_path, eventstore_paths):
        """ Find all the possible keys for a given path """
        response = []
        try:
            match = eventstore_paths.index(json_path)
            if match:
                response.append(json_path)
        except ValueError:
            # Loop through all possible keys to find matches
            # Value Error means it didn't find it, so it must be
            # a wildcard
            for path in eventstore_paths:
                match = fnmatch.fnmatch(path, json_path)
                if match:
                    response.append(path)
        return response
    # Fill out eventstore_paths using walk of json

    def get_value(self, dictionary, metric_path, index=0):
        """ Returns the value for the supplied metric path """
        split = metric_path.split('.')
        key = split[index]
        try:
            v = dictionary[key]
            if isinstance(v, dict):
                index += 1
                v = self.get_value(v, metric_path, index=index)
            else:
                v = str(v)
            if len(v) == 0:
                v = 'N/A'
            return v
        except KeyError:
            self.log.info('No value found for Metric: {}'.format(metric_path))
            return None

    def convert_value(self, value, metric):
        """ Returns the metric formatted in the specified value"""
        data_type = metric['json_type']
        v = None
        if data_type == 'float':
            try:
                v = float(value)
            except ValueError:
                v = None
        elif data_type == 'int':
            try:
                v = int(value)
            except ValueError:
                v = None
        elif data_type == 'datetime':
            dt = self.convert_to_timedelta(value)
            if dt:
                v = float(dt.total_seconds())
            else:
                v = float(0)
            # Convert to MS
        return v

    def convert_to_timedelta(self, string):
        """
        Returns a time delta for strings in a format of: 0:00:00:00.0000
        Using RegEx to not introduce a dependancy on another package
        """
        dt_re = re.compile(r'^(\d+)\:(\d\d):(\d\d):(\d\d).(\d+)$')
        tmp = dt_re.match(string)
        try:
            days = self._regex_number_to_int(tmp, 1)
            hours = self._regex_number_to_int(tmp, 2)
            mins = self._regex_number_to_int(tmp, 3)
            secs = self._regex_number_to_int(tmp, 4)
            subsecs = self._regex_number_to_int(tmp, 5)
            td = datetime.timedelta(days=days, seconds=secs, microseconds=subsecs, minutes=mins, hours=hours)
            return td
        except AttributeError:
            self.log.info('Unable to convert {} to timedelta'.format(string))
            return None
        except TypeError:
            self.log.info('Unable to convert {} to type timedelta'.format(string))
            return None

    def _regex_number_to_int(self, number, group_index):
        """ Returns the number for the group or 0 """
        try:
            return int(number.group(group_index)) or 0
        except AttributeError:
            return 0

    def dispatch_metric(self, value, metric):
        """ Formats the metric into the correct type with relevant tags"""
        metric_type = metric['metric_type']
        tags = metric['tag_by']
        metric_name = metric['metric_name']
        if metric_type == 'gauge':
            self.log.debug("Sending gauge {} v: {} t: {}".format(metric_name, value, tags))
            self.gauge(metric_name, value, tags)
        elif metric_type == 'histogram':
            self.log.debug("Sending histogram {} v: {} t: {}".format(metric_name, value, tags))
            self.histogram(metric_name, value, tags)
        else:
            self.log.info('Unable to send metric {} due to invalid metric type of {}'.format(metric_name, metric_type))

    def get_metric_definitions(self):
        """ Returns the metric definitions """
        metric_definitions = []
        # json_path: path in the json to the metric, seperated by a period (.)
        #   This can contain a wilcard at any level except the last level
        #   It can only contain a single wildcard however
        # json_type: the data type stored in the json, valid values are:
        #   int, float, datetime (this will be converted to ms)
        # metric_name: the name of the metric to be sent to datadog
        # metric_type: the type of metric to send to datadog, valid values are:
        #   gauge, histogram
        # tag_by: any additional tags to add to the metric, wilcards are only
        # supported for looking at itself,
        # eg: es.queue.*.queueName for subscriptions will resolve to es.queue.subscriptions.queueName
        # this must be specified on each metric you wish to tag.
        metric_definitions.append({
          "json_path": "proc.mem",
          "json_type": "int",
          "metric_name": "eventstore.proc.mem",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.cpu",
          "json_type": "float",
          "metric_name": "eventstore.proc.cpu",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.cpuScaled",
          "json_type": "float",
          "metric_name": "eventstore.proc.cpu_scaled",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.threadsCount",
          "json_type": "int",
          "metric_name": "eventstore.proc.threads",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.contentionsRate",
          "json_type": "float",
          "metric_name": "eventstore.proc.contentions_rate",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.thrownExceptionsRate",
          "json_type": "float",
          "metric_name": "eventstore.proc.thrown_exceptions_rate",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.diskIo.readBytes",
          "json_type": "int",
          "metric_name": "eventstore.proc.disk.read_bytes",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.diskIo.writtenBytes",
          "json_type": "int",
          "metric_name": "eventstore.proc.disk.write_bytes",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.diskIo.readOps",
          "json_type": "int",
          "metric_name": "eventstore.proc.disk.read_ops",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.diskIo.writeOps",
          "json_type": "int",
          "metric_name": "eventstore.proc.disk.write_ops",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.tcp.connections",
          "json_type": "int",
          "metric_name": "eventstore.tcp.connections",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.tcp.receivingSpeed",
          "json_type": "float",
          "metric_name": "eventstore.tcp.receiving_speed",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.tcp.sendingSpeed",
          "json_type": "float",
          "metric_name": "eventstore.tcp.sending_speed",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.tcp.inSend",
          "json_type": "int",
          "metric_name": "eventstore.tcp.in_send",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.tcp.measureTime",
          "json_type": "datetime",
          "metric_name": "eventstore.tcp.measure_time",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.tcp.pendingReceived",
          "json_type": "int",
          "metric_name": "eventstore.tcp.pending_received",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.tcp.pendingSend",
          "json_type": "int",
          "metric_name": "eventstore.tcp.pending_send",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.tcp.receivedBytesSinceLastRun",
          "json_type": "int",
          "metric_name": "eventstore.tcp.received_bytes.since_last_run",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.tcp.receivedBytesTotal",
          "json_type": "int",
          "metric_name": "eventstore.tcp.received_bytes.total",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.tcp.sentBytesSinceLastRun",
          "json_type": "int",
          "metric_name": "eventstore.tcp.sent_bytes.since_last_run",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.tcp.sentBytesTotal",
          "json_type": "int",
          "metric_name": "eventstore.tcp.sent_bytes.total",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.gc.allocationSpeed",
          "json_type": "float",
          "metric_name": "eventstore.gc.allocation_speed",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.gc.gen0ItemsCount",
          "json_type": "float",
          "metric_name": "eventstore.gc.items_count.gen0",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.gc.gen0Size",
          "json_type": "float",
          "metric_name": "eventstore.gc.size.gen0",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.gc.gen1ItemsCount",
          "json_type": "float",
          "metric_name": "eventstore.gc.items_count.gen1",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.gc.gen1Size",
          "json_type": "float",
          "metric_name": "eventstore.gc.size.gen1",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.gc.gen2ItemsCount",
          "json_type": "float",
          "metric_name": "eventstore.gc.items_count.gen2",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.gc.gen2Size",
          "json_type": "float",
          "metric_name": "eventstore.gc.size.gen2",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.gc.largeHeapSize",
          "json_type": "int",
          "metric_name": "eventstore.gc.large_heap_size",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.gc.timeInGc",
          "json_type": "float",
          "metric_name": "eventstore.gc.time_in_gc",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "proc.gc.totalBytesInHeaps",
          "json_type": "int",
          "metric_name": "eventstore.gc.total_bytes_in_heaps",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "sys.cpu",
          "json_type": "float",
          "metric_name": "eventstore.sys.cpu",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "sys.freeMem",
          "json_type": "int",
          "metric_name": "eventstore.sys.free_mem",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "es.queue.*.avgItemsPerSecond",
          "json_type": "int",
          "metric_name": "eventstore.es.queue.avg_items_per_second",
          "metric_type": "histogram",
          "tag_by": [
            "es.queue.*.queueName",
            "es.queue.*.groupName"
          ]
        })
        metric_definitions.append({
          "json_path": "es.queue.*.avgProcessingTime",
          "json_type": "float",
          "metric_name": "eventstore.es.queue.avg_processing_time",
          "metric_type": "histogram",
          "tag_by": [
            "es.queue.*.queueName",
            "es.queue.*.groupName"
          ]
        })
        metric_definitions.append({
          "json_path": "es.queue.*.currentIdleTime",
          "json_type": "datetime",
          "metric_name": "eventstore.es.queue.current_idle_time",
          "metric_type": "gauge",
          "tag_by": [
            "es.queue.*.queueName",
            "es.queue.*.groupName"
          ]
        })
        metric_definitions.append({
          "json_path": "es.queue.*.currentItemProcessingTime",
          "json_type": "datetime",
          "metric_name": "eventstore.es.queue.current_processing_time",
          "metric_type": "gauge",
          "tag_by": [
            "es.queue.*.queueName",
            "es.queue.*.groupName"
          ]
        })
        metric_definitions.append({
          "json_path": "es.queue.*.idleTimePercent",
          "json_type": "float",
          "metric_name": "eventstore.es.queue.idle_time_percent",
          "metric_type": "gauge",
          "tag_by": [
            "es.queue.*.queueName",
            "es.queue.*.groupName"
          ]
        })
        metric_definitions.append({
          "json_path": "es.queue.*.length",
          "json_type": "int",
          "metric_name": "eventstore.es.queue.length",
          "metric_type": "histogram",
          "tag_by": [
            "es.queue.*.queueName",
            "es.queue.*.groupName"
          ]
        })
        metric_definitions.append({
          "json_path": "es.queue.*.lengthCurrentTryPeak",
          "json_type": "int",
          "metric_name": "eventstore.es.queue.length_current_try_peak",
          "metric_type": "gauge",
          "tag_by": [
            "es.queue.*.queueName",
            "es.queue.*.groupName"
          ]
        })
        metric_definitions.append({
          "json_path": "es.queue.*.lengthLifetimePeak",
          "json_type": "int",
          "metric_name": "eventstore.es.queue.length_lifetime_peak",
          "metric_type": "gauge",
          "tag_by": [
            "es.queue.*.queueName",
            "es.queue.*.groupName"
          ]
        })
        metric_definitions.append({
          "json_path": "es.queue.*.totalItemsProcessed",
          "json_type": "int",
          "metric_name": "eventstore.es.queue.total_items_processed",
          "metric_type": "gauge",
          "tag_by": [
            "es.queue.*.queueName",
            "es.queue.*.groupName"
          ]
        })
        metric_definitions.append({
          "json_path": "es.writer.lastFlushSize",
          "json_type": "int",
          "metric_name": "eventstore.es.writer.flush_size.last",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "es.writer.lastFlushDelayMs",
          "json_type": "float",
          "metric_name": "eventstore.es.writer.flush_delay_ms.last",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "es.writer.meanFlushSize",
          "json_type": "int",
          "metric_name": "eventstore.es.writer.flush_size.mean",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "es.writer.meanFlushDelayMs",
          "json_type": "float",
          "metric_name": "eventstore.es.writer.flush_delay_ms.mean",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "es.writer.maxFlushSize",
          "json_type": "int",
          "metric_name": "eventstore.es.writer.flush_size.max",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "es.writer.maxFlushDelayMs",
          "json_type": "float",
          "metric_name": "eventstore.es.writer.flush_delay_ms.max",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "es.writer.queuedFlushMessages",
          "json_type": "int",
          "metric_name": "eventstore.es.writer.queued_flush_messages",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "es.readIndex.cachedRecord",
          "json_type": "int",
          "metric_name": "eventstore.es.read_index.cached_record",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "es.readIndex.notCachedRecord",
          "json_type": "int",
          "metric_name": "eventstore.es.read_index.not_cached_record",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "es.readIndex.cachedStreamInfo",
          "json_type": "int",
          "metric_name": "eventstore.es.read_index.cached_stream_info",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "es.readIndex.notCachedStreamInfo",
          "json_type": "int",
          "metric_name": "eventstore.es.read_index.not_cached_stream_info",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "es.readIndex.cachedTransInfo",
          "json_type": "int",
          "metric_name": "eventstore.es.read_index.cached_trans_info",
          "metric_type": "gauge"
        })
        metric_definitions.append({
          "json_path": "es.readIndex.notCachedTransInfo",
          "json_type": "int",
          "metric_name": "eventstore.es.read_index.not_cached_trans_info",
          "metric_type": "gauge"
        })
        return metric_definitions
