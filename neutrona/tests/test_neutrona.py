import os
import subprocess
import time

import pytest

from datadog_checks.base.errors import CheckException
from datadog_checks.neutrona import NeutronaCheck


def test_config():
    c = NeutronaCheck('neutrona', {}, {}, None)

    # empty instance
    instance = {}

    with pytest.raises(CheckException):
        c.check(instance)

    # unable to authenticate
    instance = {
        "azure": {"directory_id": "", "application_id": "", "application_key": "", "domain": "", "subscription_id": ""}
    }

    with pytest.raises(CheckException):
        c.check(instance)


@pytest.mark.integration
def test_metrics(aggregator):
    if os.getenv('APPVEYOR', 'false').lower() != "true":
        c = NeutronaCheck('neutrona', {}, {}, None)

        pwd = os.path.dirname(os.path.abspath(__file__))
        args = ["docker-compose", "-f", os.path.join(pwd, 'docker-compose.yml')]

        # start API mock containers
        subprocess.check_call(args + ["up", "-d"])
        time.sleep(60)  # we should implement a better wait strategy :)

        # should pass
        instance = {
            "azure": {
                "directory_id": "my_directory_id",
                "application_id": "my_application_id",
                "application_key": "my_application_key",
                "domain": "my_domain.com",
                "subscription_id": "my_subscription_id",
                "testing": {
                    "neutrona_express_route_api_url": "http://localhost:65000/",
                    "azure_authentication_url": "http://localhost:65001",
                    "azure_management_url": "http://localhost:65002/",
                },
            }
        }

        c.check(instance)

        connections = [
            {
                "egress_bps": 0,
                "egress_interface_errors": False,
                "ingress_bps": 0,
                "ingress_interface_errors": False,
                "output_optical_power": 0,
                "receiver_optical_power": 0,
                "tags": ["primary", "ctag_500"],
            },
            {"tags": ["performance"]},
            {
                "egress_bps": 0,
                "egress_interface_errors": False,
                "ingress_bps": 0,
                "ingress_interface_errors": False,
                "output_optical_power": 0,
                "receiver_optical_power": 0,
                "tags": ["secondary", "ctag_500"],
            },
        ]

        for conn in connections:
            for metric, value in conn.items():
                if metric != 'tags':
                    aggregator.assert_metric(
                        name='.'.join(['neutrona', 'azure', 'expressroute', metric]),
                        value=value,
                        tags=conn['tags'],
                        count=None,
                        at_least=1,
                        hostname='my_service_key',
                        metric_type=aggregator.GAUGE,
                    )
