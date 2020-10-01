# (C) Calastone Ltd. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import copy
import datetime
import fnmatch
import re
from collections import defaultdict

import requests

from datadog_checks.base import AgentCheck
from datadog_checks.base.errors import CheckException

from .metrics import ALL_METRICS


class EventStoreCheck(AgentCheck):
    def check(self, instance):
        """ Main method """
        endpoints_def = instance.get('endpoints')
        if not endpoints_def:
            raise CheckException('The list of metric endpoints is empty')
        if not isinstance(endpoints_def, (list, tuple)):
            raise CheckException('Incorrect value specified for the list of metric endpoints')

        metric_def = self.init_config.get('metric_definitions', ALL_METRICS)
        for endpoint in endpoints_def:
            metrics = metric_def.get(endpoint)
            if metrics is None:
                raise CheckException('Unknown metric endpoint: {}'.format(endpoint))
            self.check_endpoint(instance, endpoint, metrics)

    def check_endpoint(self, instance, endpoint, metrics):
        """ Process metrics from an API endpoint """
        base_url = instance.get('url', '')
        url = base_url + endpoint
        default_timeout = instance.get('default_timeout', 5)
        timeout = float(instance.get('timeout', default_timeout))
        tag_by_url = instance.get('tag_by_url', False)
        name_tag = instance.get('name', url)
        metric_def = copy.deepcopy(metrics)
        # Requests defaults to True, which causes Requests to use the certifi CA bundle
        verify_bundle = instance.get('ca_bundle', True)

        user = instance.get('user')
        password = instance.get('password')
        if user is None or password is None:
            auth = None
        else:
            auth = (user, password)
            self.log.debug('Authenticating as: %s', user)
        try:
            r = requests.get(url, timeout=timeout, auth=auth, verify=verify_bundle)
        except requests.exceptions.Timeout:
            raise CheckException('URL: {} timed out after {} seconds.'.format(url, timeout))
        except requests.exceptions.MissingSchema as e:
            raise CheckException(e)
        except requests.exceptions.ConnectionError as e:
            raise CheckException(e)
        # Bad HTTP code
        if r.status_code != 200:
            raise CheckException('Invalid Status Code, {} returned a status of {}.'.format(url, r.status_code))
        # Unable to deserialize the returned data
        try:
            parsed_api = r.json()
        except Exception as e:
            raise CheckException('{} returned an unserializable payload: {}'.format(url, e))

        eventstore_paths = self.walk(parsed_api)
        self.log.debug("Event Store Paths:")
        self.log.debug(eventstore_paths)

        # Flatten the self.init_config definitions into valid metric definitions
        metric_definitions = defaultdict(list)
        for metric in metric_def:
            self.log.debug("metric %s", metric)
            json_path = metric.get('json_path', '')
            self.log.debug("json_path %s", json_path)
            tags = metric.get('tag_by', {})
            self.log.debug("tags %s", tags)
            paths = self.get_json_path(json_path, eventstore_paths)
            self.log.debug("paths %s", paths)

            for path in paths:
                # Deep copy needed else it will overwrite previous metric data
                metric_builder = copy.deepcopy(metric)
                metric_builder['json_path'] = path
                tag_builder = []
                if tag_by_url:
                    tag_builder.append('instance:{}'.format(url))
                tag_builder.append('name:{}'.format(name_tag))
                for tag in tags:
                    if ':' in tag:
                        # example: projection:projections.*.effectiveName
                        tag_name, tag = tag.rsplit(':', 1)
                        tag_path = self.get_tag_path(tag, path, eventstore_paths)
                    else:
                        # example: projections.*.effectiveName
                        tag_path = self.get_tag_path(tag, path, eventstore_paths)
                        tag_name = self.format_tag(tag_path.split('.')[-1])
                    tag_value = self.get_value(parsed_api, tag_path)
                    tag_builder.append('{}:{}'.format(tag_name, tag_value))
                metric_builder['tag_by'] = tag_builder
                metric_definitions[path].append(metric_builder)

        # Find metrics to check:
        metrics_to_check = {}
        for metric in instance['json_path']:
            self.log.debug("metric: %s", metric)
            paths = self.get_json_path(metric, eventstore_paths)
            self.log.debug("paths: %s", paths)
            for path in paths:
                self.log.debug("path: %s", path)
                try:
                    metrics_to_check[path] = metric_definitions[path]
                    self.log.debug("metrics_to_check: %s", metric_definitions[path])
                except KeyError:
                    self.log.info("Skipping metric: %s as it is not defined", path)

        # Now we need to get the metrics from the endpoint
        # Get the value for a given key
        self.log.debug("parsed_api:")
        self.log.debug(parsed_api)
        for path, metrics in metrics_to_check.items():
            raw_value = self.get_value(parsed_api, path)
            for metric in metrics:
                metric_value = self.convert_value(raw_value, metric)
                if metric_value is not None:
                    self.dispatch_metric(metric_value, metric)
                else:
                    # self.dispatch_metric(0, metric)
                    self.log.debug("Metric %s did not return a value, skipping", path)

    @classmethod
    def format_tag(cls, name):
        """Converts the string to snake case from camel case"""
        # https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def walk(self, json_obj, p=None, es_paths=None):
        """ Walk a JSON tree and return the json paths in a list """
        if p is None:
            p = []
        if es_paths is None:
            es_paths = []

        if isinstance(json_obj, list):
            json_obj = dict((str(k), v) for k, v in enumerate(json_obj))

        for key, value in json_obj.items():
            if isinstance(value, (dict, list)):
                # We add the instance to the path global variable to build up a map
                p.append(key)
                self.walk(value, p, es_paths)
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
            self.log.warning('No tag value found for %s, path %s', tag, metric_json_path)

    def get_json_path(self, json_path, eventstore_paths):
        """ Find all the possible keys for a given path """
        self.log.debug("json paths: %s", json_path)
        self.log.debug("eventstore_paths: %s", eventstore_paths)
        response = []
        self.log.debug("response: %s", response)
        try:
            match = eventstore_paths.index(json_path)
            self.log.debug("match: %s", match)
            if match is not None:
                response.append(json_path)
                self.log.debug("match json path: %s", json_path)
        except ValueError:
            # Loop through all possible keys to find matches
            # Value Error means it didn't find it, so it must be
            # a wildcard
            self.log.debug("value error")
            for path in eventstore_paths:
                self.log.debug("path: %s", path)
                match = fnmatch.fnmatch(path, json_path)
                self.log.debug("match ve: %s", match)
                if match:
                    response.append(path)
                    self.log.debug("path ve: %s", path)
        return response

    # Fill out eventstore_paths using walk of json

    def get_value(self, json_obj, metric_path, index=0):
        """ Returns the value for the supplied metric path """
        split = metric_path.split('.')
        key = split[index]
        if isinstance(json_obj, list):
            json_obj = dict((str(k), v) for k, v in enumerate(json_obj))
        try:
            v = json_obj[key]
            if isinstance(v, (dict, list)):
                index += 1
                v = self.get_value(v, metric_path, index=index)
            else:
                v = str(v)
            if len(v) == 0:
                v = 'N/A'
            return v
        except KeyError:
            self.log.info('No value found for Metric: %s', metric_path)

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
        elif data_type == 'str':
            v = self.convert_str_to_gauge(value, metric)
        elif data_type == 'bool':
            v = 1 if value else 0
        return v

    def convert_str_to_gauge(self, value, metric):
        v = None
        match = metric.get('match')
        mismatch = metric.get('mismatch')
        if match and mismatch:
            self.log.info(
                'Only one of match or mismatch can be specified to convert the str metric to a gauge for: %s %s',
                metric['json_path'],
                metric['metric_name'],
            )
        elif not match and not mismatch:
            self.log.info(
                'Match or mismatch should be specified to convert the str metric to a gauge for: %s %s',
                metric['json_path'],
                metric['metric_name'],
            )
        else:
            checklist = match or mismatch
            if isinstance(checklist, (frozenset, list, set, tuple)):
                checklist = frozenset(checklist)
            else:
                checklist = frozenset((checklist,))
            if match:
                v = 1 if value in checklist else 0
            elif mismatch:
                v = 0 if value in checklist else 1
        return v

    def convert_to_timedelta(self, string):
        """
        Returns a time delta for strings in a format of: 0:00:00:00.0000
        Using RegEx to not introduce a dependancy on another package
        """
        dt_re = re.compile(r'^(\d+):(\d\d):(\d\d):(\d\d).(\d+)$')
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
            self.log.info('Unable to convert %s to timedelta', string)
        except TypeError:
            self.log.info('Unable to convert %s to type timedelta', string)

    @classmethod
    def _regex_number_to_int(cls, number, group_index):
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
            self.log.debug("Sending gauge %s v: %s t: %s", metric_name, value, tags)
            self.gauge(metric_name, value, tags)
        elif metric_type == 'histogram':
            self.log.debug("Sending histogram %s v: %s t: %s", metric_name, value, tags)
            self.histogram(metric_name, value, tags)
        else:
            self.log.info('Unable to send metric %s due to invalid metric type of %s', metric_name, metric_type)
