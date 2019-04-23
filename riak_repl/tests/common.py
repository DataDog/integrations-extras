import os

from datadog_checks.utils.common import get_docker_hostname

HERE = os.path.dirname(os.path.abspath(__file__))
HOST = get_docker_hostname()
URL = 'http://{}:8098/riak-repl/stats'.format(HOST)
INSTANCE = {'default_timeout': 5, 'url': URL}
