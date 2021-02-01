import json
import requests
from datetime import datetime, timedelta, timezone
from dateutil.parser import parse
from datadog_checks.base.errors import CheckException
from datadog_checks.base import AgentCheck, ConfigurationError

API_URL = 'https://api.dev.appkeeper.sios.com/v2/'
AUTH_API_URL = API_URL + 'authorize'
EVENT_API_URL = API_URL + '{}/events'
INSTANCES_API_URL = API_URL + '{}/instances'

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

        # events
        events = call_events_api(account, token)
        recover_count = get_recover_count(events)

        # instances
        instances = call_instances_api(account, token)
        number_of_all_instances = len(instances)
        number_of_monitored_instances = get_instances_number(instances)

        # send data
        # self.gauge('appkeeper.api_recover_count', recover_count)
        # self.gauge('appkeeper.integrated_instances', 1)
        # self.gauge('appkeeper.all_instances', 3)

def call_events_api(account, token):
    eventsJson = call_api_get(EVENT_API_URL.format(account), token)
    return eventsJson['events']

def call_instances_api(account, token):
    instancesJson = call_api_get(INSTANCES_API_URL.format(account), token)
    return instancesJson['instances']

def call_api_get(url, token):
    try:
        headers = {'Authorization' :'Bearer {}'.format(token)}
        response = requests.get(url, headers=headers)
    except requests.exceptions.Timeout:
        raise CheckException('Failed to get {} by timeout'.format(key))
    except Exception as e:
        raise CheckException('Failed to get {} by {}'.format(key, e))

    if response.status_code != 200:
        raise ConfigurationError('Failed to get {}. status_code={}'.format(key, response.status_code))

    try:
        resultsJson = json.loads(response.text)
    except Exception as e:
        raise CheckException('Failed to get {} by {}'.format(key, e))

    return resultsJson


def get_recover_count(events):
    filtered_api = list(filter(lambda x: x['requester'] == 'api', events))
    filtered = list(filter(isInLastOneHour, filtered_api))
    return len(filtered)

def isInLastOneHour(event, now=datetime.now(timezone.utc)):
    oneHourAgo = now - timedelta(hours=1)
    eventHour = parse(event['startTime'])
    return oneHourAgo < eventHour

def get_instances_number(instances):
    return len(list(filter(lambda x: x['state'] == 'monitoring', instances)))