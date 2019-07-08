import boto3
from collections import defaultdict
import json
import six

from botocore.exceptions import ClientError
from datadog_checks.base import AgentCheck
from datadog_checks.errors import CheckException


class AwsPricingCheck(AgentCheck):
    def check(self, instance):
        try:
            region_name = instance.get('region_name')
            if not region_name:
                message = 'No region name has been specified, please fix conf.yaml'
                self.service_check('aws_pricing.status', self.CRITICAL, message=message)
                raise CheckException(message)

            pricing_client = boto3.client('pricing', region_name=region_name)

            service_codes = get_aws_service_codes(pricing_client)
            rate_codes_dict = get_rate_codes_dict_from_instance(service_codes, instance)

            # Python dictionaries evaluate to false when empty
            if not rate_codes_dict:
                message = 'No rate codes for existing AWS services were defined, please fix conf.yaml'
                self.service_check('aws_pricing.status', self.CRITICAL, message=message)
                raise CheckException(message)

            missing_rate_codes = defaultdict(list)

            for service_code, rate_codes in six.iteritems(rate_codes_dict):
                for rate_code in rate_codes:
                    price_dimensions = get_aws_prices(pricing_client, service_code, rate_code)

                    if price_dimensions is None:
                        missing_rate_codes[service_code].append(rate_code)
                        continue

                    name = 'aws.pricing.{}'.format(service_code.lower())
                    price = get_price_from_price_dimensions(price_dimensions)
                    tags = get_tags_from_price_dimensions(price_dimensions)

                    self.gauge(name, price, tags)

            # Python dictionaries evaluate to true when not empty
            if not missing_rate_codes:
                self.service_check('aws_pricing.status', self.OK)
            else:
                message = 'Pricing data not found for these service rate codes: {}'.format(dict(missing_rate_codes))
                self.service_check('aws_pricing.status', self.WARNING, message=message)

        except ClientError as client_error:
            self.service_check('aws_pricing.status', self.CRITICAL, message=str(client_error))
            raise CheckException('Pricing Service client error: {}'.format(str(client_error)))


def get_rate_codes_dict_from_instance(service_codes, instance):
    rate_codes_dict = {}
    for service_code in service_codes:
        rate_codes_dict[service_code] = instance.get(service_code)

    return rate_codes_dict


def get_aws_service_codes(pricing_client):
    response = pricing_client.describe_services(
        FormatVersion='aws_v1'
    )

    service_codes = map(lambda service: service['ServiceCode'], response['Services'])

    return service_codes


def get_aws_prices(pricing_client, service_code, rate_code):
    response = pricing_client.get_products(
        FormatVersion='aws_v1',
        ServiceCode=service_code,
        Filters=[{'Type': 'TERM_MATCH', 'Field': 'RateCode', 'Value': rate_code}],
        MaxResults=1
    )

    price_dimensions = None

    if len(response['PriceList']) > 0:
        response_obj = json.loads(response['PriceList'][0])
        terms = response_obj['terms'].values()
        price_dimensions = find_price_dimensions_by_rate_code(rate_code, terms)

    return price_dimensions


def find_price_dimensions_by_rate_code(rate_code, terms):
    rate_code_parts = rate_code.split('.')
    term_code = '.'.join(rate_code_parts[:2])

    term = list(filter(lambda term: term_code in term, terms))[0]
    price_dimensions = term[term_code]['priceDimensions'][rate_code]

    return price_dimensions


def get_tags_from_price_dimensions(price_dimensions):
    return {
        'rate_code': price_dimensions['rateCode'],
        'unit': price_dimensions['unit']
    }


def get_price_from_price_dimensions(price_dimensions):
    return float(price_dimensions['pricePerUnit']['USD'])
