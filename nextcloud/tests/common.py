# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import os

from datadog_checks.dev import get_docker_hostname

HERE = os.path.dirname(os.path.abspath(__file__))

CONTAINER_NAME = 'nextcloud-standalone'
USER = 'admin'
PASSWORD = 'admin'
HOST = get_docker_hostname()
PORT = '8080'
VALID_URL = 'http://{}:{}/ocs/v2.php/apps/serverinfo/api/v1/info'.format(HOST, PORT)
INVALID_URL = 'http://{}:{}/ocs/v2.php'.format(HOST, PORT)

BASE_CONFIG = {'url': VALID_URL, 'username': USER, 'password': PASSWORD}
