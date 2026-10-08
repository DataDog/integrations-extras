# (C) Datadog, Inc. 2026-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from unittest import mock

import pytest

from datadog_checks.log10x import Log10xCheck

from .common import MOCKED_INSTANCE, get_fixture_path


@pytest.fixture(scope='session')
def dd_environment():
    # The unit tests run against a captured scrape of a 10x Engine; there is no
    # container environment to bring up. e2e tests are skipped for this integration.
    yield MOCKED_INSTANCE


@pytest.fixture
def instance():
    return dict(MOCKED_INSTANCE)


@pytest.fixture
def check(instance):
    return Log10xCheck('log10x', {}, [instance])


@pytest.fixture()
def mock_prometheus_metrics():
    fixture_file = get_fixture_path('metrics.txt')
    with open(fixture_file, 'r') as f:
        content = f.read()
    with mock.patch(
        'requests.Session.get',
        return_value=mock.MagicMock(
            status_code=200,
            iter_lines=lambda **kwargs: content.split('\n'),
            headers={'Content-Type': 'text/plain'},
            close=lambda: None,
        ),
    ):
        yield
