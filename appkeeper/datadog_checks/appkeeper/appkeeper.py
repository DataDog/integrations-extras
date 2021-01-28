import json
import requests
from datadog_checks.base.errors import CheckException
from datadog_checks.base import AgentCheck, ConfigurationError

API_URL = 'https://api.dev.appkeeper.sios.com/v2/'
AUTH_API_URL = API_URL + 'authorize'
EVENT_API_URL = API_URL + '{}/events'

class AppKeeperCheck(AgentCheck):
    def check(self, instance):
        account = instance.get('account')
        integrationToken = instance.get('integrationToken')

        if not account or not integrationToken:
            raise ConfigurationError('Configuration error, please fix conf.yaml')

        # Get API key
        try:
            response = requests.get(AUTH_API_URL + '?token=' + integrationToken)
        except requests.exceptions.Timeout:
            raise CheckException('Failed to get API key by timeout')
        except Exception as e:
            raise CheckException('Failed to get API key by {}'.format(e))

        if response.status_code != 200:
            raise ConfigurationError('Failed to get API key. status_code={}'.format(response.status_code))

        try:
            tokenJson = json.loads(response.text)
            token = tokenJson['accessToken']
        except Exception as e:
            raise CheckException('Failed to get API key by {}'.format(e))
        
        # Get Recovery Events
        try:
            headers = {'Authorization' :'Bearer {}'.format(token)}
            response = requests.get(EVENT_API_URL.format(account), headers=headers)
        except requests.exceptions.Timeout:
            raise CheckException('Failed to get API key by timeout')
        except Exception as e:
            raise CheckException('Failed to get API key by {}'.format(e))

        return response.text
        #
        # self.log.info(response)
        # self.gauge('appkeeper.api_recover_count', 0)
        # self.gauge('appkeeper.integrated_instances', 1)
        # self.gauge('appkeeper.all_instances', 3)
