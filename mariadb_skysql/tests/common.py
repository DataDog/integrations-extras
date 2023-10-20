# (C) Datadog, Inc. 2023-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

MOCKED_MARIADB_SKYSQL_INSTANCE = {'mariadb_skysql_endpoint': 'http://skysql:8080/metrics'}

MOCKED_MARIADB_SKYSQL_TAG = f'endpoint:{MOCKED_MARIADB_SKYSQL_INSTANCE["mariadb_skysql_endpoint"]}'

MARIADB_SKYSQL_METRICS = (
    "skysql.mariadb_global_status_aborted_clients",
    "skysql.mariadb_global_status_aborted_connects",
    "skysql.mariadb_global_status_buffer_pool_pages",
    "skysql.mariadb_global_status_bytes_received",
    "skysql.mariadb_global_status_bytes_sent",
    "skysql.mariadb_global_status_commands.count",
    "skysql.mariadb_global_status_innodb_data_read",
    "skysql.mariadb_global_status_innodb_data_written",
    "skysql.mariadb_global_status_innodb_num_open_files",
)
