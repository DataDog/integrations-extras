import os
import pytest
from datadog_checks.dev import docker_run, get_docker_hostname, get_here

URL = 'http://{}:9000'.format(get_docker_hostname())
print("Docker URL: " + str(URL))
FIDDLER_API_KEY = 'eSZ7iyuywmODU0ftl1GvqzuxLNE8mxFWovBftInhqY4'
INSTANCE = {"urlF": "https://demo.fiddler.ai", "fiddler_api_key": FIDDLER_API_KEY, "organization": "demo", 'url': URL}




compose_file = os.path.join(get_here(), 'docker-compose.yml')
print("compose file: " + str(compose_file))

with docker_run(compose_file, build=True, endpoints=[URL]):
    print("Done:")
