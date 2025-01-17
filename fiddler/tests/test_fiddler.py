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


def test_get_metrics_success(requests_mock, instance, mock_metrics_response_data, model):
    check = FiddlerCheck('fiddler', {}, [instance])

    requests_mock.get(
        'http://example.com/v3/models/8936c2b9-d9ca-4e7b-9b6a-0a49958b7599/metrics', json=mock_metrics_response_data
    )
    metrics, outputs = check._get_metrics(model)
    assert metrics == mock_metrics_response_data['data']['metrics']
    assert outputs == ['probability_churned']


def test_get_metrics_failure(requests_mock, instance, model):
    check = FiddlerCheck('fiddler', {}, [instance])

    requests_mock.get('http://example.com/v3/models/8936c2b9-d9ca-4e7b-9b6a-0a49958b7599/metrics', status_code=500)
    metrics, outputs = check._get_metrics(model)
    assert metrics == []
    assert outputs == []


def test_get_model_success(requests_mock, mock_list_models_response_data, instance):
    check = FiddlerCheck('fiddler', {}, [instance])

    requests_mock.get(
        'http://example.com/v3/models',
        json=mock_list_models_response_data,
    )
    models = check._list_models()
    assert models == [
        {
            'name': 'model1',
            'id': '8936c2b9-d9ca-4e7b-9b6a-0a49958b7599',
            'project': {'id': 'b02e9e39-7c33-41c0-96b8-55c6e7553c24', 'name': 'project1'},
        },
        {
            'name': 'model2',
            'id': '0936c2b9-d9ca-4e7b-9b6a-0a49958b7599',
            'project': {'id': 'a02e9e39-7c33-41c0-96b8-55c6e7553c24', 'name': 'project2'},
        },
        {
            'name': 'model3',
            'id': '1936c2b9-d9ca-4e7b-9b6a-0a49958b7599',
            'project': {'id': 'c02e9e39-7c33-41c0-96b8-55c6e7553c24', 'name': 'project3'},
        },
    ]


def test_get_model_failure(requests_mock, instance):
    check = FiddlerCheck('fiddler', {}, [instance])

    requests_mock.get('http://example.com/v3/models', status_code=500)
    models = check._list_models()
    assert models == []


def test_run_queries_success(
    requests_mock,
    instance,
    mock_metrics_response_data,
    mock_queries_response_data,
    model,
    mock_list_baselines_response_data,
):
    check = FiddlerCheck('fiddler', {}, [instance])

    requests_mock.get(
        'http://example.com/v3/models/8936c2b9-d9ca-4e7b-9b6a-0a49958b7599/baselines',
        json=mock_list_baselines_response_data,
    )
    requests_mock.get(
        'http://example.com/v3/models/8936c2b9-d9ca-4e7b-9b6a-0a49958b7599/metrics', json=mock_metrics_response_data
    )
    requests_mock.post('http://example.com/v3/queries', json=mock_queries_response_data)

    # Run the _run_queries method and verify the output
    response, outputs = check._run_queries(model)
    assert response == mock_queries_response_data
    assert outputs == ['probability_churned']


def test_run_queries_failure(
    requests_mock, instance, mock_metrics_response_data, model, mock_list_baselines_response_data
):
    check = FiddlerCheck('fiddler', {}, [instance])

    requests_mock.get(
        'http://example.com/v3/models/8936c2b9-d9ca-4e7b-9b6a-0a49958b7599/baselines',
        json=mock_list_baselines_response_data,
    )
    requests_mock.get(
        'http://example.com/v3/models/8936c2b9-d9ca-4e7b-9b6a-0a49958b7599/metrics', json=mock_metrics_response_data
    )
    requests_mock.post('http://example.com/v3/queries', status_code=500)

    # Run the _run_queries method and verify the output
    response, outputs = check._run_queries(model)
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
    dd_run_check,
    aggregator,
    instance,
    requests_mock,
    mock_metrics_response_data,
    mock_query_response_all_metrics,
):
    instance['v1compat'] = True
    check = FiddlerCheck('fiddler', {}, [instance])
    requests_mock.get(
        'http://example.com/v3/models',
        json={
            'data': {
                'items': [
                    {
                        'name': 'model1',
                        'id': '8936c2b9-d9ca-4e7b-9b6a-0a49958b7599',
                        'project': {'id': 'b02e9e39-7c33-41c0-96b8-55c6e7553c24', 'name': 'project1'},
                    },
                ]
            }
        },
    )
    requests_mock.get(
        'http://example.com/v3/models/8936c2b9-d9ca-4e7b-9b6a-0a49958b7599/baselines',
        json={
            'data': {
                'items': [
                    {
                        'name': 'static_default_baseline',
                        'id': '8936c2b9-d9ca-4e7b-9b6a-0a49958b7599',
                    },
                ]
            }
        },
    )
    requests_mock.get(
        'http://example.com/v3/models/8936c2b9-d9ca-4e7b-9b6a-0a49958b7599/metrics', json=mock_metrics_response_data
    )
    requests_mock.post('http://example.com/v3/queries', json=mock_query_response_all_metrics)

    dd_run_check(check)

    aggregator.assert_service_check('fiddler.can_connect', FiddlerCheck.OK)
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())

    # assert metrics we expect, and set at_least to 0 for the metrics that may not be present depending on the models
    aggregator.assert_metric('fiddler.accuracy')
    aggregator.assert_metric('fiddler.histogram_drift')
    aggregator.assert_metric('fiddler.feature_average')
    aggregator.assert_metric('fiddler.output_average')
    aggregator.assert_metric('fiddler.traffic_count')
    aggregator.assert_metric('fiddler.binary_cross_entropy')
    aggregator.assert_metric('fiddler.data_count')
    aggregator.assert_metric('fiddler.expected_callibration_error')
    aggregator.assert_metric('fiddler.fpr', at_least=0)
    aggregator.assert_metric('fiddler.precision')
    aggregator.assert_metric('fiddler.auc')
    aggregator.assert_metric('fiddler.auroc', at_least=0)
    aggregator.assert_metric('fiddler.tpr')
    aggregator.assert_metric('fiddler.mape', at_least=0)
    aggregator.assert_metric('fiddler.wmape', at_least=0)
    aggregator.assert_metric('fiddler.mae', at_least=0)
    aggregator.assert_metric('fiddler.mse', at_least=0)
    aggregator.assert_metric('fiddler.r2', at_least=0)
    aggregator.assert_metric('fiddler.callibrated_threshold')
    aggregator.assert_metric('fiddler.g_mean')
    aggregator.assert_metric('fiddler.f1_score')
    aggregator.assert_metric('fiddler.sum')
    aggregator.assert_metric('fiddler.psi')

    # ensure all metrics are covered at least 0 or 1 times
    aggregator.assert_all_metrics_covered()


def test_metric_collection_v3(
    dd_run_check,
    aggregator,
    instance,
    requests_mock,
    mock_metrics_response_data,
    mock_query_response_all_metrics,
):
    check = FiddlerCheck('fiddler', {}, [instance])
    requests_mock.get(
        'http://example.com/v3/models',
        json={
            'data': {
                'items': [
                    {
                        'name': 'model1',
                        'id': '8936c2b9-d9ca-4e7b-9b6a-0a49958b7599',
                        'project': {'id': 'b02e9e39-7c33-41c0-96b8-55c6e7553c24', 'name': 'project1'},
                    },
                ]
            }
        },
    )
    requests_mock.get(
        'http://example.com/v3/models/8936c2b9-d9ca-4e7b-9b6a-0a49958b7599/baselines',
        json={
            'data': {
                'items': [
                    {
                        'name': 'static_default_baseline',
                        'id': '8936c2b9-d9ca-4e7b-9b6a-0a49958b7599',
                    },
                ]
            }
        },
    )
    requests_mock.get(
        'http://example.com/v3/models/8936c2b9-d9ca-4e7b-9b6a-0a49958b7599/metrics', json=mock_metrics_response_data
    )
    requests_mock.post('http://example.com/v3/queries', json=mock_query_response_all_metrics)

    dd_run_check(check)

    aggregator.assert_service_check('fiddler.can_connect', FiddlerCheck.OK)
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())

    # assert metrics we expect, and set at_least to 0 for the metrics that may not be present depending on the models
    aggregator.assert_metric('fiddler.accuracy')
    aggregator.assert_metric('fiddler.jsd')
    aggregator.assert_metric('fiddler.average')
    aggregator.assert_metric('fiddler.traffic')
    aggregator.assert_metric('fiddler.log_loss')
    aggregator.assert_metric('fiddler.data_count')
    aggregator.assert_metric('fiddler.expected_calibration_error')
    aggregator.assert_metric('fiddler.fpr', at_least=0)
    aggregator.assert_metric('fiddler.precision')
    aggregator.assert_metric('fiddler.auc')
    aggregator.assert_metric('fiddler.auroc', at_least=0)
    aggregator.assert_metric('fiddler.recall')
    aggregator.assert_metric('fiddler.mape', at_least=0)
    aggregator.assert_metric('fiddler.wmape', at_least=0)
    aggregator.assert_metric('fiddler.mae', at_least=0)
    aggregator.assert_metric('fiddler.mse', at_least=0)
    aggregator.assert_metric('fiddler.r2', at_least=0)
    aggregator.assert_metric('fiddler.calibrated_threshold')
    aggregator.assert_metric('fiddler.geometric_mean')
    aggregator.assert_metric('fiddler.f1_score')
    aggregator.assert_metric('fiddler.sum')
    aggregator.assert_metric('fiddler.psi')

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
