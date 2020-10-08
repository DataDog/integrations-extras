from datadog_checks.base import ConfigurationError, OpenMetricsBaseCheck

EVENT_TYPE = SOURCE_TYPE_NAME = 'pulsar'


class PulsarCheck(OpenMetricsBaseCheck):
    """
    PulsarCheck derives from AgentCheck that provides the required check method
    """

    def __init__(self, name, init_config, instances=None):
        instance = instances[0]
        url = instance.get('prometheus_url')
        if url is None:
            raise ConfigurationError("Unable to find prometheus_url in config file.")

        # token = instance.get('token')

        # tenant = instance.get('tenant')

        self.NAMESPACE = 'kesque.pulsar'
        self.metrics_mapper = {
            'pulsar_consumer_available_permits': 'consumer.available_permits',
            'pulsar_consumer_blocked_on_unacked_messages': 'consumer.blocked_on_unacked_messages',
            'pulsar_consumer_msg_rate_out': 'consumer.msg_rate_out',
            'pulsar_consumer_msg_rate_redeliver': 'consumer.msg_rate_redeliver',
            'pulsar_consumer_msg_throughput_out': 'consumer.msg_throughput_out',
            'pulsar_consumer_unacked_messages': 'consumer.unacked_messages',
            'pulsar_consumers_count': 'consumers_count',
            'pulsar_entry_size_count': 'entry_size_count',
            'pulsar_entry_size_le_100_kb': 'entry_size_le_100_kb',
            'pulsar_entry_size_le_128': 'entry_size_le_128',
            'pulsar_entry_size_le_16_kb': 'entry_size_le_16_kb',
            'pulsar_entry_size_le_1_kb': 'entry_size_le_1_kb',
            'pulsar_entry_size_le_1_mb': 'entry_size_le_1_mb',
            'pulsar_entry_size_le_2_kb': 'entry_size_le_2_kb',
            'pulsar_entry_size_le_4_kb': 'entry_size_le_4_kb',
            'pulsar_entry_size_le_512': 'entry_size_le_512',
            'pulsar_entry_size_le_overflow': 'entry_size_le_overflow',
            'pulsar_entry_size_sum': 'entry_size_sum',
            'pulsar_in_bytes_total': 'in_bytes_total',
            'pulsar_in_messages_total': 'in_messages_total',
            'pulsar_msg_backlog': 'msg_backlog',
            'pulsar_out_bytes_total': 'out_bytes_total',
            'pulsar_out_messages_total': 'out_messages_total',
            'pulsar_producers_count': 'producers_count',
            'pulsar_rate_in': 'rate_in',
            'pulsar_rate_out': 'rate_out',
            'pulsar_replication_backlog': 'replication.backlog',
            'pulsar_replication_rate_in': 'replication.rate_in',
            'pulsar_replication_rate_out': 'replication.rate_out',
            'pulsar_replication_throughput_in': 'replication.throughput_in',
            'pulsar_replication_throughput_out': 'replication.throughput_out',
            'pulsar_storage_backlog_quota_limit': 'storage.backlog_quota_limit',
            'pulsar_storage_backlog_size': 'storage.backlog_size',
            'pulsar_storage_read_rate': 'storage.read_rate',
            'pulsar_storage_offloaded_size': 'storage.offloaded_size',
            'pulsar_storage_size': 'storage.size',
            'pulsar_storage_write_latency_count': 'storage.write_latency_count',
            'pulsar_storage_write_latency_le_0_5': 'storage.write_latency_le_0_5',
            'pulsar_storage_write_latency_le_1': 'storage.write_latency_le_1',
            'pulsar_storage_write_latency_le_10': 'storage.write_latency_le_10',
            'pulsar_storage_write_latency_le_100': 'storage.write_latency_le_100',
            'pulsar_storage_write_latency_le_1000': 'storage.write_latency_le_1000',
            'pulsar_storage_write_latency_le_20': 'storage.write_latency_le_20',
            'pulsar_storage_write_latency_le_200': 'storage.write_latency_le_200',
            'pulsar_storage_write_latency_le_5': 'storage.write_latency_le_5',
            'pulsar_storage_write_latency_le_50': 'storage.write_latency_le_50',
            'pulsar_storage_write_latency_overflow': 'storage.write_latency_overflow',
            'pulsar_storage_write_latency_sum': 'storage.write_latency_sum',
            'pulsar_storage_write_rate': 'storage.write_rate',
            'pulsar_subscription_back_log': 'subscription.back_log',
            'pulsar_subscription_back_log_no_delayed': 'subscription.back_log_no_delayed',
            'pulsar_subscription_blocked_on_unacked_messages': 'subscription.blocked_on_unacked_messages',
            'pulsar_subscription_delayed': 'subscription.delayed',
            'pulsar_subscription_msg_rate_out': 'subscription.msg_rate_out',
            'pulsar_subscription_msg_rate_redeliver': 'subscription.msg_rate_redeliver',
            'pulsar_subscription_msg_throughput_out': 'subscription.msg_throughput_out',
            'pulsar_subscription_unacked_messages': 'subscription.unacked_messages',
            'pulsar_subscriptions_count': 'subscriptions.count',
            'pulsar_throughput_in': 'throughput_in',
            'pulsar_throughput_out': 'throughput_out',
            'pulsar_topics_count': 'topics_count',
            'scrape_duration_seconds': 'scrape_duration_seconds',
            'scrape_samples_post_metric_relabeling': 'scrape_samples_post_metric_relabeling',
            'scrape_samples_scraped': 'scrape_samples_scraped',
            'topic_load_times': 'topic_load_times',
            'topic_load_times_count': 'topic_load_times_count',
            'topic_load_times_sum': 'topic_load_times_sum',
            'up': 'broker.up',
        }

        instance.update(
            {
                'prometheus_url': url,
                'namespace': self.NAMESPACE,
                'metrics': [self.metrics_mapper],
                # 'send_histograms_buckets': send_buckets,
                # 'send_distribution_counts_as_monotonic': instance.get('send_distribution_counts_as_monotonic', True)
                # default to True to submit _count histogram/summary as monotonic
                # counts to Datadog
            }
        )
        super(PulsarCheck, self).__init__(name, init_config, instances)
