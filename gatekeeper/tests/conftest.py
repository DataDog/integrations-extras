# (C) Datadog, Inc. 2021-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import os

import pytest

from datadog_checks.dev import run_command
from datadog_checks.dev.kind import kind_run
from datadog_checks.dev.kube_port_forward import port_forward

try:
    from contextlib import ExitStack
except ImportError:
    from contextlib2 import ExitStack


HERE = os.path.dirname(os.path.abspath(__file__))
HEALTH_PORT = 9090
METRICS_PORT = 8888


def setup_cert_manager():
    run_command(
        [
            "kubectl",
            "apply",
            "-f",
            "https://raw.githubusercontent.com/open-policy-agent/gatekeeper/release-3.3/deploy/gatekeeper.yaml",
        ]
    )
    run_command(
        [
            "kubectl",
            "wait",
            "deployments",
            "--all",
            "--for=condition=Available",
            "-n",
            "gatekeeper-system",
            "--timeout=300s",
        ]
    )
    run_command(
        ["kubectl", "wait", "pods", "-n", "gatekeeper-system", "--all", "--for=condition=Ready", "--timeout=300s"]
    )
    config = os.path.join(HERE, 'kubernetes', 'constrainttemplate.yaml')
    run_command(["kubectl", "create", "-f", config])
    run_command(["kubectl", "wait", "constrainttemplate", "--all", "--for=condition=Ready", "--timeout=300s"])
    config = os.path.join(HERE, 'kubernetes', 'constraintsample.yaml')
    run_command(["kubectl", "create", "-f", config])


@pytest.fixture(scope='session')
def dd_environment():
    with kind_run(conditions=[setup_cert_manager]) as kubeconfig:
        with ExitStack() as stack:
            ip_ports_metrics = [
                stack.enter_context(
                    port_forward(
                        kubeconfig, 'gatekeeper-system', METRICS_PORT, 'deployment', 'gatekeeper-controller-manager'
                    )
                )
            ]
            ip_ports_health = [
                stack.enter_context(
                    port_forward(
                        kubeconfig, 'gatekeeper-system', HEALTH_PORT, 'deployment', 'gatekeeper-controller-manager'
                    )
                )
            ]

        instances = {
            'instances': [
                {
                    'prometheus_url': 'http://{}:{}/metrics'.format(*ip_ports_metrics[0]),
                    'gatekeeper_health_endpoint': 'http://{}:{}/'.format(*ip_ports_health[0]),
                },
            ]
        }

        yield instances


@pytest.fixture
def instance():
    return {}
