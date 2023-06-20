import pytest

from datadog_checks.nextcloud import NextcloudCheck


def test_empty_url(aggregator, empty_url_instance):
    check = NextcloudCheck('nextcloud', {}, [empty_url_instance])
    check.check({})
    aggregator.assert_service_check(NextcloudCheck.STATUS_CHECK, check.CRITICAL)


@pytest.mark.usefixtures('dd_environment')
@pytest.mark.integration
def test_invalid_url(aggregator, invalid_url_instance):
    check = NextcloudCheck('nextcloud', {}, [invalid_url_instance])
    check.check({})
    aggregator.assert_service_check(NextcloudCheck.STATUS_CHECK, check.CRITICAL)


@pytest.mark.usefixtures('dd_environment')
@pytest.mark.integration
def test_valid_check(aggregator, instance):
    check = NextcloudCheck('nextcloud', {}, [instance])
    check.check({})
    aggregator.assert_service_check(NextcloudCheck.STATUS_CHECK, check.OK)

    for gauge in NextcloudCheck.METRICS_GAUGES:
        aggregator.assert_metric(check.get_metric_display_name(gauge), tags=check.tags)

    aggregator.assert_all_metrics_covered()
