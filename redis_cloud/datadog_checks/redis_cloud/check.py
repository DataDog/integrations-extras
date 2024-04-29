from collections import ChainMap
from typing import Any  # noqa: F401

from datadog_checks.base import AgentCheck, ConfigurationError, OpenMetricsBaseCheckV2
from datadog_checks.base.checks.openmetrics.v2.scraper import OpenMetricsCompatibilityScraper

from .metrics import ADDITIONAL_METRICS, DEFAULT_METRICS


class RedisCloudCheck(AgentCheck):

    # This will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = 'rdsc'

    def __init__(self, name, init_config, instances):
        super(RedisCloudCheck, self).__init__(name, init_config, instances)
        self.check_initializations.appendleft(self._parse_config)

    def _parse_config(self):
        self.scraper_configs = []
        metrics_endpoint = self.instance.get('openmetrics_endpoint')
        metrics = self.get_default_config()

        additional = []
        groups = self.instance.get('metric_groups', [])
        for g in groups:
            if g not in ADDITIONAL_METRICS:
                raise ConfigurationError(f'invalid metric in config: {g}')
            additional.append(ADDITIONAL_METRICS[g])

        if len(additional) > 0:
            self.service_check("more_groups", AgentCheck.OK)
            metrics += additional

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

    def create_scraper(self, config):
        return OpenMetricsCompatibilityScraper(self, self.get_config_with_defaults(config))

    def get_config_with_defaults(self, config):
        metrics = config.pop('metrics')
        return ChainMap(config, {'metrics': metrics})

    def can_connect(self, hostname=None, message=None, tags=None):
        print(f'hostname: {hostname}, message: {message}, tags: {tags}')
        return False

    def check(self, instance):
        # type: (Any) -> None

        # smoke test
        url = instance.get('openmetrics_endpoint')
        if not url:
            raise ConfigurationError('Configuration error, please fix conf.yaml')

        try:
            super().check(instance)
            self.service_check("can_connect", AgentCheck.OK)

        except Exception as e:
            self.log.error('exception: %s', e)
            self.service_check("can_connect", AgentCheck.CRITICAL, message=str(e))
