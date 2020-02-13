# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import requests
from six import iteritems

from datadog_checks.base import AgentCheck, ConfigurationError


class TraefikCheck(AgentCheck):
    def check(self, instance):
        host = instance.get('host')
        port = instance.get('port', '8080')
        path = instance.get('path', '/health')
        scheme = instance.get('scheme', 'http')

        if not host:
            self.warning('Configuration error, you must define `host`')
            raise ConfigurationError('Configuration error, you must define `host`')

        try:
            url = '{}://{}:{}{}'.format(scheme, host, port, path)
            response = requests.get(url)
            response_status_code = response.status_code

            if response_status_code == 200:
                self.service_check('traefik.health', self.OK)

                payload = response.json()

                if 'total_status_code_count' in payload:
                    status_code_counts = payload['total_status_code_count']

                    for status_code, count in iteritems(status_code_counts):
                        self.gauge('traefik.total_status_code_count', count, ['status_code:{}'.format(status_code)])

                else:
                    self.log.warning('Field total_status_code_count not found in response.')

                if 'total_count' in payload:
                    self.gauge('traefik.total_count', payload['total_count'])
                else:
                    self.log.warning('Field total_count not found in response.')

            else:
                self.service_check(
                    'traefik.health', self.CRITICAL, message='Traefik health check return code is not 200'
                )

        except requests.exceptions.ConnectionError:
            self.service_check('traefik.health', self.CRITICAL, message='Traefik endpoint unreachable')

        except Exception as e:
            self.service_check('traefik.health', self.UNKNOWN, message='UNKNOWN exception: {}'.format(e))
