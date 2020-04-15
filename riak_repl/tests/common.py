import os

from datadog_checks.dev import get_docker_hostname

HERE = os.path.dirname(os.path.abspath(__file__))
HOST = get_docker_hostname()
URL = 'http://{}:8098/riak-repl/stats'.format(HOST)
INSTANCE = {'default_timeout': 5, 'url': URL, 'connected_clusters': ['riak-west-1']}
