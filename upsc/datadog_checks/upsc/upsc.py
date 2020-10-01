# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
import os
import re
import subprocess

from datadog_checks.base import AgentCheck, ensure_unicode

EVENT_TYPE = SOURCE_TYPE_NAME = 'upsc'


class UpscCheck(AgentCheck):

    DEV_NULL = open(os.devnull, 'w')
    DEFAULT_STRING_TAGS = ['device.mfr', 'device.model']
    DEFAULT_EXCLUDED_TAGS = ['ups.vendorid', 'ups.productid', 'driver.version.internal', 'driver.version']

    def list_ups_devices(self):
        """Generate and return the list of configured devices.

        :return: list of devices by name
        :rtype: list[str]
        """
        try:
            results = subprocess.check_output(['upsc', '-l'], stderr=self.DEV_NULL)
            return [r.strip() for r in results.split('\n')]
        except subprocess.CalledProcessError as e:
            self.log.error("Unable to query devices: %s", e)
            return []

    def query_ups_device(self, name):
        """Query ups device and return results

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
                stats[key] = val.strip()
            return stats
        except subprocess.CalledProcessError as e:
            self.log.error("Unable to query device %s", name, e)
            return {}

    def convert_and_filter_stats(self, stats):
        """Converts raw query stats to native python types

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
                if r.match(k):
                    found_re = True
                    break
            if found_re:
                continue

            try:  # try a number conversion
                value = float(v.strip())
                results[k] = value
            except Exception:  # this is a string value instead
                if k == 'ups.status':
                    if v.lower().startswith('ol') or v.lower().startswith('on'):
                        results[k] = 1.0
                    else:
                        results[k] = 0.0
                if k in self.string_tags:
                    tags.add('{}:{}'.format(k, ensure_unicode(self.convert_to_underscore_separated(v))))
        return results, tags

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

                self.log.debug("querying device: %s", device)

                # query stats
                raw_stats = self.query_ups_device(device)
                stats, tags = self.convert_and_filter_stats(raw_stats)

                # report stats
                for k, v in stats.items():
                    self.gauge('upsc.{}'.format(k), v, tags=tags)

    def update_from_config(self, instance):
        """Update Configuration tunables from instance configuration.

        :param instance: Agent config instance.
        :return: None
        """
        self.string_tags = list(self.DEFAULT_STRING_TAGS)
        self.string_tags.extend(instance.get('string_tags', []))

        self.additional_tags = instance.get('tags', [])

        self.excluded = list(self.DEFAULT_EXCLUDED_TAGS)
        self.excluded.extend(instance.get('excluded', []))
        self.excluded_re = []
        for excluded_regex in instance.get('excluded_re', []):
            self.excluded_re.append(re.compile(excluded_regex))

        self.excluded_devices = instance.get('excluded_devices', [])
        self.excluded_devices_re = []
        for excluded_regex in instance.get('excluded_devices_re', []):
            self.excluded_devices_re.append(re.compile(excluded_regex))
