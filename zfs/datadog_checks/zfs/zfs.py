from checks import AgentCheck
from datadog_checks.base.utils.subprocess_output import get_subprocess_output

zpool_metrics = [
    'size',
    'capacity',
    'allocated',
    'free',
    'fragmentation'
]

zpool_enums = [
    'health'
]

zfs_metrics = [
    'available',
    'compressratio',
    'used',
    'usedbychildren',
    'usedbydataset',
    'usedbyrefreservation',
    'usedbysnapshots'
]

zfs_status = {
    'ONLINE': 0,  # Ok
    'DEGRADED': 1,  # Warning
    'FAULTED': 2,  # Critical
    'OFFLINE': 2,  # Critical
    'REMOVED': 2,  # Critical
    'UNAVAIL': 2,  # Critical
}


class CheckValue(AgentCheck):
    def check(self, instance):

        zpool_headers = zpool_metrics + zpool_enums
        zpool_output, err, retcode = get_subprocess_output(
            ['zpool', 'list', '-H', '-p', '-o', ','.join(['name'] + zpool_headers)], self.log, raise_on_empty_output=True)
        if err:
            self.log.error(err)
            return

        for pool in zpool_output.split('\n'):
            name, *values = pool.split('\t')
            for key, value in zip(zpool_headers, values):
                if key in zpool_metrics:
                    self.gauge('zfs.pool.' + key, value, ['pool:' + name])
                if key in zpool_enums:
                    self.gauge('zfs.pool.' + key + '.' +
                               value.lower(), 1, ['pool:' + name])
                if key == 'health':
                    self.service_check('zfs.pool.health', zfs_status.get(
                        value, 3), tags=['pool:' + name], message=value)

        zfs_output, err, retcode = get_subprocess_output(
            ['zfs', 'list', '-H', '-p', '-o', ','.join(['name'] + zfs_metrics)], self.log, raise_on_empty_output=True)
        if err:
            self.log.error(err)
            return

        for ds in zfs_output.split('\n'):
            name, *values = ds.split('\t')
            for key, value in zip(zfs_metrics, values):
                self.gauge('zfs.dataset.' + key, value, ['dataset:' + name])
