from collections import ChainMap
from typing import Any  # noqa: F401

from datadog_checks.base import AgentCheck, ConfigurationError, OpenMetricsBaseCheckV2
from datadog_checks.base.checks.openmetrics.v2.scraper import OpenMetricsCompatibilityScraper

from .metrics import ADDITIONAL_METRICS, DEFAULT_METRICS


class RedisEnterpriseCheck(OpenMetricsBaseCheckV2):

    # This will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = 'rdse'

    def __init__(self, name, init_config, instances):

        super(RedisEnterpriseCheck, self).__init__(name, init_config, instances)
        self.check_initializations.appendleft(self._parse_config)

    def _parse_config(self):
        self.scraper_configs = []
        metrics_endpoint = self.instance.get('openmetrics_endpoint')
        metrics = self.get_default_config()

        additional = []
        groups = self.instance.get('extra_metrics', [])
        for g in groups:
            if g not in ADDITIONAL_METRICS.keys():
                raise ConfigurationError(f'invalid group in extra_metrics: {g}')
            additional.append(ADDITIONAL_METRICS[g])

        if len(additional) > 0:
            self.service_check("more_groups", AgentCheck.OK)
            metrics += additional

        excludes = self.instance.get('exclude_metrics', [])
        for m in excludes:
            found = False
            for mg in metrics:
                if m in mg.keys():
                    mg.pop(m)
                    found = True
            if not found:
                raise ConfigurationError(f'invalid metric in excludes: {m}')

        config = {
            'openmetrics_endpoint': metrics_endpoint,
            'namespace': self.__NAMESPACE__,
            'metrics': metrics,
            'metadata_label_map': {'version': 'version'},
        }

        config.update(self.instance)
        self.scraper_configs.append(config)

    def get_default_config(self):

        metrics = []
        for dm in DEFAULT_METRICS:
            metrics.append(dm)
        return metrics

    def can_connect(self, hostname=None, message=None, tags=None):
        print(f'hostname: {hostname}, message: {message}, tags: {tags}')
        return False
