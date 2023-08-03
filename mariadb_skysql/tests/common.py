# (C) Datadog, Inc. 2023-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

MOCKED_MARIADB_SKYSQL_INSTANCE = {'mariadb_skysql_endpoint': 'http://skysql:8080/metrics'}

MOCKED_MARIADB_SKYSQL_TAG = f'endpoint:{MOCKED_MARIADB_SKYSQL_INSTANCE["mariadb_skysql_endpoint"]}'

MARIADB_SKYSQL_METRICS = (
    "skysql.mariadb.global.status.aborted_clients",
    "skysql.mariadb.global.status.aborted_connects",
    "skysql.mariadb.global.status.buffer_pool_pages",
    "skysql.mariadb.global.status.bytes_received",
    "skysql.mariadb.global.status.bytes_sent",
    "skysql.mariadb.global.status.commands.count",
    "skysql.mariadb.global.status.innodb_data_read",
    "skysql.mariadb.global.status.innodb_data_written",
    "skysql.mariadb.global.status.innodb_num_open_files",
)
