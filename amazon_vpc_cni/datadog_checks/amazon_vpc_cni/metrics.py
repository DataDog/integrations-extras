METRIC_MAP = {
    ## IPAMD
    'awscni_ipamd_error_count': 'ipamd_error_count',
    'awscni_ipamd_action_inprogress': 'ipamd_action_inprogress',
    'awscni_reconcile_count': 'reconcile_count',
    'awscni_add_ip_req_count': 'add_ip_req_count',
    'awscni_del_ip_req_count': 'del_ip_req_count',
    'awscni_pod_eni_error_count': 'pod_eni_error_count',
    ## AWS API
    'awscni_aws_api_latency_ms': 'aws_api_latency_ms',
    'awscni_aws_api_error_count': 'aws_api_error_count',
    'awscni_aws_utils_error_count': 'aws_utils_error_count',
    'awscni_ec2api_req_count': 'ec2api_req_count',
    'awscni_ec2api_error_count': 'ec2api_error_count',
    'awscni_sagemakerapi_req_count': 'sagemakerapi_req_count',
    'awscni_sagemakerapi_error_count': 'sagemakerapi_error_count',
    ## ENI / IP allocation
    'awscni_eni_max': 'eni_max',
    'awscni_ip_max': 'ip_max',
    'awscni_eni_allocated': 'eni_allocated',
    'awscni_total_ip_addresses': 'total_ip_addresses',
    'awscni_assigned_ip_addresses': 'assigned_ip_addresses',
    'awscni_force_removed_enis': 'force_removed_enis',
    'awscni_force_removed_ips': 'force_removed_ips',
    'awscni_total_ipv4_prefixes': 'total_ipv4_prefixes',
    'awscni_assigned_ip_per_cidr': 'assigned_ip_per_cidr',
    'awscni_no_available_ip_addresses': 'no_available_ip_addresses',
    'awscni_assigned_ip_per_eni': 'assigned_ip_per_eni',
    ## Startup duration
    'awscni_ipamd_startup_duration_seconds': 'ipamd_startup_duration_seconds',
    'awscni_ipamd_node_initialization_duration_seconds': 'ipamd_node_initialization_duration_seconds',
    ## Connmark
    'awscni_connmark_backend': 'connmark_backend',
    'awscni_connmark_reconcile': 'connmark_reconcile_total',
}
