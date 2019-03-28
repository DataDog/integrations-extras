from datadog_checks.base import AgentCheck
import boto3
import json


class AwsPricingCheck(AgentCheck):
    def check(self, instance):
        pricing_client = boto3.client('pricing', region_name='us-east-1')
        service_code = 'AmazonEC2'
        rate_code = 'YQHNG5NBWUE3D67S.4NA7Y494T4.6YS6EN2CT7'

        price_dimensions = get_aws_prices(pricing_client, service_code, rate_code)

        name = 'aws.pricing.{}'.format(service_code.lower())
        price = get_price_from_price_dimensions(price_dimensions)
        tags = get_tags_from_price_dimensions(price_dimensions)

        print(name)
        print(price)
        print(tags)

        service_code = 'AmazonCloudFront'
        rate_code = '84Z32PF576RHPTMX.JRTCKXETXF.SW9U2ZKBYX'

        price_dimensions = get_aws_prices(pricing_client, service_code, rate_code)

        name = 'aws.pricing.{}'.format(service_code.lower())
        price = get_price_from_price_dimensions(price_dimensions)
        tags = get_tags_from_price_dimensions(price_dimensions)

        print(name)
        print(price)
        print(tags)

        raise Exception()


def get_aws_prices(pricing_client, service_code, rate_code):
    response = pricing_client.get_products(
        ServiceCode=service_code,
        Filters=[{'Type': 'TERM_MATCH', 'Field': 'RateCode', 'Value': rate_code}],
        MaxResults=1
    )

    response_obj = json.loads(response['PriceList'][0])
    terms = response_obj["terms"].itervalues()
    price_dimensions = find_price_dimensions_by_rate_code(rate_code, terms)

    return price_dimensions


def find_price_dimensions_by_rate_code(rate_code, terms):
    rate_code_parts = rate_code.split('.')
    term_code = '.'.join(rate_code_parts[:2])

    term = filter(lambda term: term_code in term, terms)[0]
    price_dimensions = term[term_code]["priceDimensions"][rate_code]

    return price_dimensions


def get_tags_from_price_dimensions(price_dimensions):
    return {
        'rate_code': price_dimensions['rateCode'],
        'unit': price_dimensions['unit']
    }


def get_price_from_price_dimensions(price_dimensions):
    return float(price_dimensions['pricePerUnit']['USD'])
