from json import JSONDecodeError
from urllib.error import HTTPError

from requests.exceptions import InvalidURL, Timeout

from datadog_checks.base import AgentCheck, ConfigurationError
from datadog_checks.base.errors import CheckException

METRIC = "/metrics/entitlements/"
QUOTA = "/quota/"
WARNING_QUOTA = 75
CRITICAL_QUOTA = 85


class CloudsmithCheck(AgentCheck):
    __NAMESPACE__ = 'cloudsmith'

    def __init__(self, name, init_config, instances):
        super(CloudsmithCheck, self).__init__(name, init_config, instances)

        self.base_url = self.instance.get('url')
        self.api_key = self.instance.get('cloudsmith_api_key')
        self.org = self.instance.get('organization')

        self.validate_config()

        self.log.debug('Cloudsmith monitoring starting on %s', self.base_url)

        self.tags = self.instance.get('tags', [])
        self.tags.append('base_url:{}'.format(self.base_url))
        self.tags.append('cloudsmith_org:{}'.format(self.org))

    def validate_config(self):
        if not self.api_key:
            raise ConfigurationError('Configuration error, please specify api token in conf.yaml.')

        if not self.org:
            raise ConfigurationError('Configuration error, please specify org in conf.yaml.')

        if not self.base_url:
            raise ConfigurationError('Configuration error, please specify Cloudsmith url in conf.yaml')

    def get_full_path(self, path):
        url = self.base_url.rstrip('/') + path + self.org
        return url

    # Get stats from REST API as json
    def get_api_json(self, url):

        try:
            key = self.api_key
            headers = {"X-Api-Key": key, "content-type": "application/json"}
            response = self.http.get(url, headers=headers)
        except Timeout as e:
            error_message = "Request timeout: {}, {}".format(url, e)
            self.log.warning(error_message)
            self.service_check(
                "can_connect",
                AgentCheck.CRITICAL,
                message=error_message,
            )
            raise

        except (HTTPError, InvalidURL, ConnectionError) as e:
            error_message = "Request failed: {}, {}".format(url, e)
            self.log.warning(error_message)
            self.service_check(
                "can_connect",
                AgentCheck.CRITICAL,
                message=error_message,
            )
            raise

        except JSONDecodeError as e:
            error_message = "JSON Parse failed: {}, {}".format(url, e)
            self.log.warning(error_message)
            self.service_check(
                "can_connect",
                AgentCheck.CRITICAL,
                message=error_message,
            )
            raise

        except ValueError as e:
            error_message = str(e)
            self.log.warning(error_message)
            self.service_check("can_connect", AgentCheck.CRITICAL, message=error_message)
            raise

        if response.status_code != 200:
            error_message = (
                "Expected status code 200 for url {}, but got status code: {} check your config information".format(
                    url, response.status_code
                )
            )
            self.log.warning(error_message)
            self.service_check("can_connect", AgentCheck.CRITICAL, message=error_message)
            raise CheckException(error_message)
        else:
            self.service_check("can_connect", AgentCheck.OK)

        return response.json()

    def get_usage_info(self):
        url = self.get_full_path(QUOTA)
        response_json = self.get_api_json(url)
        return response_json

    def get_entitlement_info(self):
        url = self.get_full_path(METRIC)
        response_json = self.get_api_json(url)
        return response_json

    def get_parsed_entitlement_info(self):
        token_count = -1
        bandwidth_total = -1
        download_total = -1

        response_json = self.get_entitlement_info()

        if 'tokens' in response_json:
            if 'total' in response_json['tokens']:
                token_count = response_json['tokens']['total']
            else:
                self.log.warning("Error when parsing JSON for total token usage")
            if (
                'bandwidth' in response_json['tokens']
                and 'total' in response_json['tokens']['bandwidth']
                and 'value' in response_json['tokens']['bandwidth']['total']
            ):
                bandwidth_total = response_json['tokens']['bandwidth']['total']['value']
            else:
                self.log.warning("Error when parsing JSON for total token bandwidth usage")
            if (
                'downloads' in response_json['tokens']
                and 'total' in response_json['tokens']['downloads']
                and 'value' in response_json['tokens']['downloads']['total']
            ):
                download_total = response_json['tokens']['downloads']['total']['value']
            else:
                self.log.warning("Error when parsing JSON for total token download usage")
        else:
            self.log.warning("Error when parsing JSON for tokens")

        entitlement_info = {
            'token_count': token_count,
            'token_bandwidth_total': bandwidth_total,
            'token_download_total': download_total,
        }
        return entitlement_info

    def get_parsed_usage_info(self):
        response_json = self.get_usage_info()

        storage_used = -1
        bandwidth_used = -1
        storage_mark = self.UNKNOWN
        bandwidth_mark = self.UNKNOWN

        if 'usage' in response_json and 'raw' in response_json['usage']:
            if (
                'storage' in response_json['usage']['raw']
                and 'percentage_used' in response_json['usage']['raw']['storage']
            ):
                storage_used = response_json['usage']['raw']['storage']['percentage_used']
                storage_mark = self.OK
            else:
                self.log.warning("Error when parsing JSON for storage usage")
            if (
                'bandwidth' in response_json['usage']['raw']
                and 'percentage_used' in response_json['usage']['raw']['bandwidth']
            ):
                bandwidth_used = response_json['usage']['raw']['bandwidth']['percentage_used']
                bandwidth_mark = self.OK
            else:
                self.log.warning("Error when parsing JSON for bandwidth usage")
        else:
            self.log.warning("Error while parsing JSON for usage information")

        if storage_mark == self.OK:
            if storage_used >= CRITICAL_QUOTA:
                storage_mark = self.CRITICAL
            elif storage_used >= WARNING_QUOTA:
                storage_mark = self.WARNING

        if bandwidth_mark == self.OK:
            if bandwidth_used >= CRITICAL_QUOTA:
                bandwidth_mark = self.CRITICAL
            elif bandwidth_used >= WARNING_QUOTA:
                bandwidth_mark = self.WARNING

        usage_info = {
            'storage_mark': storage_mark,
            'storage_used': storage_used,
            'bandwidth_mark': bandwidth_mark,
            'bandwidth_used': bandwidth_used,
        }
        return usage_info

    def check(self, _):

        # Perform HTTP Requests with our HTTP wrapper.
        # More info at https://datadoghq.dev/integrations-core/base/http/

        usage_info = {
            'storage_mark': CloudsmithCheck.UNKNOWN,
            'storage_used': -1,
            'bandwidth_mark': CloudsmithCheck.UNKNOWN,
            'bandwidth_used': -1,
        }
        entitlement_info = {
            'token_count': -1,
            'token_bandwidth_total': -1,
            'token_download_total': -1,
        }

        usage_info = self.get_parsed_usage_info()
        entitlement_info = self.get_parsed_entitlement_info()

        # This is how you submit metrics
        # There are different types of metrics that you can submit (gauge, event).
        # More info at https://datadoghq.dev/integrations-core/base/api/#datadog_checks.base.checks.base.AgentCheck

        self.gauge("storage_used", usage_info['storage_used'], tags=self.tags)
        self.gauge("bandwidth_used", usage_info['bandwidth_used'], tags=self.tags)
        self.gauge("token_count", entitlement_info['token_count'], tags=self.tags)
        self.gauge("token_bandwidth_total", entitlement_info['token_bandwidth_total'], tags=self.tags)
        self.gauge("token_download_total", entitlement_info['token_download_total'], tags=self.tags)

        storage_msg = "Percentage storage used: {}%".format(usage_info['storage_used'])
        self.service_check(
            'storage',
            usage_info['storage_mark'],
            message=storage_msg if usage_info['storage_mark'] != AgentCheck.OK else "",
        )

        bandwith_msg = "Percentage bandwidth used: {}%".format(usage_info['bandwidth_used'])
        self.service_check(
            'bandwidth',
            usage_info['bandwidth_mark'],
            message=bandwith_msg if usage_info['bandwidth_mark'] != AgentCheck.OK else "",
        )
