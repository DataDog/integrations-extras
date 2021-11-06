# (C) Datadog, Inc. 2021-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)


import pytest

from datadog_checks.argo_cd import ArgoCdCheck

CHECK_NAME = 'argo_cd'


@pytest.mark.integration
def test_check_all_metrics(aggregator, dd_run_check, mock_argo_cd):
    instance = {'prometheus_url': 'http://localhost:8082/metrics'}
    c = ArgoCdCheck(CHECK_NAME, {}, [instance])
    dd_run_check(c)
    aggregator.assert_metric("argocd.app_info", count=4, value=1)
