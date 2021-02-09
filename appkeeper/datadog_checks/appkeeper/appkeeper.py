import json
import requests
from datetime import datetime, timedelta, timezone
from dateutil.parser import parse
from datadog_checks.base.errors import CheckException
from datadog_checks.base import AgentCheck, ConfigurationError

API_URL = 'https://api.appkeeper.sios.com/v2/'
AUTH_API_URL = API_URL + 'authorize'
EVENT_API_URL = API_URL + '{}/events'
INSTANCES_API_URL = API_URL + '{}/instances'

class AppKeeperCheck(AgentCheck):
    def check(self, instance, now=None):
        account = instance.get('account')
        integrationToken = instance.get('integrationToken')

        if not account or not integrationToken:
            raise ConfigurationError('Configuration error, please fix conf.yaml')

        token = self.get_token(integrationToken)

        # events
        events = self.get_events(account, token)
        if now == None:
            now = datetime.now(timezone.utc)
        recover_count = get_recover_count(events, now)

        # instances
        instances = self.get_instances(account, token)
        number_of_all_instances = len(instances)
        number_of_monitored_instances = get_monitoring_instances_number(instances)

        # send data
        self.gauge('appkeeper.api_recover_count', recover_count)
        self.gauge('appkeeper.monitored_instances', number_of_monitored_instances)
        self.gauge('appkeeper.all_instances', number_of_all_instances)

    def get_token(self, integrationToken):
        return call_auth_api(integrationToken)

    def get_events(self, account, token):
        return call_events_api(account, token)

    def get_instances(self, account, token):
        return call_instances_api(account, token)

def call_auth_api(integrationToken):
    # Get API key
    try:
        response = self.http.get(AUTH_API_URL + '?token=' + integrationToken)
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

    return token

def call_events_api(account, token):
    try:
        eventsJson = call_api_get(EVENT_API_URL.format(account), token)
    except requests.exceptions.Timeout:
        raise CheckException('Failed to get events by timeout')
    except Exception as e:
        raise CheckException('Failed to get events by {}'.format(e))
    return eventsJson['events']

def call_instances_api(account, token):
    try:
        instancesJson = call_api_get(INSTANCES_API_URL.format(account), token)
    except requests.exceptions.Timeout:
        raise CheckException('Failed to get instances by timeout')
    except Exception as e:
        raise CheckException('Failed to get instances by {}'.format(e))
    return instancesJson['instances']

def call_api_get(url, token):
    headers = {'Authorization' :'Bearer {}'.format(token)}
    response = self.http.get(url, headers=headers)

    if response.status_code != 200:
        raise ConfigurationError('Failed to get {}. status_code={}'.format(key, response.status_code))

    resultsJson = json.loads(response.text)

    return resultsJson

def get_recover_count(events, now):
    filtered_api = [event for event in events if event['requester'] == 'api']
    filtered = [event for event in filtered_api if isInLastOneHour(event, now) is True]
    return len(filtered)

def isInLastOneHour(event, now):
    oneHourAgo = now - timedelta(hours=1)
    eventHour = parse(event['startTime'])
    return oneHourAgo < eventHour

def get_monitoring_instances_number(instances):
    return len([instance for instance in instances if instance['state'] == 'monitoring'])
