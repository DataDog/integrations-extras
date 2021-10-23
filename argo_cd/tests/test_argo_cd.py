import pytest

from datadog_checks.argo_cd import ArgoCdCheck

CHECK_NAME = 'argo_cd'


@pytest.mark.unit
def test_check_all_metrics(aggregator, mock_argo_cd):
    instance = {'prometheus_url': 'http://localhost:8082/metrics'}
    c = ArgoCdCheck(CHECK_NAME, {}, [instance])
    c.check(instance)
    aggregator.assert_metric("argocd.app_info", count=4, value=1)
