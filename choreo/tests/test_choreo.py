import pytest

from datadog_checks.choreo import ChoreoCheck


# Run the Choreo check and test if the metrics are properly scraped.
@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_metrics(dd_run_check, aggregator, instance):
    c = ChoreoCheck('choreo', {}, [instance])
    print("before dd_run_check")
    dd_run_check(c)

    # Common OpenMetrics tags from the "success" function
    success_function_labels = [
        'entrypoint_function_module:datadog_choreo/success_failure:0.1.0',
        'listener_name:http',
        'src_position:main.bal:5:5',
        'protocol:http',
        'entrypoint_function_name:/success',
        'entrypoint_resource_accessor:get',
        'src_service_resource:true',
        'http_url:/srvc/success',
        'src_resource_accessor:get',
        'src_object_name:/srvc',
        'entrypoint_service_name:/srvc',
        'src_resource_path:/success',
        'src_module:datadog_choreo/success_failure:0.1.0',
        'http_method:GET',
        'endpoint:http://localhost:9797/metrics',
    ]

    # Common OpenMetrics tags from the "failure" function
    failure_function_labels = [
        'entrypoint_function_module:datadog_choreo/success_failure:0.1.0',
        'listener_name:http',
        'protocol:http',
        'src_resource_path:/failure',
        'entrypoint_resource_accessor:get',
        'src_service_resource:true',
        'http_url:/srvc/failure',
        'src_resource_accessor:get',
        'src_position:main.bal:9:5',
        'src_object_name:/srvc',
        'entrypoint_service_name:/srvc',
        'entrypoint_function_name:/failure',
        'src_module:datadog_choreo/success_failure:0.1.0',
        'http_method:GET',
        'endpoint:http://localhost:9797/metrics',
    ]

    aggregator.assert_metric(
        'choreo.ballerina.requests.total.value.count',
        value=40.0,
        tags=success_function_labels + ['http_status_code_group:2xx'],
    )
    aggregator.assert_metric(
        'choreo.ballerina.requests.total.value.count',
        value=39.0,
        tags=failure_function_labels + ['error:true', 'http_status_code_group:5xx'],
    )
    aggregator.assert_metric('choreo.ballerina.inprogress_requests.value', value=0.0, tags=success_function_labels)
    aggregator.assert_metric('choreo.ballerina.inprogress_requests.value', value=0.0, tags=failure_function_labels)
    aggregator.assert_metric(
        'choreo.ballerina.response_time.nanoseconds.total.value.count',
        value=315155084.0,
        tags=success_function_labels + ['http_status_code_group:2xx'],
    )
    aggregator.assert_metric(
        'choreo.ballerina.response_time.nanoseconds.total.value.count',
        value=373700086.0,
        tags=failure_function_labels + ['error:true', 'http_status_code_group:5xx'],
    )
    aggregator.assert_metric(
        'choreo.ballerina.response_time.seconds.quantile',
        value=0.01110076904296875,
        tags=success_function_labels + ['http_status_code_group:2xx', 'timeWindow:10000', 'quantile:0.99'],
    )
    aggregator.assert_metric(
        'choreo.ballerina.response_time.seconds.quantile',
        value=0.02220916748046875,
        tags=failure_function_labels
        + ['timeWindow:10000', 'quantile:0.99', 'error:true', 'http_status_code_group:5xx'],
    )
    aggregator.assert_metric(
        'choreo.ballerina.response_time.seconds.value',
        value=0.010873417,
        tags=success_function_labels + ['http_status_code_group:2xx'],
    )
    aggregator.assert_metric(
        'choreo.ballerina.response_time.seconds.value',
        value=0.009806958,
        tags=failure_function_labels + ['error:true', 'http_status_code_group:5xx'],
    )
    aggregator.assert_metric(
        'choreo.ballerina.response_time.seconds.mean.quantile',
        value=0.005082130432128906,
        tags=success_function_labels + ['http_status_code_group:2xx', 'timeWindow:10000'],
    )
    aggregator.assert_metric(
        'choreo.ballerina.response_time.seconds.mean.quantile',
        value=0.0069103240966796875,
        tags=failure_function_labels + ['timeWindow:10000', 'error:true', 'http_status_code_group:5xx'],
    )
    aggregator.assert_metric(
        'choreo.ballerina.response_time.seconds.max.quantile',
        value=0.01110076904296875,
        tags=success_function_labels + ['http_status_code_group:2xx', 'timeWindow:10000'],
    )
    aggregator.assert_metric(
        'choreo.ballerina.response_time.seconds.max.quantile',
        value=0.02220916748046875,
        tags=failure_function_labels + ['timeWindow:10000', 'error:true', 'http_status_code_group:5xx'],
    )
    aggregator.assert_metric(
        'choreo.ballerina.response_time.seconds.min.quantile',
        value=0.0010528564453125,
        tags=success_function_labels + ['http_status_code_group:2xx', 'timeWindow:10000'],
    )
    aggregator.assert_metric(
        'choreo.ballerina.response_time.seconds.min.quantile',
        value=0.0015869140625,
        tags=failure_function_labels + ['timeWindow:10000', 'error:true', 'http_status_code_group:5xx'],
    )
    aggregator.assert_metric(
        'choreo.ballerina.response_time.seconds.stdDev.quantile',
        value=0.004585436593280697,
        tags=success_function_labels + ['http_status_code_group:2xx', 'timeWindow:10000'],
    )
    aggregator.assert_metric(
        'choreo.ballerina.response_time.seconds.stdDev.quantile',
        value=0.006806371124147402,
        tags=failure_function_labels + ['timeWindow:10000', 'error:true', 'http_status_code_group:5xx'],
    )


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_duplicate_metrics(dd_run_check, aggregator, instance):
    c = ChoreoCheck('choreo', {}, [instance])
    dd_run_check(c)
    aggregator.assert_no_duplicate_metrics()
