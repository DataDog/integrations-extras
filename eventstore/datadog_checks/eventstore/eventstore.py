# (C) Calastone Ltd. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import json
import fnmatch
import re
import datetime
import copy

import requests

from datadog_checks.checks import AgentCheck
from datadog_checks.errors import CheckException
from .metrics import ALL_METRICS


class EventStoreCheck(AgentCheck):
    def check(self, instance):
        """ Main method """
        url = instance.get('url', '')
        default_timeout = instance.get('default_timeout', 5)
        timeout = float(instance.get('timeout', default_timeout))
        tag_by_url = instance.get('tag_by_url', False)
        name_tag = instance.get('name', url)
        metric_def = copy.deepcopy(ALL_METRICS)
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
        self.log.debug("Event Store Paths:")
        self.log.debug(eventstore_paths)

        # Flaten the self.init_config definitions into valid metric definitions
        metric_definitions = {}
        for metric in metric_def:
            self.log.debug("metric {}".format(metric))
            json_path = metric.get('json_path', '')
            self.log.debug("json_path {}".format(json_path))
            tags = metric.get('tag_by', {})
            self.log.debug("tags {}".format(tags))
            paths = self.get_json_path(json_path, eventstore_paths)
            self.log.debug("paths {}".format(paths))
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
            self.log.debug("metric: {}".format(metric))
            paths = self.get_json_path(metric, eventstore_paths)
            self.log.debug("paths: {}".format(paths))
            for path in paths:
                self.log.debug("path: {}".format(path))
                try:
                    metrics_to_check[path] = metric_definitions[path]
                    self.log.debug("metrics_to_check: {}".format(metric_definitions[path]))
                except KeyError:
                    self.log.info("Skipping metric: {} as it is not defined".format(path))

        # Now we need to get the metrics from the endpoint
        # Get the value for a given key
        self.log.debug("parsed_api:")
        self.log.debug(parsed_api)
        for key, metric in metrics_to_check.items():
            value = self.get_value(parsed_api, metric['json_path'])
            value = self.convert_value(value, metric)
            if value is not None:
                self.dispatch_metric(value, metric)
            else:
                # self.dispatch_metric(0, metric)
                self.log.debug("Metric {} did not return a value, skipping".format(metric['json_path']))
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
        self.log.debug("json paths: {}".format(json_path))
        self.log.debug("eventstore_paths: {}".format(eventstore_paths))
        response = []
        self.log.debug("response: {}".format(response))
        try:
            match = eventstore_paths.index(json_path)
            self.log.debug("match: {}".format(match))
            if match is not None:
                response.append(json_path)
                self.log.debug("match json path: {}".format(json_path))
        except ValueError:
            # Loop through all possible keys to find matches
            # Value Error means it didn't find it, so it must be
            # a wildcard
            self.log.debug("value error")
            for path in eventstore_paths:
                self.log.debug("path: {}".format(path))
                match = fnmatch.fnmatch(path, json_path)
                self.log.debug("match ve: {}".format(match))
                if match:
                    response.append(path)
                    self.log.debug("path ve: {}".format(path))
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
