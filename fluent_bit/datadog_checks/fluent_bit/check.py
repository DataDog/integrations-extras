from datadog_checks.base import ConfigurationError, OpenMetricsBaseCheckV2


class FluentBitCheck(OpenMetricsBaseCheckV2):
    __NAMESPACE__ = 'fluentbit'

    def __init__(self, name, init_config, instances):
        super(FluentBitCheck, self).__init__(name, init_config, instances)
        self.check_initializations.appendleft(self._parse_config)

    def _parse_config(self):
        self.scraper_configs = []
        metrics_endpoint = self.instance.get('metrics_endpoint')

        metrics_map = {
            'fluentbit_input_records': 'input.records',
            'fluentbit_input_bytes': 'input.bytes',
            'fluentbit_filter_add_records': 'filter.add_records',
            'fluentbit_filter_drop_records': 'filter.drop_records',
            'fluentbit_output_proc_records': 'output.proc_records',
            'fluentbit_output_proc_bytes': 'output.proc_bytes',
            'fluentbit_output_errors': 'output.errors',
            'fluentbit_output_retries': 'output.retries',
            'fluentbit_output_retries_failed': 'output.retries_failed',
            'fluentbit_output_retried_records': 'output.retried_records',
            'fluentbit_output_dropped_records': 'output.dropped_records',
        }

        config = {
            'openmetrics_endpoint': metrics_endpoint,
            'metrics': [metrics_map],
        }
        config.update(self.instance)
        self.scraper_configs.append(config)
