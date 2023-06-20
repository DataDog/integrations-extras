import json

from requests import RequestException

from datadog_checks.base import AgentCheck
from datadog_checks.base.errors import CheckException


class NeutronaCheck(AgentCheck):
    def check(self, instance):

        neutrona_express_route_api_url = 'https://expressroutetelemetry.neutrona.com'
        azure_authentication_url = 'https://login.microsoftonline.com'
        azure_management_url = 'https://management.azure.com/'

        # TESTING
        try:
            neutrona_express_route_api_url = instance['azure']['testing']['neutrona_express_route_api_url']
            azure_authentication_url = instance['azure']['testing']['azure_authentication_url']
            azure_management_url = instance['azure']['testing']['azure_management_url']
        except KeyError:
            pass

        # AZURE API OAUTH2 TOKEN
        try:
            directory_id = instance['azure']['directory_id']
            application_id = instance['azure']['application_id']
            application_key = instance['azure']['application_key']
            subscription_id = instance['azure']['subscription_id']
        except KeyError:
            self.log.error("Configuration error, please fix check's conf.yaml")
            raise CheckException("Configuration error, please fix check's conf.yaml")

        try:
            response = self.http.post(
                '/'.join([azure_authentication_url.strip('/'), directory_id, 'oauth2/token?api-version=1.0']),
                data={
                    'grant_type': 'client_credentials',
                    'resource': 'https://management.core.windows.net/',
                    'client_id': application_id,
                    'client_secret': application_key,
                },
            )
            response.raise_for_status()
        except RequestException:
            self.log.error(
                ' '.join(['Connection error to', azure_authentication_url, 'Unable to obtain Azure access token.'])
            )
            raise CheckException(
                ' '.join(['Connection error to', azure_authentication_url, 'Unable to obtain Azure access token.'])
            )

        azure_access_token = ''

        if response.status_code != 200:

            self.log.error(' '.join(['Error authenticating with Azure: ', str(response.status_code)]))
            raise CheckException(
                ' '.join(['Connection error to', azure_authentication_url, 'Unable to obtain Azure access token.'])
            )

        else:

            try:
                azure_access_token = json.loads(response.content)['access_token']
            except KeyError:
                self.log.error('Unable to obtain Azure access token. Access token not present in response.')
                raise CheckException('Unable to obtain Azure access token. Access token not present in response.')

        # EXPRESS ROUTE CROSS CONNECTIONS
        try:
            response = self.http.get(
                ''.join(
                    [
                        azure_management_url.strip('/'),
                        '/subscriptions/',
                        subscription_id,
                        '/providers/Microsoft.Network',
                        '/expressRouteCircuits',
                        '?api-version=',
                        '2018-08-01',
                    ]
                ),
                extra_headers={'Authorization': ' '.join(['Bearer', azure_access_token])},
            )
            response.raise_for_status()
        except RequestException:
            self.log.error(' '.join(['Connection error to', azure_management_url]))
            raise CheckException(' '.join(['Connection error to', azure_management_url]))

        if response.status_code != 200:

            self.log.error(''.join(['Error querying Azure API: Code ', response.status_code]))
            raise CheckException(' '.join(['Connection error to', azure_management_url]))

        else:

            inventory = json.loads(response.content)

            try:

                for cc in inventory['value']:

                    service_key = cc['properties']['serviceKey']

                    service_provider_name = cc['properties']['serviceProviderProperties']['serviceProviderName']

                    if service_provider_name == 'Neutrona Networks':
                        self.log.info(' '.join(['Querying for:', service_key, service_provider_name]))

                        # NEUTRONA TELEMETRY DATA
                        try:
                            response = self.http.get(
                                ''.join([neutrona_express_route_api_url.strip('/'), '/client/?=', service_key]),
                            )
                        except RequestException:
                            self.log.error(' '.join(['Connection error to', neutrona_express_route_api_url]))
                            raise CheckException(' '.join(['Connection error to', neutrona_express_route_api_url]))

                        if response.status_code == 200:

                            connections = json.loads(response.content)

                            try:
                                for conn in connections:
                                    for metric, value in conn.items():
                                        if metric != 'tags':
                                            self.gauge(
                                                '.'.join(['neutrona', 'azure', 'expressroute', metric]),
                                                value,
                                                conn['tags'],
                                                service_key,
                                            )
                            except KeyError:
                                self.log.error(''.join(['Error querying Neutrona Express Route API: Invalid Response']))
                                raise CheckException('Error querying Neutrona Express Route API: Invalid Response')

                        else:
                            self.log.error(
                                ' -- '.join(
                                    [
                                        service_key,
                                        service_provider_name,
                                        'Error querying Neutrona API: Code ',
                                        str(response.status_code),
                                    ]
                                )
                            )
                            raise CheckException(' '.join(['Connection error to', neutrona_express_route_api_url]))

            except KeyError:
                self.log.error(''.join(['Error querying Azure API: Invalid Response']))
                raise CheckException('Error querying Azure API: Invalid Response')
