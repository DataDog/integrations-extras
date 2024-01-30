from typing import Any, Callable, Dict  # noqa: F401

import pytest

from datadog_checks.base import AgentCheck  # noqa: F401
from datadog_checks.base.stubs.aggregator import AggregatorStub  # noqa: F401
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.fiddler import FiddlerCheck


def test_check(dd_run_check, aggregator, instance):
    check = FiddlerCheck('fiddler', {}, [instance])
    # Prevent the integration from failing
    with pytest.raises(Exception) as e:
        dd_run_check(check)
        assert 'Authorization Required' in str(e.value)


def test_initialization(instance):
    check = FiddlerCheck('fiddler', {}, [instance])
    assert check.url == 'http://example.com'
    assert check.organization == 'test_org'


def test_call_success(requests_mock, instance):
    check = FiddlerCheck('fiddler', {}, [instance])
    requests_mock.get('http://example.com/test_endpoint', text='response')
    response = check._call('test_endpoint')
    assert response.text == 'response'


def test_call_failure(requests_mock, instance):
    check = FiddlerCheck('fiddler', {}, [instance])
    requests_mock.get('http://example.com/test_endpoint', status_code=500)
    response = check._call('test_endpoint')
    assert response.status_code == 500


def test_get_metrics_success(requests_mock, instance, mock_metrics_response_data):
    check = FiddlerCheck('fiddler', {}, [instance])

    requests_mock.get(
        'http://example.com/v2/metrics/test_org:bank_churn:churn_classifier', json=mock_metrics_response_data
    )
    metrics, outputs = check._get_metrics('bank_churn', 'churn_classifier')
    assert metrics == mock_metrics_response_data["data"]["metrics"]
    assert outputs == ["probability_churn"]


def test_get_metrics_failure(requests_mock, instance):
    check = FiddlerCheck('fiddler', {}, [instance])

    requests_mock.get('http://example.com/v2/metrics/test_org:bank_churn:churn_classifier', status_code=500)
    metrics, outputs = check._get_metrics('bank_churn', 'churn_classifier')
    assert metrics == []
    assert outputs == []


def test_get_model_success(requests_mock, mock_list_models_response_data, instance):
    check = FiddlerCheck('fiddler', {}, [instance])

    requests_mock.get(
        'http://example.com/v2/models?organization_name=test_org&project_name=bank_churn',
        json=mock_list_models_response_data,
    )
    models = check._list_models('bank_churn')
    assert models == ["model1", "model2", "model3"]


def test_get_model_failure(requests_mock, instance):
    check = FiddlerCheck('fiddler', {}, [instance])

    requests_mock.get(
        'http://example.com/v2/models?organization_name=test_org&project_name=bank_churn', status_code=500
    )
    models = check._list_models('bank_churn')
    assert models == []


def test_get_project_success(requests_mock, instance, mock_list_projects_response_data):
    check = FiddlerCheck('fiddler', {}, [instance])

    requests_mock.get('http://example.com/v2/list-projects/test_org', json=mock_list_projects_response_data)
    projects = check._list_projects()
    assert projects == ["project1", "project2", "project3"]


def test_get_project_failure(requests_mock, instance):
    check = FiddlerCheck('fiddler', {}, [instance])

    requests_mock.get('http://example.com/v2/list-projects/test_org', status_code=500)
    projects = check._list_projects()
    assert projects == []


def test_run_queries_success(requests_mock, instance, mock_metrics_response_data):
    check = FiddlerCheck('fiddler', {}, [instance])

    requests_mock.get(
        'http://example.com/v2/metrics/test_org:bank_churn:churn_classifier', json=mock_metrics_response_data
    )
    requests_mock.post('http://example.com/v2/queries', json=mock_metrics_response_data)

    # Run the _run_queries method and verify the output
    response, outputs = check._run_queries('bank_churn', 'churn_classifier')
    assert response == mock_metrics_response_data
    assert outputs == ['probability_churn']


def test_run_queries_failure(requests_mock, instance, mock_metrics_response_data):
    check = FiddlerCheck('fiddler', {}, [instance])

    requests_mock.get(
        'http://example.com/v2/metrics/test_org:bank_churn:churn_classifier', json=mock_metrics_response_data
    )
    requests_mock.post('http://example.com/v2/queries', status_code=500)

    # Run the _run_queries method and verify the output
    response, outputs = check._run_queries('bank_churn', 'churn_classifier')
    assert response == {}
    assert outputs == []


def test_create_tags(instance):
    check = FiddlerCheck('fiddler', {}, [instance])
    tags = check._create_tags('bank_churn', 'churn_classifier')
    assert tags == ['project:bank_churn', 'model:churn_classifier']

    tags = check._create_tags('bank_churn', None)
    assert tags == ['project:bank_churn']

    tags = check._create_tags(None, 'churn_classifier')
    assert tags == ['model:churn_classifier']

    tags = check._create_tags(None, None)
    assert tags == []

    tags = check._create_tags('bank_churn', 'churn_classifier', 'test_tag')
    assert tags == ['project:bank_churn', 'model:churn_classifier', 'feature:test_tag']


def test_metric_collection(
    dd_run_check, aggregator, instance, requests_mock, mock_metrics_response_data, mock_query_expanded_response_data
):
    check = FiddlerCheck('fiddler', {}, [instance])

    requests_mock.get(
        'http://example.com/v2/list-projects/test_org', json={"data": {"projects": [{"name": "bank_churn"}]}}
    )
    requests_mock.get(
        'http://example.com/v2/models?organization_name=test_org&project_name=bank_churn',
        json={"data": {"items": [{"name": "churn_classifier"}]}},
    )
    requests_mock.get(
        'http://example.com/v2/metrics/test_org:bank_churn:churn_classifier', json=mock_metrics_response_data
    )
    requests_mock.post('http://example.com/v2/queries', json=mock_query_expanded_response_data)

    dd_run_check(check)

    aggregator.assert_service_check('fiddler.can_connect', FiddlerCheck.OK)
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())

    # assert metrics we expect, and set at_least to 0 for the metrics that may not be present depending on the models
    aggregator.assert_metric('fiddler.accuracy', at_least=0)
    aggregator.assert_metric('fiddler.histogram_drift')
    aggregator.assert_metric('fiddler.feature_average')
    aggregator.assert_metric('fiddler.output_average')
    aggregator.assert_metric('fiddler.traffic_count')
    aggregator.assert_metric('fiddler.binary_cross_entropy', at_least=0)
    aggregator.assert_metric('fiddler.data_count', at_least=0)
    aggregator.assert_metric('fiddler.expected_calibration_error', at_least=0)
    aggregator.assert_metric('fiddler.fpr', at_least=0)
    aggregator.assert_metric('fiddler.precision', at_least=0)
    aggregator.assert_metric('fiddler.auc', at_least=0)
    aggregator.assert_metric('fiddler.auroc', at_least=0)
    aggregator.assert_metric('fiddler.recall', at_least=0)
    aggregator.assert_metric('fiddler.mape', at_least=0)
    aggregator.assert_metric('fiddler.wmape', at_least=0)
    aggregator.assert_metric('fiddler.mae', at_least=0)
    aggregator.assert_metric('fiddler.mse', at_least=0)
    aggregator.assert_metric('fiddler.r2', at_least=0)
    aggregator.assert_metric('fiddler.calibrated_threshold', at_least=0)
    aggregator.assert_metric('fiddler.g_mean', at_least=0)
    aggregator.assert_metric('fiddler.f1_score', at_least=0)
    aggregator.assert_metric('fiddler.sum', at_least=0)

    # ensure all metrics are covered at least 0 or 1 times
    aggregator.assert_all_metrics_covered()


@pytest.mark.e2e
@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_service_check(aggregator, instance):
    c = FiddlerCheck('fiddler', {}, [instance])

    # the check should send OK
    c.check(instance)
    aggregator.assert_service_check('fiddler.can_connect', FiddlerCheck.OK)
