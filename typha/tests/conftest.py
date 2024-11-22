# (C) Datadog, Inc. 2021-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import os

import pytest

from os import path
from datadog_checks.dev import run_command
from datadog_checks.dev.kind import kind_run
from datadog_checks.dev.kube_port_forward import port_forward

try:
    from contextlib import ExitStack
except ImportError:
    from contextlib2 import ExitStack


HERE = os.path.dirname(os.path.abspath(__file__))
HEALTH_PORT = 9098
METRICS_PORT = 9093


def setup_typha():
    # Deploy typha
    run_command(["kubectl", "apply", "-f", path.join(HERE, 'kind', 'typha.yaml')])

    # Wait for pods
    run_command(
        [
            "kubectl",
            "wait",
            "--for=condition=Ready",
            "pods",
            "--selector=k8s-app=calico-typha",
            "--all-namespaces",
            "--timeout=300s",
        ]
    )


@pytest.fixture(scope='session')
def dd_environment():
    with kind_run(
        conditions=[setup_typha], kind_config=path.join(HERE, 'kind', 'kind-typha.yaml'), sleep=10
    ) as kubeconfig:
        with ExitStack() as stack:
            ip_ports_metrics = [
                stack.enter_context(port_forward(kubeconfig, 'kube-system', METRICS_PORT, 'service', 'calico-typha'))
            ]

        instances = {
            'instances': [
                {
                    'prometheus_url': 'http://{}:{}/metrics'.format(*ip_ports_metrics[0]),
                },
            ]
        }

        yield instances


@pytest.fixture
def instance():
    return {}
