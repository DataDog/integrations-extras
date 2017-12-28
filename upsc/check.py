# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib
import os
import re
import subprocess

# 3rd party

# project
from checks import AgentCheck

EVENT_TYPE = SOURCE_TYPE_NAME = 'upsc'


class UpscCheck(AgentCheck):

    DEV_NULL = open(os.devnull, 'w')

    def list_ups_devices(self):
        """ Generate and return the list of configured devices.

        :return: list of devices by name
        :rtype: list[str]
        """
        try:
            results = subprocess.check_output(['upsc', '-l'], stderr=self.DEV_NULL)
            return results.splitlines(False)
        except subprocess.CalledProcessError as e:
            self.log.error("Unable to query devices", e)
            return []

    def query_ups_device(self, name):
        """ Query ups device and return results

        :param name: UPS device name from `list_ups_devices`
        :type name: str
        :return: raw results in simple form
        :rtype: dict(str, str)
        """
        try:
            results = subprocess.check_output(['upsc', name], stderr=self.DEV_NULL)
            stats = {}
            for line in results.splitlines(False):
                key, val = line.split(':', 1)
                stats[key] = val
            return stats
        except subprocess.CalledProcessError as e:
            self.log.error("Unable to query device %s" % name, e)
            return {}

    def convert_and_filter_stats(self, stats):
        """ Converts raw query stats to native python types

        Drops string results as well.

        :param stats: raw query stats
        :type stats: dict(str, str)
        :return: converted results and tags
        :rtype: tuple[dict(str, float), list[str]]
        """
        results = {}
        tags = set(self.additional_tags)
        for k, v in stats.items():
            if k in self.excluded:
                continue
            found_re = False
            for r in self.excluded_re:
                "type: re.compile"
                if r.match(k):
                    found_re = True
                    break
            if found_re:
                continue

            v = v.lstrip().rstrip()
            try:
                value = float(v.lstrip().rstrip())
                results[k] = value
            except Exception:
                if k == 'ups.status':
                    if v.lower().startswith('ol') or v.lower().startswith('on'):
                        results[k] = 1
                    else:
                        results[k] = 0
                if k in self.string_tags:
                    tags.add('{}:{}'.format(k, self.convert_to_underscore_separated(v)))
        return results

    def check(self, instance):
        self.update_from_config(instance)

        for device in self.list_ups_devices():
            if device not in self.excluded_devices:
                excluded = False
                for r in self.excluded_devices_re:
                    if r.match(device):
                        excluded = True
                        break
                if excluded:
                    continue

                # query stats
                stats, tags = self.query_ups_device(device)

                # report stats
                for k, v in stats:
                    self.gauge('upsc.{}'.format(k), v, tags=tags)

    def update_from_config(self, instance):
        """ Update Configuration tunables from instance configuration.

        :param instance: Agent config instance.
        :return: None
        """
        self.string_tags = ['device.mfr', 'device.model']
        self.string_tags.extend(instance.get('string_tags', []))

        self.additional_tags = []
        self.additional_tags.extend(instance.get('tags', []))

        self.excluded = ['ups.vendorid', 'ups.productid', 'driver.version.internal', 'driver.version']
        self.excluded.extend(instance.get('excluded', []))
        self.excluded_re = []
        for excluded_regex in instance.get('excluded_re', []):
            self.excluded_re.append(re.compile(excluded_regex))

        self.excluded_devices = []
        self.excluded_devices.extend(instance.get('excluded_devices', []))
        self.excluded_devices_re = []
        for excluded_regex in instance.get('excluded_devices_re', []):
            self.excluded_devices_re.append(re.compile(excluded_regex))