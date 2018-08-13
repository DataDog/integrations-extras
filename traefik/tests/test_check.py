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
    """
    Unit test to check:
        - all expected metrics are collected
        - expected exception are raised
    """

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
def test_service_check_critical(aggregator):
    """
    Unit test to check:
        - service_check return CRITICAL
    """

    c = TraefikCheck('traefik', {}, {}, None)

    local_ip = '127.0.0.1'

    instance = {
        'host': local_ip
    }

    c.check(instance)
    aggregator.assert_service_check('traefik.health', TraefikCheck.CRITICAL)


@pytest.mark.integration
@pytest.mark.usefixtures('spin_up_traefik')
def test_service_check_ok(aggregator):
    """
    Unit test to check:
        - service_check return OK
    """

    c = TraefikCheck('traefik', {}, {}, None)

    local_ip = '127.0.0.1'

    instance = {
        'host': local_ip
    }

    c.check(instance)
    aggregator.assert_service_check('traefik.health', TraefikCheck.OK)



@pytest.mark.integration
@pytest.mark.usefixtures('spin_up_traefik')
def test_collect_metrics(aggregator):
    """
    Unit test to check:
        - that we get metrics with the expected value and tag.
    """

    c = TraefikCheck('traefik', {}, {}, None)

    local_ip = '127.0.0.1'

    instance = {
        'host': local_ip
    }

    requests.get('http://' + local_ip)

    c.check(instance)
    aggregator.assert_metric('traefik.total_count', value=1, tags=None)

    c.check(instance)
    aggregator.assert_metric('traefik.total_status_code_count', value=1, tags=['status_code:404'])