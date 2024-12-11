# (C) Datadog, Inc. 2024-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

from datadog_checks.base.constants import ServiceCheck
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.scaphandre import ScaphandreCheck

from .common import METRICS, MOCKED_INSTANCE, get_fixture_path


def test_check(dd_run_check, aggregator, mock_http_response):
    mock_http_response(file_path=get_fixture_path('output.txt'))
    check = ScaphandreCheck('scaphandre', {}, [MOCKED_INSTANCE])
    dd_run_check(check)

    for metric in METRICS:
        aggregator.assert_metric(f'scaphandre.{metric}')

    aggregator.assert_service_check('scaphandre.openmetrics.health', ServiceCheck.OK)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
    aggregator.assert_service_check('scaphandre.openmetrics.health', ServiceCheck.OK)
