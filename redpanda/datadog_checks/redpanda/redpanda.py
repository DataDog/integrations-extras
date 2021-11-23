from collections import ChainMap

from six.moves.urllib.parse import urlparse

from datadog_checks.base import ConfigurationError, OpenMetricsBaseCheckV2
from datadog_checks.base.checks.openmetrics.v2.scraper import OpenMetricsCompatibilityScraper

from .metrics import ADDITIONAL_METRICS_MAP, INSTANCE_DEFAULT_METRICS


class RedpandaCheck(OpenMetricsBaseCheckV2):
    __NAMESPACE__ = 'redpanda'

    DEFAULT_METRIC_LIMIT = 0

    def __init__(self, name, init_config, instances):
        super(RedpandaCheck, self).__init__(name, init_config, instances)
        self.check_initializations.appendleft(self._parse_config)

    def _parse_config(self):
        self.scraper_configs = []
        endpoint = self.instance.get('openmetrics_endpoint')

        if endpoint is None:
            raise ConfigurationError("Unable to find openmetrics URL in config file.")

        # extract additional metrics requested and validate the correct names
        metric_groups = self.instance.get('metric_groups', [])
        additional_metrics = []
        if metric_groups:
            errors = []
            for group in metric_groups:
                try:
                    additional_metrics.append(ADDITIONAL_METRICS_MAP[group])
                except KeyError:
                    errors.append(group)

            if errors:
                raise ConfigurationError(
                    'Invalid metric_groups found in redpanda conf.yaml: {}'.format(', '.join(errors))
                )

        tags = self.instance.get('tags', [])

        # include hostname:port for server tag
        tags.append('redpanda_server:{}'.format(urlparse(endpoint).netloc))

        metrics = INSTANCE_DEFAULT_METRICS + additional_metrics

        config = {
            'openmetrics_endpoint': endpoint,
            'namespace': self.__NAMESPACE__,
            'metrics': metrics,
            'tags': tags,
            'metadata_label_map': {'version': 'version'},
        }
        config.update(self.instance)
        self.scraper_configs.append(config)

    def create_scraper(self, config):
        return OpenMetricsCompatibilityScraper(self, self.get_config_with_defaults(config))

    def get_config_with_defaults(self, config):
        return ChainMap(config, {'metrics': config.pop('metrics')})
