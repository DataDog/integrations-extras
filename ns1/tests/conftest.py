import json

import pytest

CONFIG = {
    'api_endpoint': 'https://my.nsone.net',
    # The api authentication key.
    'api_key': 'testkey',
    'metrics': {'qps': [{"test.com": None}], 'usage': [{"test.com": None}], 'pulsar': None, 'ddi': None},
}

CONFIG_NOMETRICS = {
    'api_endpoint': 'https://test.com',
    # The api authentication key.
    'api_key': 'testkey',
    'metrics': None,
}

CONFIG_NOKEY = {
    'api_endpoint': 'https://test.com',
    # The api authentication key.
    'api_key': None,
    'metrics': None,
}

CONFIG_2 = """{
    "api_endpoint": "https://my.nsone.net",
    "api_key": "testkey",
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
    "ddi": null,
    "account":[
        {"billing": null},
        {"ttl": ["dloc.com", "dloc1.com", "dloc2.com"]}
    ]
  }
}"""
CONFIG_DDI = """
{
  "api_endpoint": "https://localhost",
  "api_key": "testkey",
  "min_collection_interval": 15,
  "metrics": {
    "ddi": [
      2
    ]
  }
}
"""
CONFIG_1 = """
{
  "api_endpoint": "https://my.nsone.net",
  "api_key": "testkey",
  "min_collection_interval": 15,
  "networks":[
    0,
    5,
    80
  ],
  "query_params": {
    "pulsar_period": "1m",
    "pulsar_geo": "*",
    "pulsar_asn": "*",
    "pulsar_agg": "avg"
  },
  "metrics": {
    "pulsar": null,
    "pulsar_by_app": [
      {
        "1xy4sn3": "1xtvhvx"
      }
    ],
    "pulsar_by_record": [
      {
        "www.dloc1.com": "A"
      },
      {
        "www.dloc2.com": "A"
      }
    ],
    "qps": [
      {
        "dloc.com": [
          {
            "www.dloc.com": "A"
          },
          {
            "email.dloc.com": "A"
          }
        ]
      },
      {
        "dloc1.com": null
      },
      {
        "dloc2.com": [
          {
            "www.dloc2.com": "A"
          },
          {
            "email.dloc2.com": "A"
          }
        ]
      }
    ],
    "usage": [
      {
        "dloc.com": [
          {
            "www.dloc.com": "A"
          },
          {
            "email.dloc.com": "A"
          }
        ]
      },
      {
        "dloc1.com": null
      },
      {
        "dloc2.com": [
          {
            "www.dloc2.com": "A"
          },
          {
            "email.dloc2.com": "A"
          }
        ]
      }
    ],
    "account": [
      {
        "billing": null
      },
      {
        "ttl": [
          "dloc.com",
          "dloc1.com",
          "dloc2.com"
        ]
      }
    ]
  }
}
"""


@pytest.fixture
def instance():
    return CONFIG


@pytest.fixture
def instance_nokey():
    return CONFIG_NOKEY


@pytest.fixture
def instance_nometrics():
    return CONFIG_NOMETRICS


@pytest.fixture
def instance_empty():
    return {}


@pytest.fixture
def instance_1():
    return json.loads(CONFIG_1)


@pytest.fixture
def instance_ddi():
    return json.loads(CONFIG_DDI)
