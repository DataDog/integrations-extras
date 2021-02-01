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
        
        # Get Recovery Events
        try:
            headers = {'Authorization' :'Bearer {}'.format(token)}
            response = requests.get(EVENT_API_URL.format(account), headers=headers)
        except requests.exceptions.Timeout:
            raise CheckException('Failed to get events by timeout')
        except Exception as e:
            raise CheckException('Failed to get events by {}'.format(e))

        if response.status_code != 200:
            raise ConfigurationError('Failed to get events. status_code={}'.format(response.status_code))

        try:
            eventsJson = json.loads(response.text)
            events = eventsJson['events']
        except Exception as e:
            raise CheckException('Failed to get events by {}'.format(e))

        # filter events
        # get the number of events form 'api' in the last 1 hours
        recover_count = get_recover_count(events)

        # Get Instances
        try:
            headers = {'Authorization' :'Bearer {}'.format(token)}
            response = requests.get(INSTANCES_API_URL.format(account), headers=headers)
        except requests.exceptions.Timeout:
            raise CheckException('Failed to get instances by timeout')
        except Exception as e:
            raise CheckException('Failed to get instances by {}'.format(e))

        if response.status_code != 200:
            raise ConfigurationError('Failed to get instances. status_code={}'.format(response.status_code))

        try:
            instancesJson = json.loads(response.text)
            instances = instancesJson['instances']
        except Exception as e:
            raise CheckException('Failed to get instances by {}'.format(e))

        # get the number of all instances
        all_instances = len(instances)

        # filter instances
        # get the number of monitored instances
        monitored_instances = get_instances_number(instances)

        # send data
        # self.gauge('appkeeper.api_recover_count', recover_count)
        # self.gauge('appkeeper.integrated_instances', 1)
        # self.gauge('appkeeper.all_instances', 3)

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