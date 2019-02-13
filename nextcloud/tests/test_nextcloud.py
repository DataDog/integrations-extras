from datadog_checks.nextcloud import NextcloudCheck

import pytest

NEXTCLOUD_SERVICE_CHECK = "nextcloud.can_connect"

CHECK_GAUGES = [
    "nextcloud.system.freespace",
    "nextcloud.system.apps.num_installed",
    "nextcloud.system.apps.num_updates_available",
    "nextcloud.storage.num_users",
    "nextcloud.storage.num_files",
    "nextcloud.storage.num_storages",
    "nextcloud.storage.num_storages_local",
    "nextcloud.storage.num_storages_home",
    "nextcloud.storage.num_storages_other",
    "nextcloud.shares.num_shares",
    "nextcloud.shares.num_shares_user",
    "nextcloud.shares.num_shares_groups",
    "nextcloud.shares.num_shares_link_no_password",
    "nextcloud.shares.num_fed_shares_sent",
    "nextcloud.shares.num_fed_shares_received",
    "nextcloud.server.database.size",
    "nextcloud.activeUsers.last5minutes",
    "nextcloud.activeUsers.last1hour",
    "nextcloud.activeUsers.last24hours"
]


def test_empty_url(aggregator, empty_url_instance):
    check = NextcloudCheck('nextcloud', {}, {})
    check.check(empty_url_instance)
    aggregator.assert_service_check(NEXTCLOUD_SERVICE_CHECK, check.CRITICAL)


@pytest.mark.usefixtures('dd_environment')
@pytest.mark.integration
def test_invalid_url(aggregator, invalid_url_instance):
    check = NextcloudCheck('nextcloud', {}, {})
    check.check(invalid_url_instance)
    aggregator.assert_service_check(NEXTCLOUD_SERVICE_CHECK, check.CRITICAL)


@pytest.mark.usefixtures('dd_environment')
@pytest.mark.integration
def test_valid_check(aggregator, instance):
    check = NextcloudCheck('nextcloud', {}, {})
    check.check(instance)
    aggregator.assert_service_check(NEXTCLOUD_SERVICE_CHECK, check.OK)

    for gauge in CHECK_GAUGES:
        aggregator.assert_metric(gauge)

    aggregator.assert_all_metrics_covered()
