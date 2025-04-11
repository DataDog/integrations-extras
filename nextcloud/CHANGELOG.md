# CHANGELOG - Nextcloud

# 1.1.0 / 2025-04-12


***Changed***:

* Move `nextcloud.system.apps.*` metrics behind the `apps_stats` option.

    Beginning with Nextcloud 28, the monitoring endpoint no longer provides information about available app updates, as gathering the data always involves at least one external request to apps.nextcloud.com.

    It is still possible to ask the monitoring endpoint to show new app updates by using the URL parameter skipApps=false. However, Nextcloud recommends to not check this endpoint too often.

    https://github.com/nextcloud/serverinfo#api
