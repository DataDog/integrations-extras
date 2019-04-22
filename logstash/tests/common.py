import os

from datadog_checks.utils.common import get_docker_hostname

HERE = os.path.dirname(os.path.abspath(__file__))

HOST = get_docker_hostname()

URL = 'http://{}:9600'.format(HOST)
