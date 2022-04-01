from typing import Any

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

    def __check_folders(self, tags):
        folders = [f['id'] for f in self.__get_json('config/folders')]
        for folder in folders:
            s = self.__get_json('db/status?folder=' + folder)

            ft = tags + ('folder:' + folder,)

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

            self.gauge('folder.errors', int(s['errors']), tags=ft)
            self.gauge('folder.pull_errors', int(s['pullErrors']), tags=ft)
            self.gauge('folder.bytes', int(s['inSyncBytes']), tags=ft)
            self.gauge('folder.files', int(s['inSyncFiles']), tags=ft)

    def __check_errors(self, tags):
        res = self.__get_json('system/error')['errors']
        count = 0
        if res is not None:
            count = len(res)
        self.gauge('errors', count, tags=tags)

    def check(self, _):
        # type: (Any) -> None

        try:
            tags = self.__get_tags()
            self.__check_connections(tags)
            self.__check_folders(tags)
            self.__check_errors(tags)

            self.service_check('can_connect', AgentCheck.OK)
        except Timeout as e:
            self.service_check(
                'can_connect',
                AgentCheck.CRITICAL,
                message='Request timeout: {}, {}'.format(self.url, e),
            )
            raise

        except (HTTPError, InvalidURL, ConnectionError) as e:
            self.service_check(
                'can_connect',
                AgentCheck.CRITICAL,
                message='Request failed: {}, {}'.format(self.url, e),
            )
            raise

        except JSONDecodeError as e:
            self.service_check(
                'can_connect',
                AgentCheck.CRITICAL,
                message='JSON Parse failed: {}, {}'.format(self.url, e),
            )
            raise

        except ValueError as e:
            self.service_check('can_connect', AgentCheck.CRITICAL, message=str(e))
            raise

        self.service_check('can_connect', AgentCheck.CRITICAL)
