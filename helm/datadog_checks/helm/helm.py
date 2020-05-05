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
        super(HelmCheck, self).__init__(*args, **kwargs)

    def dump_all_secrets(self):
        # The command kubectl  get secret -l owner=helm -A
        # https://github.com/helm/helm/blob/1911870958098b774973c6fe56bfdf4441f61596/pkg/storage/driver/secrets.go#L82
        all_releases = self.v1.list_secret_for_all_namespaces(label_selector='owner=helm')
        ret = []
        while all_releases.metadata._continue is not None:
            ret.extend(all_releases.items)
            all_releases = self.v1.list_secret_for_all_namespaces(
                label_selector='owner=helm', _continue=all_releases.metadata._continue
            )
        ret.extend(all_releases.items)
        return ret

    def build_result(self, item):
        # Mostly reverse engineered from
        # https://github.com/helm/helm/blob/88f42929d779e145b24dad12657d6984d755dd2c/pkg/storage/driver/util.go#L56
        release = item.data['release']
        # Yo dawg, I heard you like b64decode
        decoded_release = base64.b64decode(release)
        compressed_content = base64.b64decode(decoded_release)
        try:
            # Note: gzip.decompress won't exist in python 2
            content = decompress(compressed_content)
        except Exception:
            # In helm, the content does not have to be gzip encoded
            pass
        content = json.loads(content)
        return {
            'chart_name': content.get('chart', {}).get('metadata', {}).get('name'),
            'release_name': content.get('name'),
            'release_version': int(content.get('version', -1)),
            'status': content.get('info', {}).get('status'),
            'namespace': item.metadata.namespace,
            'key': "%s/%s" % (item.metadata.namespace, content.get('name')),
        }

    def check(self, instance):
        custom_tags = instance.get('tags', [])
        if custom_tags is None:
            custom_tags = []
        else:
            custom_tags = list(set(custom_tags))
        all_releases = self.dump_all_secrets()
        self.gauge("managed_secrets", len(all_releases), tags=custom_tags)
        # To debug a release, try this from the CLI:
        #   kubectl get secrets  XYZ -o yaml | yq read - data.release | \
        #     base64 --decode | base64 --decode | gunzip | yq read - info
        latest_release = {}
        for item in all_releases:
            res = self.build_result(item)
            key = res['key']
            # https://github.com/helm/helm/blob/1911870958098b774973c6fe56bfdf4441f61596/pkg/action/list.go#L226
            if key not in latest_release:
                latest_release[key] = res
            else:
                if latest_release[key]['release_version'] < res['release_version']:
                    latest_release[key] = res
        self.gauge("total_releases", len(latest_release))
        for release in latest_release.values():
            tags = []
            tags.extend(custom_tags)
            # kube_namespace terminology taken from other datadog metrics
            tags.append("kube_namespace:%s" % release['namespace'])
            tags.append("chart_name:%s" % release['chart_name'])
            tags.append("release_name:%s" % release['release_name'])
            status_num = STATUS_MAP.get(release['status'], 0)

            # Using the terminology of `helm list` the names are status/revision
            self.gauge("chart_status", status_num, tags=tags)
            self.gauge("chart_revision", release['release_version'], tags=tags)
