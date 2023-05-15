import boto3
import pytest

from tests.pricing_client_stubber import PricingClientStubber


@pytest.fixture()
def pricing_client():
    pricing_client = boto3.client('pricing', region_name='us-east-1')

    return pricing_client


@pytest.fixture()
def pricing_client_stubber(pricing_client):
    pricing_client_stubber = PricingClientStubber(pricing_client)

    return pricing_client_stubber
