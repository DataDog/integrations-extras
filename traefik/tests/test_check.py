# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import pytest
import subprocess
import os
import time
import socket
import requests

from datadog_checks.utils.common import get_docker_hostname
from datadog_checks.traefik import TraefikCheck
from datadog_checks.errors import CheckException


def test_check(aggregator):

    c = TraefikCheck('traefik', {}, {}, None)

    c.check({'host': 'foobar'})
    aggregator.assert_all_metrics_covered()

    instance = {}
    with pytest.raises(CheckException):
        c.check(instance)

    with pytest.raises(CheckException):
        c.check({'port': '16080'})

    with pytest.raises(CheckException):
        c.check({'path': 'foo'})


@pytest.mark.integration
def test_service_check(aggregator):
    c = TraefikCheck('traefik', {}, {}, None)

    HERE = os.path.dirname(os.path.abspath(__file__))
    args = [
        "docker-compose",
        "-f", os.path.join(HERE, 'docker-compose.yml')
    ]

    # start the Traefik container
    subprocess.check_call(args + ["up", "-d"])
    time.sleep(5)  # we should implement a better wait strategy :)

    local_ip = '127.0.0.1'

    instance = {
        'host': local_ip
    }

    # the check should send OK
    c.check(instance)
    aggregator.assert_service_check('traefik.health', TraefikCheck.OK)

    # stop the container
    subprocess.check_call(args + ["down"])
    time.sleep(5)  # we should implement a better wait strategy :)

    # the check should send CRITICAL
    c.check(instance)
    aggregator.assert_service_check('traefik.health', TraefikCheck.CRITICAL)


@pytest.mark.integration
def test_collect_metrics(aggregator):
    c = TraefikCheck('traefik', {}, {}, None)

    HERE = os.path.dirname(os.path.abspath(__file__))
    args = [
        "docker-compose",
        "-f", os.path.join(HERE, 'docker-compose.yml')
    ]

    # start the Traefik container
    subprocess.check_call(args + ["up", "-d"])
    time.sleep(5)  # we should implement a better wait strategy :)

    local_ip = '127.0.0.1'

    instance = {
        'host': local_ip
    }

    requests.get('http://' + local_ip)

    c.check(instance)
    aggregator.assert_metric('traefik.total_count', value=1, tags=None)

    c.check(instance)
    aggregator.assert_metric('traefik.total_status_code_count', value=1, tags=['status_code:404'])

    # stop the container
    subprocess.check_call(args + ["down"])