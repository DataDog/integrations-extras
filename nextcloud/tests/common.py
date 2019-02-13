# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import os

HERE = os.path.dirname(os.path.abspath(__file__))

CONTAINER_NAME = 'nextcloud-standalone'
USER = 'admin'
PASSWORD = 'admin'
PORT = '8080'
VALID_URL = 'http://localhost:{}/ocs/v2.php/apps/serverinfo/api/v1/info?format=json'.format(PORT)
INVALID_URL = 'http://localhost:{}/ocs/v2.php'.format(PORT)

BASE_CONFIG = {
    'url': VALID_URL,
    'user': USER,
    'password': PASSWORD
}
