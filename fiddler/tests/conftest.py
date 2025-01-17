import os

import pytest
from datadog_checks.dev import docker_run, get_docker_hostname, get_here

URL = 'http://{}:9000'.format(get_docker_hostname())
INSTANCE = {'url': 'http://example.com', 'fiddler_api_key': 'testtoken', 'organization': 'test_org'}


@pytest.fixture(scope='session')
def dd_environment():
    compose_file = os.path.join(get_here(), 'docker-compose.yml')

    # This does 3 things:
    #
    # 1. Spins up the services defined in the compose file
    # 2. Waits for the url to be available before running the tests
    # 3. Tears down the services when the tests are finished
    with docker_run(compose_file, endpoints=[URL], build=True):
        yield instance


@pytest.fixture
def instance():
    return INSTANCE.copy()


@pytest.fixture
def model():
    return {
        'id': '8936c2b9-d9ca-4e7b-9b6a-0a49958b7599',
        'name': 'bank_churn',
        'project': {'id': 'b02e9e39-7c33-41c0-96b8-55c6e7553c24', 'name': 'bank_churn_project'},
    }


@pytest.fixture
def mock_metrics_response_data():
    return {
        'data': {
            'model': {'id': '8936c2b9-d9ca-4e7b-9b6a-0a49958b7599', 'name': 'bank_churn', 'version': 'v1'},
            'project': {'id': 'b02e9e39-7c33-41c0-96b8-55c6e7553c24', 'name': 'bank_churn_project'},
            'organization': {'id': '6a1b8197-a285-46ec-a61a-c403306bcfb6', 'name': 'mainbuild'},
            'metric_types': [
                {'key': 'drift', 'name': 'Data Drift'},
                {'key': 'data_integrity', 'name': 'Data Integrity'},
                {'key': 'performance', 'name': 'Performance'},
                {'key': 'service_metrics', 'name': 'Traffic'},
                {'key': 'statistic', 'name': 'Statistic'},
                {'key': 'custom', 'name': 'Custom Metric'},
            ],
            'metrics': [
                {
                    'id': 'auc',
                    'name': 'AUC',
                    'type': 'performance',
                    'columns': [],
                    'requires_baseline': False,
                    'requires_categories': False,
                    'is_percentage_comparison': False,
                    'requires_threshold': False,
                    'requires_top_k': False,
                },
                {
                    'id': 'auroc',
                    'name': 'AUROC',
                    'type': 'performance',
                    'columns': [],
                    'requires_baseline': False,
                    'requires_categories': False,
                    'is_percentage_comparison': False,
                    'requires_threshold': False,
                    'requires_top_k': False,
                },
                {
                    'id': 'accuracy',
                    'name': 'Accuracy',
                    'type': 'performance',
                    'columns': [],
                    'requires_baseline': False,
                    'requires_categories': False,
                    'is_percentage_comparison': False,
                    'requires_threshold': False,
                    'requires_top_k': False,
                },
                {
                    'id': 'average',
                    'name': 'Average',
                    'type': 'statistic',
                    'columns': [
                        'creditscore',
                        'age',
                        'tenure',
                        'balance',
                        'numofproducts',
                        'estimatedsalary',
                        'probability_churned',
                    ],
                    'requires_baseline': False,
                    'requires_categories': False,
                    'is_percentage_comparison': False,
                    'requires_threshold': False,
                    'requires_top_k': False,
                },
                {
                    'id': 'calibrated_threshold',
                    'name': 'Calibrated Threshold',
                    'type': 'performance',
                    'columns': [],
                    'requires_baseline': False,
                    'requires_categories': False,
                    'is_percentage_comparison': False,
                    'requires_threshold': False,
                    'requires_top_k': False,
                },
                {
                    'id': 'expected_calibration_error',
                    'name': 'Expected Calibration Error',
                    'type': 'performance',
                    'columns': [],
                    'requires_baseline': False,
                    'requires_categories': False,
                    'is_percentage_comparison': False,
                    'requires_threshold': False,
                    'requires_top_k': False,
                },
                {
                    'id': 'f1_score',
                    'name': 'F1',
                    'type': 'performance',
                    'columns': [],
                    'requires_baseline': False,
                    'requires_categories': False,
                    'is_percentage_comparison': False,
                    'requires_threshold': True,
                    'requires_top_k': False,
                },
                {
                    'id': 'fpr',
                    'name': 'False Positive Rate',
                    'type': 'performance',
                    'columns': [],
                    'requires_baseline': False,
                    'requires_categories': False,
                    'is_percentage_comparison': False,
                    'requires_threshold': True,
                    'requires_top_k': False,
                },
                {
                    'id': 'frequency',
                    'name': 'Frequency',
                    'type': 'statistic',
                    'columns': ['geography', 'gender', 'hascrcard', 'isactivemember', 'churned'],
                    'requires_baseline': False,
                    'requires_categories': True,
                    'is_percentage_comparison': False,
                    'requires_threshold': False,
                    'requires_top_k': False,
                },
                {
                    'id': 'geometric_mean',
                    'name': 'Geometric Mean',
                    'type': 'performance',
                    'columns': [],
                    'requires_baseline': False,
                    'requires_categories': False,
                    'is_percentage_comparison': False,
                    'requires_threshold': True,
                    'requires_top_k': False,
                },
                {
                    'id': 'jsd',
                    'name': 'Jensen-Shannon Distance',
                    'type': 'drift',
                    'columns': [
                        'creditscore',
                        'geography',
                        'gender',
                        'age',
                        'tenure',
                        'balance',
                        'numofproducts',
                        'hascrcard',
                        'isactivemember',
                        'estimatedsalary',
                        'churned',
                        'probability_churned',
                    ],
                    'requires_baseline': True,
                    'requires_categories': False,
                    'is_percentage_comparison': False,
                    'requires_threshold': False,
                    'requires_top_k': False,
                },
                {
                    'id': 'log_loss',
                    'name': 'Log Loss',
                    'type': 'performance',
                    'columns': [],
                    'requires_baseline': False,
                    'requires_categories': False,
                    'is_percentage_comparison': False,
                    'requires_threshold': False,
                    'requires_top_k': False,
                },
                {
                    'id': 'psi',
                    'name': 'Population Stability Index',
                    'type': 'drift',
                    'columns': [
                        'creditscore',
                        'geography',
                        'gender',
                        'age',
                        'tenure',
                        'balance',
                        'numofproducts',
                        'hascrcard',
                        'isactivemember',
                        'estimatedsalary',
                        'churned',
                        'probability_churned',
                    ],
                    'requires_baseline': True,
                    'requires_categories': False,
                    'is_percentage_comparison': False,
                    'requires_threshold': False,
                    'requires_top_k': False,
                },
                {
                    'id': 'precision',
                    'name': 'Precision',
                    'type': 'performance',
                    'columns': [],
                    'requires_baseline': False,
                    'requires_categories': False,
                    'is_percentage_comparison': False,
                    'requires_threshold': True,
                    'requires_top_k': False,
                },
                {
                    'id': 'recall',
                    'name': 'Recall / TPR',
                    'type': 'performance',
                    'columns': [],
                    'requires_baseline': False,
                    'requires_categories': False,
                    'is_percentage_comparison': False,
                    'requires_threshold': True,
                    'requires_top_k': False,
                },
                {
                    'id': 'sum',
                    'name': 'Sum',
                    'type': 'statistic',
                    'columns': [
                        'creditscore',
                        'age',
                        'tenure',
                        'balance',
                        'numofproducts',
                        'estimatedsalary',
                        'probability_churned',
                    ],
                    'requires_baseline': False,
                    'requires_categories': False,
                    'is_percentage_comparison': False,
                    'requires_threshold': False,
                    'requires_top_k': False,
                },
                {
                    'id': 'data_count',
                    'name': 'Total Count',
                    'type': 'performance',
                    'columns': [],
                    'requires_baseline': False,
                    'requires_categories': False,
                    'is_percentage_comparison': False,
                    'requires_threshold': False,
                    'requires_top_k': False,
                },
                {
                    'id': 'traffic',
                    'name': 'Traffic',
                    'type': 'service_metrics',
                    'columns': [],
                    'requires_baseline': False,
                    'requires_categories': False,
                    'is_percentage_comparison': False,
                    'requires_threshold': False,
                    'requires_top_k': False,
                },
            ],
            'columns': [
                {'id': '__ANY__', 'name': 'All columns'},
                {'id': 'creditscore', 'name': 'CreditScore', 'group': 'Inputs', 'data_type': 'int'},
                {'id': 'geography', 'name': 'Geography', 'group': 'Inputs', 'data_type': 'category'},
                {'id': 'gender', 'name': 'Gender', 'group': 'Inputs', 'data_type': 'category'},
                {'id': 'age', 'name': 'Age', 'group': 'Inputs', 'data_type': 'int'},
                {'id': 'tenure', 'name': 'Tenure', 'group': 'Inputs', 'data_type': 'int'},
                {'id': 'balance', 'name': 'Balance', 'group': 'Inputs', 'data_type': 'float'},
                {'id': 'numofproducts', 'name': 'NumOfProducts', 'group': 'Inputs', 'data_type': 'int'},
                {'id': 'hascrcard', 'name': 'HasCrCard', 'group': 'Inputs', 'data_type': 'category'},
                {'id': 'isactivemember', 'name': 'IsActiveMember', 'group': 'Inputs', 'data_type': 'category'},
                {'id': 'estimatedsalary', 'name': 'EstimatedSalary', 'group': 'Inputs', 'data_type': 'float'},
                {'id': 'probability_churned', 'name': 'probability_churned', 'group': 'Outputs', 'data_type': 'float'},
                {'id': 'churned', 'name': 'Churned', 'group': 'Targets', 'data_type': 'category'},
            ],
        },
        'api_version': '3.0',
        'kind': 'NORMAL',
    }


@pytest.fixture
def mock_list_projects_response_data():
    return {'data': {'projects': [{'name': 'project1'}, {'name': 'project2'}, {'name': 'project3'}]}}


@pytest.fixture
def mock_list_models_response_data():
    return {
        'data': {
            'items': [
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
        }
    }


@pytest.fixture
def mock_list_baselines_response_data():
    return {
        'data': {
            'items': [
                {
                    'name': 'static_default_baseline',
                    'id': '8936c2b9-d9ca-4e7b-9b6a-0a49958b7599',
                },
                {
                    'name': 'baseline2',
                    'id': '0936c2b9-d9ca-4e7b-9b6a-0a49958b7599',
                },
                {
                    'name': 'baseline3',
                    'id': '1936c2b9-d9ca-4e7b-9b6a-0a49958b7599',
                },
            ]
        }
    }


@pytest.fixture
def mock_metrics():
    return ([{'key': 'traffic', 'type': 'service_metrics'}], ['output1', 'output2'])


@pytest.fixture
def mock_queries_response_data():
    return {
        'data': {
            'organization_name': 'demo',
            'project_name': 'bank_churn',
            'time_comparison': None,
            'filters': {'bin_size': 'Day', 'time_zone': 'UTC', 'time_label': '7d'},
            'query_type': 'MONITORING',
            'results': [
                {
                    'fddc4480-e262-41b8-8cc2-13249683c378': {
                        'col_names': ['timestamp', 'traffic'],
                        'data': [
                            # Sample data points, include as many as needed for the test
                            ['2023-11-21T00:00:00+00:00', 294],
                            ['2023-11-22T00:00:00+00:00', 290],
                            ['2023-11-23T00:00:00+00:00', 20],
                            ['2023-11-24T00:00:00+00:00', 200],
                            ['2023-11-25T00:00:00+00:00', 190],
                            ['2023-11-26T00:00:00+00:00', 590],
                            ['2023-11-27T00:00:00+00:00', None],
                        ],
                        'query_key': 'fddc4480-e262-41b8-8cc2-13249683c378',
                        'model_name': 'churn_classifier',
                        'viz_type': 'line',
                        'metric': 'traffic',
                        'metric_type': 'service_metrics',
                        'columns': [],
                    }
                }
            ],
        },
        'api_version': '2.0',
        'kind': 'NORMAL',
    }


@pytest.fixture
def mock_query_expanded_response_data():
    return {
        'data': {
            'organization_name': 'demo',
            'project_name': 'bank_churn',
            'time_comparison': None,
            'filters': {'bin_size': 'Day', 'time_zone': 'UTC', 'time_label': '30d'},
            'query_type': 'MONITORING',
            'results': [
                {
                    'query_key_traffic': {
                        'col_names': ['timestamp', 'traffic'],
                        'data': [['2023-11-21T00:00:00+00:00', 294], ['2023-11-22T00:00:00+00:00', 290]],
                        'model_name': 'churn_classifier',
                        'viz_type': 'line',
                        'metric': 'traffic',
                        'metric_type': 'service_metrics',
                    },
                    'query_key_jsd': {
                        'col_names': ['timestamp', 'probability_churn'],
                        'data': [['2023-11-21T00:00:00+00:00', 0.05], ['2023-11-22T00:00:00+00:00', 0.04]],
                        'model_name': 'churn_classifier',
                        'viz_type': 'line',
                        'metric': 'jsd',
                        'metric_type': 'performance',
                    },
                    'query_key_accuracy': {
                        'col_names': ['timestamp', 'accuracy'],
                        'data': [['2023-11-21T00:00:00+00:00', 0.90], ['2023-11-22T00:00:00+00:00', 0.92]],
                        'model_name': 'churn_classifier',
                        'viz_type': 'line',
                        'metric': 'accuracy',
                        'metric_type': 'performance',
                    },
                    'query_key_average': {
                        'col_names': ['timestamp', 'average,probability_churn', 'average,creditscore'],
                        'data': [['2023-11-21T00:00:00+00:00', 50, 100], ['2023-11-22T00:00:00+00:00', 52, 101]],
                        'model_name': 'churn_classifier',
                        'viz_type': 'line',
                        'metric': 'average',
                        'metric_type': 'statistic',
                    },
                    'query_key_sum': {
                        'col_names': ['timestamp', 'sum,probability_churn'],
                        'data': [['2023-11-21T00:00:00+00:00', 100], ['2023-11-22T00:00:00+00:00', 104]],
                        'model_name': 'churn_classifier',
                        'viz_type': 'line',
                        'metric': 'sum',
                        'metric_type': 'statistic',
                    },
                    'query_key_data_count': {
                        'col_names': ['timestamp', 'data_count'],
                        'data': [['2023-11-21T00:00:00+00:00', 1000], ['2023-11-22T00:00:00+00:00', 1040]],
                        'model_name': 'churn_classifier',
                        'viz_type': 'line',
                        'metric': 'data_count',
                        'metric_type': 'performance',
                    },
                    'query_key_auroc': {
                        'col_names': ['timestamp', 'auroc'],
                        'data': [['2023-11-21T00:00:00+00:00', 0.95], ['2023-11-22T00:00:00+00:00', 0.96]],
                        'model_name': 'churn_classifier',
                        'viz_type': 'line',
                        'metric': 'auroc',
                        'metric_type': 'performance',
                    },
                    'query_key_auc': {
                        'col_names': ['timestamp', 'auc'],
                        'data': [['2023-11-21T00:00:00+00:00', 0.95], ['2023-11-22T00:00:00+00:00', 0.96]],
                        'model_name': 'churn_classifier',
                        'viz_type': 'line',
                        'metric': 'auc',
                        'metric_type': 'performance',
                    },
                    'query_key_precision': {
                        'col_names': ['timestamp', 'precision'],
                        'data': [['2023-11-21T00:00:00+00:00', 0.95], ['2023-11-22T00:00:00+00:00', 0.96]],
                        'model_name': 'churn_classifier',
                        'viz_type': 'line',
                        'metric': 'precision',
                        'metric_type': 'performance',
                    },
                    'query_key_recall': {
                        'col_names': ['timestamp', 'recall'],
                        'data': [['2023-11-21T00:00:00+00:00', 0.95], ['2023-11-22T00:00:00+00:00', 0.96]],
                        'model_name': 'churn_classifier',
                        'viz_type': 'line',
                        'metric': 'recall',
                        'metric_type': 'performance',
                    },
                    'query_key_fpr': {
                        'col_names': ['timestamp', 'fpr'],
                        'data': [['2023-11-21T00:00:00+00:00', 0.95], ['2023-11-22T00:00:00+00:00', 0.96]],
                        'model_name': 'churn_classifier',
                        'viz_type': 'line',
                        'metric': 'fpr',
                        'metric_type': 'performance',
                    },
                    'query_key_mape': {
                        'col_names': ['timestamp', 'mape'],
                        'data': [['2023-11-21T00:00:00+00:00', 0.95], ['2023-11-22T00:00:00+00:00', 0.96]],
                        'model_name': 'churn_classifier',
                        'viz_type': 'line',
                        'metric': 'mape',
                        'metric_type': 'performance',
                    },
                    'query_key_wmape': {
                        'col_names': ['timestamp', 'wmape'],
                        'data': [['2023-11-21T00:00:00+00:00', 0.95], ['2023-11-22T00:00:00+00:00', 0.96]],
                        'model_name': 'churn_classifier',
                        'viz_type': 'line',
                        'metric': 'wmape',
                        'metric_type': 'performance',
                    },
                    'query_key_mae': {
                        'col_names': ['timestamp', 'mae'],
                        'data': [['2023-11-21T00:00:00+00:00', 100], ['2023-11-22T00:00:00+00:00', 104]],
                        'model_name': 'churn_classifier',
                        'viz_type': 'line',
                        'metric': 'mae',
                        'metric_type': 'performance',
                    },
                    'query_key_mse': {
                        'col_names': ['timestamp', 'mse'],
                        'data': [['2023-11-21T00:00:00+00:00', 100], ['2023-11-22T00:00:00+00:00', 104]],
                        'model_name': 'churn_classifier',
                        'viz_type': 'line',
                        'metric': 'mse',
                        'metric_type': 'performance',
                    },
                    'query_key_r2': {
                        'col_names': ['timestamp', 'r2'],
                        'data': [['2023-11-21T00:00:00+00:00', 100], ['2023-11-22T00:00:00+00:00', 104]],
                        'model_name': 'churn_classifier',
                        'viz_type': 'line',
                        'metric': 'r2',
                        'metric_type': 'performance',
                    },
                    'query_key_calibrated_threshold': {
                        'col_names': ['timestamp', 'calibrated_threshold'],
                        'data': [['2023-11-21T00:00:00+00:00', 0.95], ['2023-11-22T00:00:00+00:00', 0.96]],
                        'model_name': 'churn_classifier',
                        'viz_type': 'line',
                        'metric': 'calibrated_threshold',
                        'metric_type': 'performance',
                    },
                    'query_key_g_mean': {
                        'col_names': ['timestamp', 'g_mean'],
                        'data': [['2023-11-21T00:00:00+00:00', 100], ['2023-11-22T00:00:00+00:00', 104]],
                        'model_name': 'churn_classifier',
                        'viz_type': 'line',
                        'metric': 'g_mean',
                        'metric_type': 'performance',
                    },
                    'query_key_f1_score': {
                        'col_names': ['timestamp', 'f1_score'],
                        'data': [['2023-11-21T00:00:00+00:00', 100], ['2023-11-22T00:00:00+00:00', 104]],
                        'model_name': 'churn_classifier',
                        'viz_type': 'line',
                        'metric': 'f1_score',
                        'metric_type': 'performance',
                    },
                    'query_key_expected_calibration_error': {
                        'col_names': ['timestamp', 'expected_calibration_error'],
                        'data': [['2023-11-21T00:00:00+00:00', 0.05], ['2023-11-22T00:00:00+00:00', 0.04]],
                        'model_name': 'churn_classifier',
                        'viz_type': 'line',
                        'metric': 'expected_calibration_error',
                        'metric_type': 'performance',
                    },
                }
            ],
        },
        'api_version': '2.0',
        'kind': 'NORMAL',
    }


@pytest.fixture
def mock_query_response_all_metrics():
    return {
        'data': {
            'organization': {'id': 'a6423ca2-44af-4392-89cf-05c4a9b381c4', 'name': 'testdd'},
            'project': {'id': 'e4bd2641-461e-4284-babf-8914bf18f20d', 'name': 'nick_dd'},
            'query_type': 'MONITORING',
            'time_comparison': None,
            'filters': {
                'time_label': None,
                'time_range': {'start_time': '2025-01-16 03:26:58', 'end_time': '2025-01-16 04:26:58'},
                'time_zone': 'UTC',
                'bin_size': 'Hour',
            },
            'results': {
                'auc': {
                    'col_names': ['timestamp', 'auc'],
                    'data': [['2025-01-16T04:00:00+00:00', 0.7619712746219789]],
                    'query_key': 'auc',
                    'model': {'id': '8be665fc-1dbc-4b6d-9e9c-24a92fa72a2b', 'name': 'bank_churn', 'version': 'v1'},
                    'viz_type': 'line',
                    'metric': 'auc',
                    'columns': [],
                },
                'auroc': {
                    'col_names': ['timestamp', 'auroc'],
                    'data': [['2025-01-16T04:00:00+00:00', 0.7619712746219789]],
                    'query_key': 'auroc',
                    'model': {'id': '8be665fc-1dbc-4b6d-9e9c-24a92fa72a2b', 'name': 'bank_churn', 'version': 'v1'},
                    'viz_type': 'line',
                    'metric': 'auroc',
                    'columns': [],
                },
                'accuracy': {
                    'col_names': ['timestamp', 'accuracy'],
                    'data': [['2025-01-16T04:00:00+00:00', 0.7633785942492013]],
                    'query_key': 'accuracy',
                    'model': {'id': '8be665fc-1dbc-4b6d-9e9c-24a92fa72a2b', 'name': 'bank_churn', 'version': 'v1'},
                    'viz_type': 'line',
                    'metric': 'accuracy',
                    'columns': [],
                },
                'average': {
                    'col_names': [
                        'timestamp',
                        'average,age',
                        'average,balance',
                        'average,creditscore',
                        'average,estimatedsalary',
                        'average,numofproducts',
                        'average,probability_churned',
                        'average,tenure',
                    ],
                    'data': [
                        [
                            '2025-01-16T04:00:00+00:00',
                            29.910343450479232,
                            85556.22808327297,
                            632.0299520766773,
                            81095.49326821431,
                            1.4880191693290734,
                            0.27643869134970356,
                            4.26517571884984,
                        ]
                    ],
                    'query_key': 'average',
                    'model': {'id': '8be665fc-1dbc-4b6d-9e9c-24a92fa72a2b', 'name': 'bank_churn', 'version': 'v1'},
                    'viz_type': 'line',
                    'metric': 'average',
                    'columns': [
                        'creditscore',
                        'age',
                        'tenure',
                        'balance',
                        'numofproducts',
                        'estimatedsalary',
                        'probability_churned',
                    ],
                },
                'calibrated_threshold': {
                    'col_names': ['timestamp', 'calibrated_threshold'],
                    'data': [['2025-01-16T04:00:00+00:00', 0.20999999999999996]],
                    'query_key': 'calibrated_threshold',
                    'model': {'id': '8be665fc-1dbc-4b6d-9e9c-24a92fa72a2b', 'name': 'bank_churn', 'version': 'v1'},
                    'viz_type': 'line',
                    'metric': 'calibrated_threshold',
                    'columns': [],
                },
                'expected_calibration_error': {
                    'col_names': ['timestamp', 'expected_calibration_error'],
                    'data': [['2025-01-16T04:00:00+00:00', 0.0805311501597444]],
                    'query_key': 'expected_calibration_error',
                    'model': {'id': '8be665fc-1dbc-4b6d-9e9c-24a92fa72a2b', 'name': 'bank_churn', 'version': 'v1'},
                    'viz_type': 'line',
                    'metric': 'expected_calibration_error',
                    'columns': [],
                },
                'f1_score': {
                    'col_names': ['timestamp', 'f1_score'],
                    'data': [['2025-01-16T04:00:00+00:00', 0.4814004376367615]],
                    'query_key': 'f1_score',
                    'model': {'id': '8be665fc-1dbc-4b6d-9e9c-24a92fa72a2b', 'name': 'bank_churn', 'version': 'v1'},
                    'viz_type': 'line',
                    'metric': 'f1_score',
                    'columns': [],
                },
                'fpr': {
                    'col_names': ['timestamp', 'fpr'],
                    'data': [['2025-01-16T04:00:00+00:00', 0.10914534567229178]],
                    'query_key': 'fpr',
                    'model': {'id': '8be665fc-1dbc-4b6d-9e9c-24a92fa72a2b', 'name': 'bank_churn', 'version': 'v1'},
                    'viz_type': 'line',
                    'metric': 'fpr',
                    'columns': [],
                },
                'geometric_mean': {
                    'col_names': ['timestamp', 'geometric_mean'],
                    'data': [['2025-01-16T04:00:00+00:00', 0.48830876097679504]],
                    'query_key': 'geometric_mean',
                    'model': {'id': '8be665fc-1dbc-4b6d-9e9c-24a92fa72a2b', 'name': 'bank_churn', 'version': 'v1'},
                    'viz_type': 'line',
                    'metric': 'geometric_mean',
                    'columns': [],
                },
                'jsd': {
                    'col_names': [
                        'timestamp',
                        'jsd,age',
                        'jsd,balance',
                        'jsd,churned',
                        'jsd,creditscore',
                        'jsd,decisions',
                        'jsd,estimatedsalary',
                        'jsd,gender',
                        'jsd,geography',
                        'jsd,hascrcard',
                        'jsd,isactivemember',
                        'jsd,numofproducts',
                        'jsd,probability_churned',
                        'jsd,tenure',
                    ],
                    'data': [
                        [
                            '2025-01-16T04:00:00+00:00',
                            0.01690929677427003,
                            0.01227213486309167,
                            0.0031412945944094962,
                            0.01681825366631649,
                            0.0,
                            0.018075742038753968,
                            0.0052200229094806535,
                            0.00565356188802863,
                            0.003294246042484123,
                            0.002320628362841629,
                            0.007696440857031694,
                            0.012501877486277853,
                            0.016676093049180003,
                        ]
                    ],
                    'query_key': 'jsd',
                    'model': {'id': '8be665fc-1dbc-4b6d-9e9c-24a92fa72a2b', 'name': 'bank_churn', 'version': 'v1'},
                    'baseline': {'id': '5625bbd8-262d-4246-8dac-d703cca2833f', 'name': 'default_static_baseline'},
                    'viz_type': 'line',
                    'metric': 'jsd',
                    'columns': [
                        'creditscore',
                        'geography',
                        'gender',
                        'age',
                        'tenure',
                        'balance',
                        'numofproducts',
                        'hascrcard',
                        'isactivemember',
                        'estimatedsalary',
                        'churned',
                        'decisions',
                        'probability_churned',
                    ],
                },
                'log_loss': {
                    'col_names': ['timestamp', 'log_loss'],
                    'data': [['2025-01-16T04:00:00+00:00', 0.530702657716497]],
                    'query_key': 'log_loss',
                    'model': {'id': '8be665fc-1dbc-4b6d-9e9c-24a92fa72a2b', 'name': 'bank_churn', 'version': 'v1'},
                    'baseline': {},
                    'viz_type': 'line',
                    'metric': 'log_loss',
                    'columns': [],
                },
                'psi': {
                    'col_names': [
                        'timestamp',
                        'psi,age',
                        'psi,balance',
                        'psi,churned',
                        'psi,creditscore',
                        'psi,decisions',
                        'psi,estimatedsalary',
                        'psi,gender',
                        'psi,geography',
                        'psi,hascrcard',
                        'psi,isactivemember',
                        'psi,numofproducts',
                        'psi,probability_churned',
                        'psi,tenure',
                    ],
                    'data': [
                        [
                            '2025-01-16T04:00:00+00:00',
                            0.0033558799372856753,
                            0.0022704732368361903,
                            0.001578259267871853,
                            0.002295408119522658,
                            0.002280795179247903,
                            0.0027435715580854444,
                            0.0016730032527976324,
                            0.0016949219790024462,
                            0.0015796346473842986,
                            0.0015503609078269974,
                            0.006671550941384573,
                            0.0017025926285851106,
                            0.0017365884780108079,
                        ]
                    ],
                    'query_key': 'psi',
                    'model': {'id': '8be665fc-1dbc-4b6d-9e9c-24a92fa72a2b', 'name': 'bank_churn', 'version': 'v1'},
                    'baseline': {'id': '5625bbd8-262d-4246-8dac-d703cca2833f', 'name': 'default_static_baseline'},
                    'viz_type': 'line',
                    'metric': 'psi',
                    'columns': [
                        'creditscore',
                        'geography',
                        'gender',
                        'age',
                        'tenure',
                        'balance',
                        'numofproducts',
                        'hascrcard',
                        'isactivemember',
                        'estimatedsalary',
                        'churned',
                        'decisions',
                        'probability_churned',
                    ],
                },
                'precision': {
                    'col_names': ['timestamp', 'precision'],
                    'data': [['2025-01-16T04:00:00+00:00', 0.5783385909568874]],
                    'query_key': 'precision',
                    'model': {'id': '8be665fc-1dbc-4b6d-9e9c-24a92fa72a2b', 'name': 'bank_churn', 'version': 'v1'},
                    'baseline': {},
                    'viz_type': 'line',
                    'metric': 'precision',
                    'columns': [],
                },
                'recall': {
                    'col_names': ['timestamp', 'recall'],
                    'data': [['2025-01-16T04:00:00+00:00', 0.4122938530734633]],
                    'query_key': 'recall',
                    'model': {'id': '8be665fc-1dbc-4b6d-9e9c-24a92fa72a2b', 'name': 'bank_churn', 'version': 'v1'},
                    'baseline': {},
                    'viz_type': 'line',
                    'metric': 'recall',
                    'columns': [],
                },
                'sum': {
                    'col_names': [
                        'timestamp',
                        'sum,age',
                        'sum,balance',
                        'sum,creditscore',
                        'sum,estimatedsalary',
                        'sum,numofproducts',
                        'sum,probability_churned',
                        'sum,tenure',
                    ],
                    'data': [
                        [
                            '2025-01-16T04:00:00+00:00',
                            149791,
                            428465590.24103105,
                            3165206,
                            406126230.28721726,
                            7452,
                            1384.4049662793154,
                            21360,
                        ]
                    ],
                    'query_key': 'sum',
                    'model': {'id': '8be665fc-1dbc-4b6d-9e9c-24a92fa72a2b', 'name': 'bank_churn', 'version': 'v1'},
                    'baseline': {},
                    'viz_type': 'line',
                    'metric': 'sum',
                    'columns': [
                        'creditscore',
                        'age',
                        'tenure',
                        'balance',
                        'numofproducts',
                        'estimatedsalary',
                        'probability_churned',
                    ],
                },
                'data_count': {
                    'col_names': ['timestamp', 'data_count'],
                    'data': [['2025-01-16T04:00:00+00:00', 5008]],
                    'query_key': 'data_count',
                    'model': {'id': '8be665fc-1dbc-4b6d-9e9c-24a92fa72a2b', 'name': 'bank_churn', 'version': 'v1'},
                    'baseline': {},
                    'viz_type': 'line',
                    'metric': 'data_count',
                    'columns': [],
                },
                'traffic': {
                    'col_names': ['timestamp', 'traffic'],
                    'data': [['2025-01-16T04:00:00+00:00', 5008]],
                    'query_key': 'traffic',
                    'model': {'id': '8be665fc-1dbc-4b6d-9e9c-24a92fa72a2b', 'name': 'bank_churn', 'version': 'v1'},
                    'baseline': {},
                    'viz_type': 'line',
                    'metric': 'traffic',
                    'columns': [],
                },
            },
        },
        'api_version': '3.0',
        'kind': 'NORMAL',
    }
