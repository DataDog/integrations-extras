# (C) Datadog, Inc. 2022-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from json import JSONDecodeError
from typing import Any  # noqa: F401

from requests.exceptions import ConnectionError, HTTPError, InvalidURL, Timeout
from six.moves.urllib.parse import urljoin

from datadog_checks.base import AgentCheck, ConfigurationError


class CfsslCheck(AgentCheck):

    SERVICE_CHECK_CONNECT_NAME = 'cfssl.can_connect'
    SERVICE_CHECK_HEALTH_NAME = 'cfssl.health'

    HEALTH_ENDPOINT = "/api/v1/cfssl/health"

    def __init__(self, name, init_config, instances):
        super(CfsslCheck, self).__init__(name, init_config, instances)

    def check(self, _):
        # type: (Any) -> None
        url = self.instance.get("url")

        if not url:
            raise ConfigurationError('Configuration error, please fix cfssl.yaml')

        health_url = urljoin(url, self.HEALTH_ENDPOINT)

        try:
            response = self.http.get(health_url)
            response.raise_for_status()
            response_json = response.json()

        except Timeout as e:
            error_message = f"Request timeout: {health_url}, {e}"
            self.log.warning(error_message)
            self.service_check(self.SERVICE_CHECK_CONNECT_NAME, AgentCheck.CRITICAL, message=error_message)
            raise

        except (HTTPError, InvalidURL, ConnectionError) as e:
            error_message = f"Request failed: {health_url}, {e}"
            self.log.warning(error_message)
            self.service_check(self.SERVICE_CHECK_CONNECT_NAME, AgentCheck.CRITICAL, message=error_message)
            raise

        except JSONDecodeError as e:
            error_message = f"JSON Parse failed: {health_url}, {e}"
            self.log.warning(error_message)
            self.service_check(self.SERVICE_CHECK_CONNECT_NAME, AgentCheck.CRITICAL, message=error_message)
            raise

        except ValueError as e:
            self.service_check(self.SERVICE_CHECK_CONNECT_NAME, AgentCheck.CRITICAL, message=str(e))
            raise

        self.service_check(self.SERVICE_CHECK_CONNECT_NAME, AgentCheck.OK)

        if response_json['result']['healthy']:
            self.service_check(self.SERVICE_CHECK_HEALTH_NAME, AgentCheck.OK)

        else:
            self.service_check(self.SERVICE_CHECK_HEALTH_NAME, AgentCheck.CRITICAL)
