# (C) Datadog, Inc. 2020
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from datadog_checks.errors import CheckException
from datadog_checks.checks.openmetrics import OpenMetricsBaseCheck

class FluentBitCheck(OpenMetricsBaseCheck):
    """
    Collect Fluent Bit metrics from Prometheus endpoint
    """
    def __init__(self, name, init_config, agentConfig, instances=None):
        super(FluentBitCheck, self).__init__(name, init_config, agentConfig, instances)
        self.NAMESPACE = 'fluentbit'

        self.metrics_mapper = {
            'fluentbit_filter_add_records_total': 'filter.add_record',
            'fluentbit_filter_drop_records_total': 'filter.drop_record',
            'fluentbit_input_bytes_total': 'input.bytes',
            'fluentbit_input_records_total': 'input.record',
            'fluentbit_output_errors_total': 'output.errors',
            'fluentbit_output_proc_bytes_total': 'output.proc_bytes',
            'fluentbit_output_proc_records_total': 'output.proc_records',
            'fluentbit_output_retries_failed_total': 'output.retries_failed',
            'fluentbit_output_retries_total': 'output.retries',
        }

        # TODO : consider another metric "process_start_time_seconds"
        #  It is a epoch number and not very useful (ex 1586379595).
        #  Would be better to send "date - process_start_time_seconds" to show uptime

        # TODO : send status checks

    def check(self, instance):
        endpoint = instance.get('prometheus_endpoint')
        if endpoint is None:
            raise CheckException("Unable to find prometheus_endpoint in config file.")

        send_buckets = instance.get('send_histograms_buckets', True)
        # By default, we send the buckets.
        if send_buckets is not None and str(send_buckets).lower() == 'false':
            send_buckets = False
        else:
            send_buckets = True

        self.process(endpoint, send_histograms_buckets=send_buckets, instance=instance)
