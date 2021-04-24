import json

import pytest

CONFIG = {
    'api_endpoint': 'https://my.nsone.net',
    # The api authentication key.
    'api_key': 'svgRdvxF6XpWtqXGBJi7',
    'metrics': {'qps': [{"test.com": None}], 'usage': [{"test.com": None}], 'pulsar': None, 'ddi': None},
}

CONFIG_NOMETRICS = {
    'api_endpoint': 'https://test.com',
    # The api authentication key.
    'api_key': 'testkey',
    'metrics': None,
}

CONFIG_1 = """{
    "api_endpoint": "https://my.nsone.net",
    "api_key": "svgRdvxF6XpWtqXGBJi7",
    "metrics": {
    "qps": [
      {
        "test.com": [
          {
            "www": "A"
          },
          {
            "mail": "A"
          }
        ]
      }
    ],
    "usage": [
      {
        "test.com": null
      }
    ],
    "pulsar": null,
    "ddi": null
  }
}"""


@pytest.fixture(scope='session')
def dd_environment():
    yield


@pytest.fixture
def instance():
    return CONFIG


@pytest.fixture
def instance_nometrics():
    return CONFIG_NOMETRICS


@pytest.fixture
def instance_empty():
    return {}


@pytest.fixture
def instance_1():
    return json.loads(CONFIG_1)
