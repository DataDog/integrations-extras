import pytest

from datadog_checks.base.constants import ServiceCheck
from datadog_checks.cloudnatix import CloudNatixCheck

from .common import METRICS_URL


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_cloudnatix(aggregator, dd_run_check, instance):
    check = CloudNatixCheck('cloudnatix', {}, [instance])
    dd_run_check(check)

    aggregator.assert_service_check('cloudnatix.openmetrics.health', ServiceCheck.OK)
    aggregator.assert_metric(
        'cloudnatix.vpa',
        tags=[
            f'endpoint:{METRICS_URL}',
            'mode:AutoPilot',
            'namespace:cloudnatix',
            'target_resource_name:clusteragent',
        ],
    )
    aggregator.assert_metric(
        'cloudnatix.vpa.recommendation',
        tags=[
            f'endpoint:{METRICS_URL}',
            'target_container_name:metrics-server',
            'target_resource_name:metrics-server',
            'namespace:kube-system',
            'recommendation_resource:cpu',
            'recommendation_target_spec:requests',
        ],
    )
    aggregator.assert_metric(
        'cloudnatix.vpa.recommendation',
        tags=[
            f'endpoint:{METRICS_URL}',
            'target_container_name:metrics-server',
            'target_resource_name:metrics-server',
            'namespace:kube-system',
            'recommendation_resource:memory',
            'recommendation_target_spec:requests',
        ],
    )
    aggregator.assert_metric(
        'cloudnatix.workload.resource',
        tags=[
            f'endpoint:{METRICS_URL}',
            'container_name:metrics-server',
            'name:metrics-server',
            'namespace:kube-system',
            'resource:cpu',
            'spec:requests',
        ],
    )
    aggregator.assert_metric(
        'cloudnatix.workload.resource',
        tags=[
            f'endpoint:{METRICS_URL}',
            'container_name:metrics-server',
            'name:metrics-server',
            'namespace:kube-system',
            'resource:memory',
            'spec:requests',
        ],
    )
    aggregator.assert_metric(
        'cloudnatix.workload.monthly_spend',
        tags=[f'endpoint:{METRICS_URL}', 'name:metrics-server', 'namespace:kube-system'],
    )
    aggregator.assert_metric(
        'cloudnatix.workload.monthly_projected_saving',
        tags=[f'endpoint:{METRICS_URL}', 'name:metrics-server', 'namespace:kube-system'],
    )
    aggregator.assert_metric(
        'cloudnatix.pod_eviction_by_vpa.count',
        tags=[f'endpoint:{METRICS_URL}', 'name:unknown', 'namespace:cloudnatix'],
    )
    aggregator.assert_metric('cloudnatix.compute.daily_spend', tags=[f'endpoint:{METRICS_URL}'])
