import base64
import json
from gzip import decompress

from kubernetes import client, config

from datadog_checks.base import AgentCheck

# Values to mirror https://github.com/sstarcher/helm-exporter/blob/master/main.go#L50
# Makes for easier migration
STATUS_MAP = {
    "unknown": 0,
    "deployed": 1,
    "uninstalled": 2,
    "superseded": 3,
    "failed": -1,
    "uninstalling": 5,
    "pending-install": 6,
    "pending-upgrade": 7,
    "pending-rollback": 8,
}


class HelmCheck(AgentCheck):
    __NAMESPACE__ = 'helm'

    def __init__(self, *args, **kwargs):
        config.load_incluster_config()
        self.v1 = client.CoreV1Api()
        AgentCheck.__init__(self, *args, **kwargs)

    def check(self, instance):
        # The command kubectl  get secret -l owner=helm --field-selector 'type=helm.sh/release.v1' -A
        all_releases = self.v1.list_secret_for_all_namespaces(label_selector='owner=helm')
        self.gauge("managed_secrets", len(all_releases.items))
        # kubectl get secrets  XYZ -o yaml | yq read - data.release |
        #   base64 --decode | base64 --decode | gunzip | yq read - info
        latest_release = {}
        for item in all_releases.items:
            # Mostly reverse engineered from
            # https://github.com/helm/helm/blob/88f42929d779e145b24dad12657d6984d755dd2c/pkg/storage/driver/util.go#L56
            release = item.data['release']
            # Yo dawg, I heard you like b64decode
            decoded_release = base64.b64decode(release)
            compressed_content = base64.b64decode(decoded_release)
            # gzip.decompress won't exist in python 2
            try:
                content = decompress(compressed_content)
            except Exception:
                # helm code has this optional
                pass
            content = json.loads(content)
            res = {
                'chart_name': content['chart']['metadata']['name'],
                'release_name': content['name'],
                'release_version': int(content['version']),
                'status': content['info']['status'],
                'namespace': item.metadata.namespace,
                'key': "%s/%s" % (item.metadata.namespace, content['name']),
            }
            key = res['key']
            if key not in latest_release:
                latest_release[key] = res
            else:
                if latest_release[key]['release_version'] < res['release_version']:
                    latest_release[key] = res
        self.gauge("total_releases", len(latest_release))
        for release in latest_release.values():
            tags = []
            # kube_namespace terminology taken from other datadog metrics
            tags.append("kube_namespace:%s" % release['namespace'])
            # Unclear if I should call this 'chart_name' or just 'chart'
            tags.append("chart_name:%s" % release['chart_name'])
            tags.append("release_name:%s" % release['release_name'])
            status_num = STATUS_MAP.get(release['status'], 0)

            # Using the terminology of `helm list` the names are status/revision
            self.gauge("chart_status", status_num, tags=tags)
            self.gauge("chart_revision", release['release_version'], tags=tags)
