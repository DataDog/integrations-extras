import os

import pytest

FIDDLER_API_KEY = os.environ.get('FIDDLER_API_KEY')


@pytest.fixture(scope='session')
def dd_environment(instance, e2e_instance):
    if FIDDLER_API_KEY:
        yield e2e_instance
    else:
        yield instance


@pytest.fixture(scope='session')
def instance():
    return {
        "url": "https://demo.fiddler.ai",
        "fiddler_api_key": "apikey",
        "organization": "demo",
    }


@pytest.fixture(scope='session')
def e2e_instance():
    return {
        "url": "https://demo.fiddler.ai",
        "fiddler_api_key": FIDDLER_API_KEY,
        "organization": "demo",
    }
