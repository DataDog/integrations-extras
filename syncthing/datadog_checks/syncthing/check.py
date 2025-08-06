from datetime import datetime
from typing import Any  # noqa: F401

from requests.exceptions import ConnectionError, HTTPError, InvalidURL, Timeout
from simplejson import JSONDecodeError

from datadog_checks.base import AgentCheck


class SyncthingCheck(AgentCheck):
    # This will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = 'syncthing'

    def __init__(self, name, init_config, instances):
        super(SyncthingCheck, self).__init__(name, init_config, instances)

        self.url = self.instance.get('url')
        self.api_key = self.instance.get('api_key')

    def __get_json(self, url_path):
        response = self.http.get(self.url + url_path, headers={'X-API-Key': self.api_key})
        response.raise_for_status()
        return response.json()

    def __get_tags(self):
        version = self.__get_json('system/version')
        status = self.__get_json('system/status')
        return (
            'arch:' + version['arch'],
            'os:' + version['os'],
            'syncthing_version:' + version['version'],
            'syncthing_id:' + status['myID'],
        )

    def __check_connections(self, tags):
        res = self.__get_json('system/connections')
        connected = 0
        paused = 0
        connections = res['connections']
        for c in connections.values():
            if c['connected']:
                connected += 1
            if c['paused']:
                paused += 1
        self.gauge('connections.connected', connected, tags=tags)
        self.gauge('connections.paused', paused, tags=tags)
        self.gauge('connections.count', len(connections), tags=tags)

    def __get_delta(self, now, val):
        # remove timezone info since python2 has no native support
        return (now - datetime.strptime(val[:19], "%Y-%m-%dT%H:%M:%S")).total_seconds()

    def __check_device_stats(self, tags):
        names = {d['deviceID']: d['name'] for d in self.__get_json('config/devices')}
        devices = self.__get_json('stats/device')
        now = datetime.now()

        for d, v in devices.items():
            if v['lastConnectionDurationS'] == 0:
                # skip local and never connected devices
                continue

            dt = tags + ('device_id:' + d, 'device_name:' + names[d])

            self.gauge('stats.device.last_seen', self.__get_delta(now, v['lastSeen']), tags=dt)
            self.gauge('stats.device.last_connection_duration', v['lastConnectionDurationS'], tags=dt)

    def __check_folders(self, tags):
        folders = [(f['id'], f['type']) for f in self.__get_json('config/folders')]
        folders_stat = self.__get_json('stats/folder')
        now = datetime.now()

        for folder, tp in folders:
            s = self.__get_json('db/status?folder=' + folder)

            ft = tags + ('folder:' + folder, 'type:' + tp)

            self.gauge('folder.global.bytes', int(s['globalBytes']), tags=ft)
            self.gauge('folder.global.deleted', int(s['globalDeleted']), tags=ft)
            self.gauge('folder.global.directories', int(s['globalDirectories']), tags=ft)
            self.gauge('folder.global.files', int(s['globalFiles']), tags=ft)
            self.gauge('folder.global.total_items', int(s['globalTotalItems']), tags=ft)
            self.gauge('folder.local.bytes', int(s['localBytes']), tags=ft)
            self.gauge('folder.local.deleted', int(s['localDeleted']), tags=ft)
            self.gauge('folder.local.directories', int(s['localDirectories']), tags=ft)
            self.gauge('folder.local.files', int(s['localFiles']), tags=ft)
            self.gauge('folder.local.total_items', int(s['localTotalItems']), tags=ft)
            self.gauge('folder.need.bytes', int(s['needBytes']), tags=ft)
            self.gauge('folder.need.deletes', int(s['needDeletes']), tags=ft)
            self.gauge('folder.need.directories', int(s['needDirectories']), tags=ft)
            self.gauge('folder.need.files', int(s['needFiles']), tags=ft)
            self.gauge('folder.need.total_items', int(s['needTotalItems']), tags=ft)

            self.count('folder.errors', int(s['errors']), tags=ft)
            self.count('folder.pull_errors', int(s['pullErrors']), tags=ft)
            self.gauge('folder.bytes', int(s['inSyncBytes']), tags=ft)
            self.gauge('folder.files', int(s['inSyncFiles']), tags=ft)

            self.gauge('folder.last_scan', self.__get_delta(now, folders_stat[folder]['lastScan']), tags=ft)

    def __check_errors(self, tags):
        res = self.__get_json('system/error')['errors']
        count = 0
        if res is not None:
            count = len(res)
        self.count('errors', count, tags=tags)

    def check(self, _):
        # type: (Any) -> None

        try:
            tags = self.__get_tags()
            self.__check_connections(tags)
            self.__check_device_stats(tags)
            self.__check_folders(tags)
            self.__check_errors(tags)

            self.service_check('can_connect', AgentCheck.OK)
        except Timeout as e:
            self.service_check(
                'can_connect',
                AgentCheck.CRITICAL,
                message='Request timeout: {}, {}'.format(self.url, e),
            )

        except (HTTPError, InvalidURL, ConnectionError) as e:
            self.service_check(
                'can_connect',
                AgentCheck.CRITICAL,
                message='Request failed: {}, {}'.format(self.url, e),
            )

        except JSONDecodeError as e:
            self.service_check(
                'can_connect',
                AgentCheck.CRITICAL,
                message='JSON Parse failed: {}, {}'.format(self.url, e),
            )

        except ValueError as e:
            self.service_check('can_connect', AgentCheck.CRITICAL, message=str(e))

        except BaseException as e:
            self.service_check('can_connect', AgentCheck.CRITICAL, message=str(e))
