import os

import pytest

from datadog_checks.dev import docker_run, get_docker_hostname, get_here

URL = 'http://{}:9000'.format(get_docker_hostname())
INSTANCE = {'url': 'http://example.com', "fiddler_api_key": 'testtoken', 'organization': 'test_org'}


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
def mock_metrics_response_data():
    return {
        "data": {
            "metric_types": [
                {"display_name": "Data Drift", "key": "drift"},
                {"display_name": "Data Integrity", "key": "data_integrity"},
                {"display_name": "Performance", "key": "performance"},
                {"display_name": "Traffic", "key": "service_metrics"},
                {"display_name": "Statistic", "key": "statistic"},
                {"display_name": "Custom Metric", "key": "custom"},
            ],
            "columns": [
                {"display_name": "All columns", "key": "__ANY__"},
                {"display_name": "creditscore", "data_type": "int", "key": "creditscore", "group": "Inputs"},
                {"display_name": "geography", "data_type": "category", "key": "geography", "group": "Inputs"},
                {"display_name": "age", "data_type": "int", "key": "age", "group": "Inputs"},
                {"display_name": "tenure", "data_type": "int", "key": "tenure", "group": "Inputs"},
                {"display_name": "balance", "data_type": "float", "key": "balance", "group": "Inputs"},
                {"display_name": "numofproducts", "data_type": "int", "key": "numofproducts", "group": "Inputs"},
                {"display_name": "hascrcard", "data_type": "int", "key": "hascrcard", "group": "Inputs"},
                {"display_name": "isactivemember", "data_type": "int", "key": "isactivemember", "group": "Inputs"},
                {"display_name": "estimatedsalary", "data_type": "float", "key": "estimatedsalary", "group": "Inputs"},
                {
                    "display_name": "probability_churn",
                    "data_type": "float",
                    "key": "probability_churn",
                    "group": "Outputs",
                },
                {"display_name": "churn", "data_type": "category", "key": "churn", "group": "Targets"},
                {"display_name": "decisions", "data_type": "category", "key": "decisions", "group": "Decisions"},
                {"display_name": "gender", "data_type": "category", "key": "gender", "group": "Metadata"},
            ],
            "metrics": [
                {
                    "display_name": "AUC",
                    "key": "auc",
                    "needs_baseline": False,
                    "type": "performance",
                    "needs_categories": False,
                    "columns": [],
                },
                {
                    "display_name": "AUROC",
                    "key": "auroc",
                    "needs_baseline": False,
                    "type": "performance",
                    "needs_categories": False,
                    "columns": [],
                },
                {
                    "display_name": "Accuracy",
                    "key": "accuracy",
                    "needs_baseline": False,
                    "type": "performance",
                    "needs_categories": False,
                    "columns": [],
                },
                {
                    "display_name": "Any Violation",
                    "key": "any_violation_count",
                    "needs_baseline": False,
                    "type": "data_integrity",
                    "needs_categories": False,
                    "columns": [
                        "__ANY__",
                        "creditscore",
                        "geography",
                        "age",
                        "tenure",
                        "balance",
                        "numofproducts",
                        "hascrcard",
                        "isactivemember",
                        "estimatedsalary",
                        "probability_churn",
                        "gender",
                        "decisions",
                        "churn",
                    ],
                },
                {
                    "display_name": "Average",
                    "key": "average",
                    "needs_baseline": False,
                    "type": "statistic",
                    "needs_categories": False,
                    "columns": [
                        "creditscore",
                        "age",
                        "tenure",
                        "balance",
                        "numofproducts",
                        "hascrcard",
                        "isactivemember",
                        "estimatedsalary",
                        "probability_churn",
                    ],
                },
                {
                    "display_name": "Calibrated Threshold",
                    "key": "calibrated_threshold",
                    "needs_baseline": False,
                    "type": "performance",
                    "needs_categories": False,
                    "columns": [],
                },
                {
                    "display_name": "Expected Calibration Error",
                    "key": "expected_calibration_error",
                    "needs_baseline": False,
                    "type": "performance",
                    "needs_categories": False,
                    "columns": [],
                },
                {
                    "display_name": "F1",
                    "key": "f1_score",
                    "needs_baseline": False,
                    "type": "performance",
                    "needs_categories": False,
                    "columns": [],
                },
                {
                    "display_name": "False Positive Count",
                    "key": "90140dfc-8600-46d4-b2e1-2105c7c17852",
                    "needs_baseline": False,
                    "type": "custom",
                    "needs_categories": False,
                    "columns": [],
                },
                {
                    "display_name": "False Positive Rate",
                    "key": "fpr",
                    "needs_baseline": False,
                    "type": "performance",
                    "needs_categories": False,
                    "columns": [],
                },
                {
                    "display_name": "Frequency",
                    "key": "frequency",
                    "needs_baseline": False,
                    "type": "statistic",
                    "needs_categories": True,
                    "columns": ["geography", "gender", "decisions", "churn"],
                },
                {
                    "display_name": "Geometric Mean",
                    "key": "geometric_mean",
                    "needs_baseline": False,
                    "type": "performance",
                    "needs_categories": False,
                    "columns": [],
                },
                {
                    "display_name": "Jensen-Shannon Distance",
                    "key": "jsd",
                    "needs_baseline": True,
                    "type": "drift",
                    "needs_categories": False,
                    "columns": [
                        "creditscore",
                        "geography",
                        "age",
                        "tenure",
                        "balance",
                        "numofproducts",
                        "hascrcard",
                        "isactivemember",
                        "estimatedsalary",
                        "probability_churn",
                        "gender",
                        "decisions",
                        "churn",
                    ],
                },
                {
                    "display_name": "Log Loss",
                    "key": "log_loss",
                    "needs_baseline": False,
                    "type": "performance",
                    "needs_categories": False,
                    "columns": [],
                },
                {
                    "display_name": "Missing Value Violation",
                    "key": "null_violation_count",
                    "needs_baseline": False,
                    "type": "data_integrity",
                    "needs_categories": False,
                    "columns": [
                        "__ANY__",
                        "creditscore",
                        "geography",
                        "age",
                        "tenure",
                        "balance",
                        "numofproducts",
                        "hascrcard",
                        "isactivemember",
                        "estimatedsalary",
                        "probability_churn",
                        "gender",
                        "decisions",
                        "churn",
                    ],
                },
                {
                    "display_name": "Population Stability Index",
                    "key": "psi",
                    "needs_baseline": True,
                    "type": "drift",
                    "needs_categories": False,
                    "columns": [
                        "creditscore",
                        "geography",
                        "age",
                        "tenure",
                        "balance",
                        "numofproducts",
                        "hascrcard",
                        "isactivemember",
                        "estimatedsalary",
                        "probability_churn",
                        "gender",
                        "decisions",
                        "churn",
                    ],
                },
                {
                    "display_name": "Precision",
                    "key": "precision",
                    "needs_baseline": False,
                    "type": "performance",
                    "needs_categories": False,
                    "columns": [],
                },
                {
                    "display_name": "Range Violation",
                    "key": "range_violation_count",
                    "needs_baseline": False,
                    "type": "data_integrity",
                    "needs_categories": False,
                    "columns": [
                        "__ANY__",
                        "creditscore",
                        "geography",
                        "age",
                        "tenure",
                        "balance",
                        "numofproducts",
                        "hascrcard",
                        "isactivemember",
                        "estimatedsalary",
                        "probability_churn",
                        "gender",
                        "decisions",
                        "churn",
                    ],
                },
                {
                    "display_name": "Recall / TPR",
                    "key": "recall",
                    "needs_baseline": False,
                    "type": "performance",
                    "needs_categories": False,
                    "columns": [],
                },
                {
                    "display_name": "Revenue Lost",
                    "key": "c09ffcb5-1fe0-485f-93b7-4fb735624407",
                    "needs_baseline": False,
                    "type": "custom",
                    "needs_categories": False,
                    "columns": [],
                },
                {
                    "display_name": "Sum",
                    "key": "sum",
                    "needs_baseline": False,
                    "type": "statistic",
                    "needs_categories": False,
                    "columns": [
                        "creditscore",
                        "age",
                        "tenure",
                        "balance",
                        "numofproducts",
                        "hascrcard",
                        "isactivemember",
                        "estimatedsalary",
                        "probability_churn",
                    ],
                },
                {
                    "display_name": "Total Count",
                    "key": "data_count",
                    "needs_baseline": False,
                    "type": "performance",
                    "needs_categories": False,
                    "columns": [],
                },
                {
                    "display_name": "Traffic",
                    "key": "traffic",
                    "needs_baseline": False,
                    "type": "service_metrics",
                    "needs_categories": False,
                    "columns": [],
                },
                {
                    "display_name": "Type Violation",
                    "key": "type_violation_count",
                    "needs_baseline": False,
                    "type": "data_integrity",
                    "needs_categories": False,
                    "columns": [
                        "__ANY__",
                        "creditscore",
                        "geography",
                        "age",
                        "tenure",
                        "balance",
                        "numofproducts",
                        "hascrcard",
                        "isactivemember",
                        "estimatedsalary",
                        "probability_churn",
                        "gender",
                        "decisions",
                        "churn",
                    ],
                },
            ],
            "model": "churn_classifier",
        },
        "api_version": "2.0",
        "kind": "NORMAL",
    }


@pytest.fixture
def mock_list_projects_response_data():
    return {"data": {"projects": [{"name": "project1"}, {"name": "project2"}, {"name": "project3"}]}}


@pytest.fixture
def mock_list_models_response_data():
    return {"data": {"items": [{"name": "model1"}, {"name": "model2"}, {"name": "model3"}]}}


@pytest.fixture
def mock_metrics():
    return ([{'key': 'traffic', 'type': 'service_metrics'}], ['output1', 'output2'])


@pytest.fixture
def mock_queries_response_data():
    return {
        "data": {
            "organization_name": "demo",
            "project_name": "bank_churn",
            "time_comparison": None,
            "filters": {"bin_size": "Day", "time_zone": "UTC", "time_label": "7d"},
            "query_type": "MONITORING",
            "results": [
                {
                    "fddc4480-e262-41b8-8cc2-13249683c378": {
                        "col_names": ["timestamp", "traffic"],
                        "data": [
                            # Sample data points, include as many as needed for the test
                            ["2023-11-21T00:00:00+00:00", 294],
                            ["2023-11-22T00:00:00+00:00", 290],
                            ["2023-11-23T00:00:00+00:00", 20],
                            ["2023-11-24T00:00:00+00:00", 200],
                            ["2023-11-25T00:00:00+00:00", 190],
                            ["2023-11-26T00:00:00+00:00", 590],
                            ["2023-11-27T00:00:00+00:00", None],
                        ],
                        "query_key": "fddc4480-e262-41b8-8cc2-13249683c378",
                        "model_name": "churn_classifier",
                        "viz_type": "line",
                        "metric": "traffic",
                        "metric_type": "service_metrics",
                        "columns": [],
                    }
                }
            ],
        },
        "api_version": "2.0",
        "kind": "NORMAL",
    }


@pytest.fixture
def mock_query_expanded_response_data():
    return {
        "data": {
            "organization_name": "demo",
            "project_name": "bank_churn",
            "time_comparison": None,
            "filters": {"bin_size": "Day", "time_zone": "UTC", "time_label": "30d"},
            "query_type": "MONITORING",
            "results": [
                {
                    "query_key_traffic": {
                        "col_names": ["timestamp", "traffic"],
                        "data": [["2023-11-21T00:00:00+00:00", 294], ["2023-11-22T00:00:00+00:00", 290]],
                        "model_name": "churn_classifier",
                        "viz_type": "line",
                        "metric": "traffic",
                        "metric_type": "service_metrics",
                    },
                    "query_key_jsd": {
                        "col_names": ["timestamp", "probability_churn"],
                        "data": [["2023-11-21T00:00:00+00:00", 0.05], ["2023-11-22T00:00:00+00:00", 0.04]],
                        "model_name": "churn_classifier",
                        "viz_type": "line",
                        "metric": "jsd",
                        "metric_type": "performance",
                    },
                    "query_key_accuracy": {
                        "col_names": ["timestamp", "accuracy"],
                        "data": [["2023-11-21T00:00:00+00:00", 0.90], ["2023-11-22T00:00:00+00:00", 0.92]],
                        "model_name": "churn_classifier",
                        "viz_type": "line",
                        "metric": "accuracy",
                        "metric_type": "performance",
                    },
                    "query_key_average": {
                        "col_names": ["timestamp", "average,probability_churn", "average,creditscore"],
                        "data": [["2023-11-21T00:00:00+00:00", 50, 100], ["2023-11-22T00:00:00+00:00", 52, 101]],
                        "model_name": "churn_classifier",
                        "viz_type": "line",
                        "metric": "average",
                        "metric_type": "statistic",
                    },
                    "query_key_sum": {
                        "col_names": ["timestamp", "sum,probability_churn"],
                        "data": [["2023-11-21T00:00:00+00:00", 100], ["2023-11-22T00:00:00+00:00", 104]],
                        "model_name": "churn_classifier",
                        "viz_type": "line",
                        "metric": "sum",
                        "metric_type": "statistic",
                    },
                    "query_key_data_count": {
                        "col_names": ["timestamp", "data_count"],
                        "data": [["2023-11-21T00:00:00+00:00", 1000], ["2023-11-22T00:00:00+00:00", 1040]],
                        "model_name": "churn_classifier",
                        "viz_type": "line",
                        "metric": "data_count",
                        "metric_type": "performance",
                    },
                    "query_key_auroc": {
                        "col_names": ["timestamp", "auroc"],
                        "data": [["2023-11-21T00:00:00+00:00", 0.95], ["2023-11-22T00:00:00+00:00", 0.96]],
                        "model_name": "churn_classifier",
                        "viz_type": "line",
                        "metric": "auroc",
                        "metric_type": "performance",
                    },
                    "query_key_auc": {
                        "col_names": ["timestamp", "auc"],
                        "data": [["2023-11-21T00:00:00+00:00", 0.95], ["2023-11-22T00:00:00+00:00", 0.96]],
                        "model_name": "churn_classifier",
                        "viz_type": "line",
                        "metric": "auc",
                        "metric_type": "performance",
                    },
                    "query_key_precision": {
                        "col_names": ["timestamp", "precision"],
                        "data": [["2023-11-21T00:00:00+00:00", 0.95], ["2023-11-22T00:00:00+00:00", 0.96]],
                        "model_name": "churn_classifier",
                        "viz_type": "line",
                        "metric": "precision",
                        "metric_type": "performance",
                    },
                    "query_key_recall": {
                        "col_names": ["timestamp", "recall"],
                        "data": [["2023-11-21T00:00:00+00:00", 0.95], ["2023-11-22T00:00:00+00:00", 0.96]],
                        "model_name": "churn_classifier",
                        "viz_type": "line",
                        "metric": "recall",
                        "metric_type": "performance",
                    },
                    "query_key_fpr": {
                        "col_names": ["timestamp", "fpr"],
                        "data": [["2023-11-21T00:00:00+00:00", 0.95], ["2023-11-22T00:00:00+00:00", 0.96]],
                        "model_name": "churn_classifier",
                        "viz_type": "line",
                        "metric": "fpr",
                        "metric_type": "performance",
                    },
                    "query_key_mape": {
                        "col_names": ["timestamp", "mape"],
                        "data": [["2023-11-21T00:00:00+00:00", 0.95], ["2023-11-22T00:00:00+00:00", 0.96]],
                        "model_name": "churn_classifier",
                        "viz_type": "line",
                        "metric": "mape",
                        "metric_type": "performance",
                    },
                    "query_key_wmape": {
                        "col_names": ["timestamp", "wmape"],
                        "data": [["2023-11-21T00:00:00+00:00", 0.95], ["2023-11-22T00:00:00+00:00", 0.96]],
                        "model_name": "churn_classifier",
                        "viz_type": "line",
                        "metric": "wmape",
                        "metric_type": "performance",
                    },
                    "query_key_mae": {
                        "col_names": ["timestamp", "mae"],
                        "data": [["2023-11-21T00:00:00+00:00", 100], ["2023-11-22T00:00:00+00:00", 104]],
                        "model_name": "churn_classifier",
                        "viz_type": "line",
                        "metric": "mae",
                        "metric_type": "performance",
                    },
                    "query_key_mse": {
                        "col_names": ["timestamp", "mse"],
                        "data": [["2023-11-21T00:00:00+00:00", 100], ["2023-11-22T00:00:00+00:00", 104]],
                        "model_name": "churn_classifier",
                        "viz_type": "line",
                        "metric": "mse",
                        "metric_type": "performance",
                    },
                    "query_key_r2": {
                        "col_names": ["timestamp", "r2"],
                        "data": [["2023-11-21T00:00:00+00:00", 100], ["2023-11-22T00:00:00+00:00", 104]],
                        "model_name": "churn_classifier",
                        "viz_type": "line",
                        "metric": "r2",
                        "metric_type": "performance",
                    },
                    "query_key_calibrated_threshold": {
                        "col_names": ["timestamp", "calibrated_threshold"],
                        "data": [["2023-11-21T00:00:00+00:00", 0.95], ["2023-11-22T00:00:00+00:00", 0.96]],
                        "model_name": "churn_classifier",
                        "viz_type": "line",
                        "metric": "calibrated_threshold",
                        "metric_type": "performance",
                    },
                    "query_key_g_mean": {
                        "col_names": ["timestamp", "g_mean"],
                        "data": [["2023-11-21T00:00:00+00:00", 100], ["2023-11-22T00:00:00+00:00", 104]],
                        "model_name": "churn_classifier",
                        "viz_type": "line",
                        "metric": "g_mean",
                        "metric_type": "performance",
                    },
                    "query_key_f1_score": {
                        "col_names": ["timestamp", "f1_score"],
                        "data": [["2023-11-21T00:00:00+00:00", 100], ["2023-11-22T00:00:00+00:00", 104]],
                        "model_name": "churn_classifier",
                        "viz_type": "line",
                        "metric": "f1_score",
                        "metric_type": "performance",
                    },
                    "query_key_expected_calibration_error": {
                        "col_names": ["timestamp", "expected_calibration_error"],
                        "data": [["2023-11-21T00:00:00+00:00", 0.05], ["2023-11-22T00:00:00+00:00", 0.04]],
                        "model_name": "churn_classifier",
                        "viz_type": "line",
                        "metric": "expected_calibration_error",
                        "metric_type": "performance",
                    },
                }
            ],
        },
        "api_version": "2.0",
        "kind": "NORMAL",
    }
