from concurrent import futures

import grpc
import pytest
from grpc_health.v1 import health, health_pb2, health_pb2_grpc

from datadog_checks.base import AgentCheck, ConfigurationError
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.grpc_check import GrpcCheck


def create_insecure_grpc_server(expected_status=health_pb2.HealthCheckResponse.SERVING):
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    health_servicer = health.HealthServicer()
    health_servicer.set("grpc.test", expected_status)
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, grpc_server)
    grpc_server.add_insecure_port("localhost:50051")
    return grpc_server


def create_secure_grpc_server(expected_status=health_pb2.HealthCheckResponse.SERVING):
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    health_servicer = health.HealthServicer()
    health_servicer.set("grpc.test", expected_status)
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, grpc_server)
    ca_cert = open("tests/fixtures/ca.pem", "rb").read()
    private_key = open("tests/fixtures/server-key.pem", "rb").read()
    certificate_chain = open("tests/fixtures/server.pem", "rb").read()
    credentials = grpc.ssl_server_credentials(
        [(private_key, certificate_chain)],
        root_certificates=ca_cert,
        require_client_auth=True,
    )
    grpc_server.add_secure_port("localhost:50052", credentials)
    return grpc_server


def test_insecure_server_is_serving(dd_run_check, aggregator):
    instance = {
        "grpc_server_address": "localhost:50051",
        "grpc_server_service": "grpc.test",
        "tags": ["tag_key1:value1", "tag_key2:value2"],
    }
    grpc_server = create_insecure_grpc_server()
    grpc_server.start()

    check = GrpcCheck("grpc_check", {}, [instance])
    dd_run_check(check)
    grpc_server.stop(None)

    expected_tags = [
        "grpc_server_service:grpc.test",
        "grpc_server_address:localhost:50051",
        "status_code:OK",
        "tag_key1:value1",
        "tag_key2:value2",
    ]

    aggregator.assert_metric(
        "grpc_check.healthy",
        value=1.0,
        tags=expected_tags,
        hostname="",
        flush_first_value=False,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        "grpc_check.unhealthy",
        value=0.0,
        tags=expected_tags,
        hostname="",
        flush_first_value=False,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_service_check(
        "grpc.healthy",
        status=AgentCheck.OK,
        tags=expected_tags,
        count=1,
        hostname="",
        message="",
    )
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_insecure_server_is_not_serving(dd_run_check, aggregator):
    instance = {
        "grpc_server_address": "localhost:50051",
        "grpc_server_service": "grpc.test",
        "tags": ["tag_key1:value1", "tag_key2:value2"],
    }
    grpc_server = create_insecure_grpc_server(health_pb2.HealthCheckResponse.NOT_SERVING)
    grpc_server.start()

    check = GrpcCheck("grpc_check", {}, [instance])
    dd_run_check(check)
    grpc_server.stop(None)

    expected_tags = [
        "grpc_server_service:grpc.test",
        "grpc_server_address:localhost:50051",
        "status_code:OK",
        "tag_key1:value1",
        "tag_key2:value2",
    ]

    aggregator.assert_metric(
        "grpc_check.healthy",
        value=0.0,
        tags=expected_tags,
        hostname="",
        flush_first_value=False,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        "grpc_check.unhealthy",
        value=1.0,
        tags=expected_tags,
        hostname="",
        flush_first_value=False,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_service_check(
        "grpc.healthy",
        status=AgentCheck.CRITICAL,
        tags=expected_tags,
        count=1,
        hostname="",
        message="",
    )
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_insecure_server_is_unknown(dd_run_check, aggregator):
    instance = {
        "grpc_server_address": "localhost:50051",
        "grpc_server_service": "grpc.test",
        "tags": ["tag_key1:value1", "tag_key2:value2"],
    }
    grpc_server = create_insecure_grpc_server(health_pb2.HealthCheckResponse.UNKNOWN)
    grpc_server.start()

    check = GrpcCheck("grpc_check", {}, [instance])
    dd_run_check(check)
    grpc_server.stop(None)

    expected_tags = [
        "grpc_server_service:grpc.test",
        "grpc_server_address:localhost:50051",
        "status_code:OK",
        "tag_key1:value1",
        "tag_key2:value2",
    ]

    aggregator.assert_metric(
        "grpc_check.healthy",
        value=0.0,
        tags=expected_tags,
        hostname="",
        flush_first_value=False,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        "grpc_check.unhealthy",
        value=1.0,
        tags=expected_tags,
        hostname="",
        flush_first_value=False,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_service_check(
        "grpc.healthy",
        status=AgentCheck.CRITICAL,
        tags=expected_tags,
        count=1,
        hostname="",
        message="",
    )
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_unavailable(dd_run_check, aggregator):
    instance = {
        "grpc_server_address": "localhost:80",
        "grpc_server_service": "grpc.test",
        "tags": ["tag_key1:value1", "tag_key2:value2"],
    }
    grpc_server = create_insecure_grpc_server()
    grpc_server.start()

    check = GrpcCheck("grpc_check", {}, [instance])
    dd_run_check(check)
    grpc_server.stop(None)

    expected_tags = [
        "grpc_server_service:grpc.test",
        "grpc_server_address:localhost:80",
        "status_code:UNAVAILABLE",
        "tag_key1:value1",
        "tag_key2:value2",
    ]

    aggregator.assert_metric(
        "grpc_check.healthy",
        value=0.0,
        tags=expected_tags,
        hostname="",
        flush_first_value=False,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        "grpc_check.unhealthy",
        value=1.0,
        tags=expected_tags,
        hostname="",
        flush_first_value=False,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_service_check(
        "grpc.healthy",
        status=AgentCheck.CRITICAL,
        tags=expected_tags,
        count=1,
        hostname="",
        message="",
    )
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_timeout(dd_run_check, aggregator):
    instance = {
        "grpc_server_address": "localhost:50051",
        "timeout": 0.00001,
        "grpc_server_service": "grpc.test",
        "tags": ["tag_key1:value1", "tag_key2:value2"],
    }
    grpc_server = create_insecure_grpc_server()
    grpc_server.start()

    check = GrpcCheck("grpc_check", {}, [instance])
    dd_run_check(check)
    grpc_server.stop(None)

    expected_tags = [
        "grpc_server_service:grpc.test",
        "grpc_server_address:localhost:50051",
        "status_code:DEADLINE_EXCEEDED",
        "tag_key1:value1",
        "tag_key2:value2",
    ]

    aggregator.assert_metric(
        "grpc_check.healthy",
        value=0.0,
        tags=expected_tags,
        hostname="",
        flush_first_value=False,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        "grpc_check.unhealthy",
        value=1.0,
        tags=expected_tags,
        hostname="",
        flush_first_value=False,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_service_check(
        "grpc.healthy",
        status=AgentCheck.CRITICAL,
        tags=expected_tags,
        count=1,
        hostname="",
        message="",
    )
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_not_found(dd_run_check, aggregator):
    instance = {
        "grpc_server_address": "localhost:50051",
        "grpc_server_service": "not_found",
        "tags": ["tag_key1:value1", "tag_key2:value2"],
    }
    grpc_server = create_insecure_grpc_server()
    grpc_server.start()

    check = GrpcCheck("grpc_check", {}, [instance])
    dd_run_check(check)
    grpc_server.stop(None)

    expected_tags = [
        "grpc_server_service:not_found",
        "grpc_server_address:localhost:50051",
        "status_code:NOT_FOUND",
        "tag_key1:value1",
        "tag_key2:value2",
    ]

    aggregator.assert_metric(
        "grpc_check.healthy",
        value=0.0,
        tags=expected_tags,
        hostname="",
        flush_first_value=False,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        "grpc_check.unhealthy",
        value=1.0,
        tags=expected_tags,
        hostname="",
        flush_first_value=False,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_service_check(
        "grpc.healthy",
        status=AgentCheck.CRITICAL,
        tags=expected_tags,
        count=1,
        hostname="",
        message="",
    )
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_secure_server_is_serving(dd_run_check, aggregator):
    instance = {
        "grpc_server_address": "localhost:50052",
        "grpc_server_service": "grpc.test",
        "tags": ["tag_key1:value1", "tag_key2:value2"],
        "ca_cert": "tests/fixtures/ca.pem",
        "client_cert": "tests/fixtures/client.pem",
        "client_key": "tests/fixtures/client-key.pem",
    }
    grpc_server = create_secure_grpc_server()
    grpc_server.start()

    check = GrpcCheck("grpc_check", {}, [instance])
    dd_run_check(check)
    grpc_server.stop(None)

    expected_tags = [
        "grpc_server_service:grpc.test",
        "grpc_server_address:localhost:50052",
        "status_code:OK",
        "tag_key1:value1",
        "tag_key2:value2",
    ]

    aggregator.assert_metric(
        "grpc_check.healthy",
        value=1.0,
        tags=expected_tags,
        hostname="",
        flush_first_value=False,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        "grpc_check.unhealthy",
        value=0.0,
        tags=expected_tags,
        hostname="",
        flush_first_value=False,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_service_check(
        "grpc.healthy",
        status=AgentCheck.OK,
        tags=expected_tags,
        count=1,
        hostname="",
        message="",
    )
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_secure_server_is_not_serving(dd_run_check, aggregator):
    instance = {
        "grpc_server_address": "localhost:50052",
        "grpc_server_service": "grpc.test",
        "tags": ["tag_key1:value1", "tag_key2:value2"],
        "ca_cert": "tests/fixtures/ca.pem",
        "client_cert": "tests/fixtures/client.pem",
        "client_key": "tests/fixtures/client-key.pem",
    }
    grpc_server = create_secure_grpc_server(health_pb2.HealthCheckResponse.NOT_SERVING)
    grpc_server.start()

    check = GrpcCheck("grpc_check", {}, [instance])
    dd_run_check(check)
    grpc_server.stop(None)

    expected_tags = [
        "grpc_server_service:grpc.test",
        "grpc_server_address:localhost:50052",
        "status_code:OK",
        "tag_key1:value1",
        "tag_key2:value2",
    ]

    aggregator.assert_metric(
        "grpc_check.healthy",
        value=0.0,
        tags=expected_tags,
        hostname="",
        flush_first_value=False,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        "grpc_check.unhealthy",
        value=1.0,
        tags=expected_tags,
        hostname="",
        flush_first_value=False,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_service_check(
        "grpc.healthy",
        status=AgentCheck.CRITICAL,
        tags=expected_tags,
        count=1,
        hostname="",
        message="",
    )
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_secure_server_is_unknown(dd_run_check, aggregator):
    instance = {
        "grpc_server_address": "localhost:50052",
        "grpc_server_service": "grpc.test",
        "tags": ["tag_key1:value1", "tag_key2:value2"],
        "ca_cert": "tests/fixtures/ca.pem",
        "client_cert": "tests/fixtures/client.pem",
        "client_key": "tests/fixtures/client-key.pem",
    }
    grpc_server = create_secure_grpc_server(health_pb2.HealthCheckResponse.UNKNOWN)
    grpc_server.start()

    check = GrpcCheck("grpc_check", {}, [instance])
    dd_run_check(check)
    grpc_server.stop(None)

    expected_tags = [
        "grpc_server_service:grpc.test",
        "grpc_server_address:localhost:50052",
        "status_code:OK",
        "tag_key1:value1",
        "tag_key2:value2",
    ]

    aggregator.assert_metric(
        "grpc_check.healthy",
        value=0.0,
        tags=expected_tags,
        hostname="",
        flush_first_value=False,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        "grpc_check.unhealthy",
        value=1.0,
        tags=expected_tags,
        hostname="",
        flush_first_value=False,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_service_check(
        "grpc.healthy",
        status=AgentCheck.CRITICAL,
        tags=expected_tags,
        count=1,
        hostname="",
        message="",
    )
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_ca_cert_missing():
    instance = {
        "grpc_server_address": "localhost:50052",
        "grpc_server_service": "grpc.test",
        "tags": ["tag_key1:value1", "tag_key2:value2"],
        # missing ca_cert
        "client_cert": "tests/fixtures/client.pem",
        "client_key": "tests/fixtures/client-key.pem",
    }
    with pytest.raises(
        ConfigurationError,
        match="^ca_cert, client_cert or client_key is missing$",
    ):
        GrpcCheck("grpc_check", {}, [instance])


def test_client_cert_missing():
    instance = {
        "grpc_server_address": "localhost:50052",
        "grpc_server_service": "grpc.test",
        "tags": ["tag_key1:value1", "tag_key2:value2"],
        "ca_cert": "tests/fixtures/ca.pem",
        # missing client_cert
        "client_key": "tests/fixtures/client-key.pem",
    }
    with pytest.raises(
        ConfigurationError,
        match="^ca_cert, client_cert or client_key is missing$",
    ):
        GrpcCheck("grpc_check", {}, [instance])


def test_client_key_missing():
    instance = {
        "grpc_server_address": "localhost:50052",
        "grpc_server_service": "grpc.test",
        "tags": ["tag_key1:value1", "tag_key2:value2"],
        "ca_cert": "tests/fixtures/ca.pem",
        "client_cert": "tests/fixtures/client.pem",
        # missing client_key
    }
    with pytest.raises(
        ConfigurationError,
        match="^ca_cert, client_cert or client_key is missing$",
    ):
        GrpcCheck("grpc_check", {}, [instance])


def test_empty_instance():
    instance = {}
    with pytest.raises(ConfigurationError, match="^grpc_server_address must be specified$"):
        GrpcCheck("grpc_check", {}, [instance])


def test_timeout_zero():
    instance = {"grpc_server_address": "localhost:50051", "timeout": 0}
    with pytest.raises(ConfigurationError, match="^timeout must be greater than zero$"):
        GrpcCheck("grpc_check", {}, [instance])


@pytest.mark.integration
@pytest.mark.usefixtures("dd_environment")
def test_check_integration(dd_run_check, aggregator, instance):
    check = GrpcCheck("grpc_check", {}, [instance])
    dd_run_check(check)

    expected_tags = [
        "grpc_server_service:",
        "grpc_server_address:localhost:50051",
        "status_code:OK",
    ]

    aggregator.assert_metric(
        "grpc_check.healthy",
        value=1.0,
        tags=expected_tags,
        hostname="",
        flush_first_value=False,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        "grpc_check.unhealthy",
        value=0.0,
        tags=expected_tags,
        hostname="",
        flush_first_value=False,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_service_check(
        "grpc.healthy",
        status=AgentCheck.OK,
        tags=expected_tags,
        count=1,
        hostname="",
        message="",
    )
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
