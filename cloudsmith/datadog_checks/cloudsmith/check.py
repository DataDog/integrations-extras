from json import JSONDecodeError
from urllib.error import HTTPError

import requests
from requests.exceptions import InvalidURL, Timeout

from datadog_checks.base import AgentCheck, ConfigurationError

METRIC_URL = "/metrics/entitlements/"
VULNERABILITIES = "/vulnerabilities/"
QUOTA = "/quota/"
TIMEOUT = 10
WARNING_QUOTA = 75
CRITICAL_QUOTA = 85


class CloudsmithCheck(AgentCheck):
    def __init__(self, name, init_config, instance):
        super(CloudsmithCheck, self).__init__(name, init_config, instance)

        self.base_url = self.instance.get('url')
        self.api_key = self.instance.get('cloudsmith_api_key')
        self.org = self.instance.get('organization')

        self.log.debug('Cloudsmith monitoring starting on %s', self.base_url)

    def get_full_path(self, path):
        url = self.base_url + path + self.org
        return url

    # Get stats from REST API as json
    def get_api_info(self, url):
        try:
            key = self.api_key
            headers = {"X-Api-Key": key, "content-type": "application/json"}
            req = requests.get(url, timeout=TIMEOUT, headers=headers)
        except Timeout as e:
            self.service_check(
                "cloudsmith.can_connect",
                AgentCheck.CRITICAL,
                message="Request timeout: {}, {}".format(url, e),
            )
            raise

        except (HTTPError, InvalidURL, ConnectionError) as e:
            self.service_check(
                "cloudsmith.can_connect",
                AgentCheck.CRITICAL,
                message="Request failed: {}, {}".format(url, e),
            )
            raise

        except JSONDecodeError as e:
            self.service_check(
                "cloudsmith.can_connect",
                AgentCheck.CRITICAL,
                message="JSON Parse failed: {}, {}".format(url, e),
            )
            raise

        except ValueError as e:
            self.service_check("cloudsmith.can_connect", AgentCheck.CRITICAL, message=str(e))
            raise

        return req.json()

    def get_usage_info(self):
        url = self.get_full_path(QUOTA)
        response_json = self.get_api_info(url)
        return response_json

    def get_vulnerability_info(self):
        url = self.get_full_path(VULNERABILITIES)
        response_json = self.get_api_info(url)
        return response_json

    def get_parsed_usage_info(self):
        response_json = self.get_usage_info()
        storage_used = response_json['usage']['raw']['storage']['percentage_used']
        bandwidth_used = response_json['usage']['raw']['bandwidth']['percentage_used']

        storage_mark = self.OK
        bandwidth_mark = self.OK

        if storage_used >= CRITICAL_QUOTA:
            storage_mark = self.CRITICAL
        elif storage_used >= WARNING_QUOTA:
            storage_mark = self.WARNING

        if bandwidth_used >= CRITICAL_QUOTA:
            bandwidth_used = self.CRITICAL
        elif bandwidth_used >= WARNING_QUOTA:
            bandwidth_used = self.WARNING

        usage_info = {
            'storage_mark': storage_mark,
            'storage_used': storage_used,
            'bandwidth_mark': bandwidth_mark,
            'bandwidth_used': bandwidth_used,
        }
        return usage_info

    def get_parsed_vulnerability_info(self):
        response_json = self.get_vulnerability_info()
        package_count = len(response_json)
        vulnerability_at_least_high_count = 0
        total_vulnerabilities = 0

        for package in response_json:
            if 'has_vulnerabilities' in package:
                total_vulnerabilities += package['num_vulnerabilities']
                print("package['max_severity']: {}".format(package['max_severity']))
                if package['max_severity'] in {'Critical', 'High'}:
                    vulnerability_at_least_high_count += 1

        vulnerability_info = {
            'package_count': package_count,
            'vulnerability_at_least_high_count': vulnerability_at_least_high_count,
            'total_vulnerabilities': total_vulnerabilities,
        }

        print("vulnerability infor: {}".format(vulnerability_info))
        return vulnerability_info

    def check(self, instance):
        # Use self.instance to read the check configuration
        if not self.api_key:
            raise ConfigurationError('Configuration error, please specify api token in conf.yaml.')

        if not self.org:
            raise ConfigurationError('Configuration error, please specify org in conf.yaml.')

        if not self.base_url:
            raise ConfigurationError('Configuration error, please specify Cloudsmith url in conf.yaml')

        vulnerability_count = 0
        usage_info = {
            'storage_mark': self.UNKNOWN,
            'storage_value': -1,
            'bandwidth_mark': self.UNKNOWN,
            'bandwidth_value': -1,
        }

        # Perform HTTP Requests with our HTTP wrapper.
        # More info at https://datadoghq.dev/integrations-core/base/http/

        vulnerability_info = self.get_parsed_vulnerability_info()
        if 'vulnerability_at_least_high_count' in vulnerability_info:
            vulnerability_count = vulnerability_info['vulnerability_at_least_high_count']

        usage_info = self.get_parsed_usage_info()

        # This is how you submit metrics
        # There are different types of metrics that you can submit (gauge, event).
        # More info at https://datadoghq.dev/integrations-core/base/api/#datadog_checks.base.checks.base.AgentCheck
        self.gauge("cloudsmith.vulnerability_count", vulnerability_count, tags=[vulnerability_info])

        self.service_check(
            'cloudsmith.storage',
            usage_info['storage_mark'],
            message="Percentage storaged used: {}%".format(usage_info['storage_used']),
        )
