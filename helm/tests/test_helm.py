import base64
import json
from gzip import compress

import mock
from kubernetes.client.models.v1_list_meta import V1ListMeta
from kubernetes.client.models.v1_object_meta import V1ObjectMeta
from kubernetes.client.models.v1_secret import V1Secret
from kubernetes.client.models.v1_secret_list import V1SecretList

from datadog_checks.helm import HelmCheck


class MockConfig:
    @staticmethod
    def load_incluster_config():
        pass


class MockClient:
    @staticmethod
    def CoreV1Api():
        return MockClient()

    def list_secret_for_all_namespaces(self, label_selector=''):
        if label_selector != 'owner=helm':
            raise BaseException("Unexpected label")
        return V1SecretList(items=[MockClient.example_item1(), MockClient.example_item2()], metadata=V1ListMeta())

    @staticmethod
    def example_item1():
        example_content = {
            'name': 'external-dns-custom-chart',
            'version': 5,
            'info': {'status': 'deployed', 'last_deployed': 126},
            'chart': {'metadata': {'name': 'external-dns', 'version': '2.15.3'}},
        }
        compressed_content = compress(json.dumps(example_content).encode("utf-8"))
        return V1Secret(
            data={'release': base64.b64encode(base64.b64encode(compressed_content))},
            metadata=V1ObjectMeta(namespace='external-dns-ns'),
        )

    @staticmethod
    def example_item2():
        example_content = {
            'name': 'external-dns-custom-chart',
            'version': 4,
            'info': {'status': 'superseded', 'last_deployed': 123},
            'chart': {'metadata': {'name': 'external-dns', 'version': '2.15.2'}},
        }
        compressed_content = compress(json.dumps(example_content).encode("utf-8"))
        return V1Secret(
            data={'release': base64.b64encode(base64.b64encode(compressed_content))},
            metadata=V1ObjectMeta(namespace='external-dns-ns'),
        )


def test_check(aggregator, instance):
    """
    If you want to run the test_check locally against your kubeconfig file
    just to verify parsing, you can copy/paste this to remove the mock

    check = HelmCheck('helm', {}, [instance])
    check.check(instance)
"""
    with mock.patch('kubernetes.config.load_incluster_config', MockConfig.load_incluster_config):
        with mock.patch('kubernetes.client.CoreV1Api', MockClient.CoreV1Api):
            check = HelmCheck('helm', {}, [instance])
            check.check(instance)
    tags = ['chart_name:external-dns', 'kube_namespace:external-dns-ns', 'release_name:external-dns-custom-chart']
    aggregator.assert_metric('helm.total_releases', count=1, metric_type=aggregator.GAUGE, value=1)
    aggregator.assert_metric('helm.managed_secrets', count=1, metric_type=aggregator.GAUGE, value=2)
    aggregator.assert_metric('helm.chart_status', count=1, metric_type=aggregator.GAUGE, value=1, tags=tags)
    aggregator.assert_metric('helm.chart_revision', count=1, metric_type=aggregator.GAUGE, value=5, tags=tags)

    aggregator.assert_all_metrics_covered()
