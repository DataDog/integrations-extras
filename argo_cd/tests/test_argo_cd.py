# (C) Datadog, Inc. 2021-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)


import pytest
from datadog_checks.argo_cd import ArgoCdCheck
from datadog_checks.argo_cd.metrics import APPLICATION_METRICS
CHECK_NAME = 'argocd'

# EXPECTED_VALUES = (
#     ("argocd.app_info", 4,1),
#     ("argocd.cluster_api_resource_objects",1,1077.0),
#     ("argocd.cluster_api_resources",1,89.0),
#     ("argocd.kubectl_exec_pending", 1,0.0),
#     ("argocd.cluster_info", 1,1.0),
#     ("argocd.cluster_cache_age_seconds", 1,16003.0),
# )

# @pytest.mark.integration
# def test_check_all_metrics(aggregator, dd_run_check, mock_argo_cd):
#     instance = {'openmetrics_endpoint': 'http://localhost:50000/metrics'}
#     c = ArgoCdCheck(CHECK_NAME, {}, [instance])
#     requests.get(mock_argo_cd)
#     dd_run_check(c)
#     # aggregator.assert_metric("argocd.app_info", count=6, value=1)
#     # print(aggregator.assert_metric("argocd.app_info"))
#     #aggregator.assert_metric("argocd.cluster_api_resource_objects", count=1, value=1077.0)
#     for metric, count,value in EXPECTED_VALUES:
#         aggregator.assert_metric(metric, count=count, value=value)


@pytest.mark.usefixtures('mock_argo_cd')
def test_external_dns(aggregator, dd_run_check, instance):
    """
    Testing argo_cd
    """

    c = ArgoCdCheck(CHECK_NAME, {}, [instance])
    dd_run_check(c)

    for metric in APPLICATION_METRICS.values():
        aggregator.assert_metric('argocd'+'.'+metric)

    aggregator.assert_all_metrics_covered()