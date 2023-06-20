from datadog_checks.base.checks.prometheus.prometheus_base import PrometheusCheck
from datadog_checks.base.errors import CheckException

EVENT_TYPE = SOURCE_TYPE_NAME = 'portworx'


class PortworxCheck(PrometheusCheck):
    """
    Collect px metrics from Portworx
    """

    def __init__(self, name, init_config, instances=None):
        super(PortworxCheck, self).__init__(name, init_config, instances)
        self.NAMESPACE = 'portworx'
        self.metrics_mapper = {
            'px_cluster_cpu_percent': 'cluster.cpu_percent',
            'px_cluster_disk_available_bytes': 'cluster.disk_available_bytes',
            'px_cluster_disk_total_bytes': 'cluster.disk_total_bytes',
            'px_cluster_disk_utilized_bytes': 'cluster.disk_utilized_bytes',
            'px_cluster_memory_utilized_percent': 'cluster.memory_utilized_percent',
            'px_cluster_pendingio': 'cluster.pendingio',
            'px_cluster_status_cluster_quorum': 'cluster.status.cluster_quorum',
            'px_cluster_status_cluster_size': 'cluster.status.cluster_size',
            'px_cluster_status_nodes_offline': 'cluster.status.nodes_offline',
            'px_cluster_status_nodes_online': 'cluster.status.nodes_online',
            'px_cluster_status_nodes_storage_down': 'cluster.status.nodes_storage_down',
            'px_cluster_status_storage_nodes_offline': 'cluster.status.storage_nodes_offline',
            'px_cluster_status_storage_nodes_online': 'cluster.status.storage_nodes_online',
            'px_disk_stats_interval_seconds': 'disk_stats.interval_seconds',
            'px_disk_stats_io_seconds': 'disk_stats.io_seconds',
            'px_disk_stats_progress_io': 'disk_stats.progress_io',
            'px_disk_stats_read_bytes': 'disk_stats.read_bytes',
            'px_disk_stats_read_latency_seconds': 'disk_stats.read_latency_seconds',
            'px_disk_stats_read_seconds': 'disk_stats.read_seconds',
            'px_disk_stats_reads': 'disk_stats.reads',
            'px_disk_stats_used_bytes': 'disk_stats.used_bytes',
            'px_disk_stats_write_bytes': 'disk_stats.write_bytes',
            'px_disk_stats_write_latency_seconds': 'disk_stats.write_latency_seconds',
            'px_disk_stats_write_seconds': 'disk_stats.write_seconds',
            'px_disk_stats_writes': 'disk_stats.writes',
            'px_network_io_bytessent': 'network_io.bytessent',
            'px_network_io_received_bytes': 'network_io.received_bytes',
            'px_pool_stats_pool_flushed_bytes': 'pool_stats.flushed_bytes',
            'px_pool_stats_pool_flushms': 'pool_stats.flushms',
            'px_pool_stats_pool_num_flushes': 'pool_stats.num_flushes',
            'px_pool_stats_pool_write_latency_seconds': 'pool_stats.write_latency_seconds',
            'px_pool_stats_pool_writethroughput': 'pool_stats.writethroughput',
            'px_pool_stats_pool_written_bytes': 'pool_stats.written_bytes',
            'px_proc_stats_cpu_percenttime': 'proc.cpu_percenttime',
            'px_proc_stats_res': 'proc.res',
            'px_proc_stats_virt': 'proc.virt',
            'px_volume_capacity_bytes': 'volume.capacity_bytes',
            'px_volume_currhalevel': 'volume.currhalevel',
            'px_volume_depth_io': 'volume.depth_io',
            'px_volume_dev_depth_io': 'volume.dev.depth_io',
            'px_volume_dev_read_latency_seconds': 'volume.dev.read_latency_seconds',
            'px_volume_dev_readthroughput': 'volume.dev.readthroughput',
            'px_volume_dev_write_latency_seconds': 'volume.dev.write_latency_seconds',
            'px_volume_dev_writethroughput': 'volume.dev.writethroughput',
            'px_volume_halevel': 'volume.halevel',
            'px_volume_iopriority': 'volume.iopriority',
            'px_volume_iops': 'volume.iops',
            'px_volume_num_long_flushes': 'volume.num_long_flushes',
            'px_volume_num_long_reads': 'volume.num_long_reads',
            'px_volume_num_long_writes': 'volume.num_long_writes',
            'px_volume_readthroughput': 'volume.readthroughput',
            'px_volume_usage_bytes': 'volume.usage_bytes',
            'px_volume_vol_read_latency_seconds': 'volume.vol_read_latency_seconds',
            'px_volume_vol_write_latency_seconds': 'volume.vol_write_latency_seconds',
            'px_volume_writethroughput': 'volume.writethroughput',
            'px_volume_written_bytes': 'volume.written_bytes',
            'fs_usage_bytes': 'fs.usage_bytes',
            'fs_capacity_bytes': 'fs.capacity_bytes',
        }

    def check(self, instance):
        endpoint = instance.get('prometheus_endpoint')
        if endpoint is None:
            raise CheckException("Unable to find prometheus_endpoint in config file.")

        send_buckets = instance.get('send_histograms_buckets', True)
        # By default we send the buckets.
        if send_buckets is not None and str(send_buckets).lower() == 'false':
            send_buckets = False
        else:
            send_buckets = True

        self.process(endpoint, send_histograms_buckets=send_buckets, instance=instance)
