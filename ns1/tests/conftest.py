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

CONFIG_2 = """{
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
    "ddi": null,
    "account":[
        {"billing": null},
        {"ttl": ["dloc.com", "dloc1.com", "dloc2.com"]}
    ]
  }
}"""

CONFIG_1 = """
{
  "api_endpoint": "https://my.nsone.net",
  "api_key": "svgRdvxF6XpWtqXGBJi7",
  "min_collection_interval": 15,
  "query_params": {
    "usage_networks": "*",
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
      }
    ],
    "ddi": [
      13,
      14,
      15
    ],
    "qps": [
      {
        "dloc.com": [
          {
            "www": "A"
          },
          {
            "email": "A"
          }
        ]
      },
      {
        "dloc1.com": [
          {
            "www": "A"
          },
          {
            "email": "A"
          }
        ]
      },
      {
        "dloc2.com": [
          {
            "www": "A"
          },
          {
            "email": "A"
          }
        ]
      }
    ],
    "usage": [
      {
        "dloc.com": [
          {
            "www": "A"
          },
          {
            "email": "A"
          }
        ]
      },
      {
        "dloc1.com": [
          {
            "www": "A"
          },
          {
            "email": "A"
          }
        ]
      },
      {
        "dloc2.com": [
          {
            "www": "A"
          },
          {
            "email": "A"
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
