import os

HERE = os.path.dirname(os.path.abspath(__file__))

EXPECTED_PROMETHEUS_METRICS = [
    'amazon_vpc_cni.ipamd_action_inprogress',
    'amazon_vpc_cni.eni_max',
    'amazon_vpc_cni.ip_max',
    'amazon_vpc_cni.eni_allocated',
    'amazon_vpc_cni.total_ip_addresses',
    'amazon_vpc_cni.assigned_ip_addresses',
    'amazon_vpc_cni.total_ipv4_prefixes',
    'amazon_vpc_cni.assigned_ip_per_cidr',
    'amazon_vpc_cni.assigned_ip_per_eni',
    'amazon_vpc_cni.connmark_backend',
    'amazon_vpc_cni.ipamd_error_count.count',
    'amazon_vpc_cni.reconcile_count.count',
    'amazon_vpc_cni.add_ip_req_count.count',
    'amazon_vpc_cni.del_ip_req_count.count',
    'amazon_vpc_cni.pod_eni_error_count.count',
    'amazon_vpc_cni.aws_api_error_count.count',
    'amazon_vpc_cni.aws_utils_error_count.count',
    'amazon_vpc_cni.ec2api_req_count.count',
    'amazon_vpc_cni.ec2api_error_count.count',
    'amazon_vpc_cni.sagemakerapi_req_count.count',
    'amazon_vpc_cni.sagemakerapi_error_count.count',
    'amazon_vpc_cni.force_removed_enis.count',
    'amazon_vpc_cni.force_removed_ips.count',
    'amazon_vpc_cni.no_available_ip_addresses.count',
    'amazon_vpc_cni.connmark_reconcile_total.count',
    'amazon_vpc_cni.aws_api_latency_ms.count',
    'amazon_vpc_cni.aws_api_latency_ms.sum',
    'amazon_vpc_cni.aws_api_latency_ms.quantile',
    'amazon_vpc_cni.ipamd_startup_duration_seconds.count',
    'amazon_vpc_cni.ipamd_startup_duration_seconds.sum',
    'amazon_vpc_cni.ipamd_startup_duration_seconds.bucket',
    'amazon_vpc_cni.ipamd_node_initialization_duration_seconds.count',
    'amazon_vpc_cni.ipamd_node_initialization_duration_seconds.sum',
    'amazon_vpc_cni.ipamd_node_initialization_duration_seconds.bucket',
]

MOCKED_INSTANCE = {'openmetrics_endpoint': 'http://localhost:61678/metrics'}

BAD_HOSTNAME_INSTANCE = {'openmetrics_endpoint': 'http://invalid-hostname:61678/metrics'}


def get_fixture_path(filename):
    return os.path.join(HERE, 'fixtures', filename)
