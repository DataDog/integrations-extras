import boto3
import json

from datadog_checks.base import AgentCheck
from datadog_checks.errors import CheckException


class AwsPricingCheck(AgentCheck):
    def check(self, instance):
        try:
            pricing_client = boto3.client('pricing', region_name='us-east-1')
            service_codes = get_aws_service_codes(pricing_client)

            rate_codes_dict = get_rate_codes_dict_from_instance(service_codes, instance)

            # Python dictionaries evaluate to false when empty
            if not rate_codes_dict:
                raise CheckException('No rate codes were defined, please fix aws_pricing.yaml')

            any_rate_codes_not_found = False

            for service_code, rate_codes in rate_codes_dict.iteritems():
                for rate_code in rate_codes:
                    price_dimensions = get_aws_prices(pricing_client, service_code, rate_code)

                    if price_dimensions is None:
                        any_rate_codes_not_found = True
                        continue

                    name = 'aws.pricing.{}'.format(service_code.lower())
                    price = get_price_from_price_dimensions(price_dimensions)
                    tags = get_tags_from_price_dimensions(price_dimensions)

                    self.gauge(name, price, tags)

            if any_rate_codes_not_found:
                self.service_check('aws_pricing.all_good', self.WARNING)
        except Exception as e:
            self.service_check('aws_pricing.all_good', self.CRITICAL, e)

        self.service_check('aws_pricing.all_good', self.OK)


def get_rate_codes_dict_from_instance(service_codes, instance):
    rate_codes_dict = {}
    for service_code in service_codes:
        rate_codes_string = instance.get(service_code)
        if rate_codes_string is not None:
            rate_codes = map(str.strip, rate_codes_string.split(','))
            rate_codes_dict[service_code] = rate_codes

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
        terms = response_obj['terms'].itervalues()
        price_dimensions = find_price_dimensions_by_rate_code(rate_code, terms)

    return price_dimensions


def find_price_dimensions_by_rate_code(rate_code, terms):
    rate_code_parts = rate_code.split('.')
    term_code = '.'.join(rate_code_parts[:2])

    term = filter(lambda term: term_code in term, terms)[0]
    price_dimensions = term[term_code]['priceDimensions'][rate_code]

    return price_dimensions


def get_tags_from_price_dimensions(price_dimensions):
    return {
        'rate_code': price_dimensions['rateCode'],
        'unit': price_dimensions['unit']
    }


def get_price_from_price_dimensions(price_dimensions):
    return float(price_dimensions['pricePerUnit']['USD'])
