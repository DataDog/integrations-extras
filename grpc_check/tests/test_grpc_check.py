from concurrent import futures
from unittest import mock

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


def test_timeout_deadline_exceeded(dd_run_check, aggregator):
    instance = {
        "grpc_server_address": "localhost:50051",
        "timeout": 1,
        "grpc_server_service": "grpc.test",
        "tags": ["tag_key1:value1", "tag_key2:value2"],
    }

    check = GrpcCheck("grpc_check", {}, [instance])

    class MockRpcError(grpc.RpcError):
        def code(self):
            return grpc.StatusCode.DEADLINE_EXCEEDED

        def details(self):
            return "Deadline Exceeded"

    mock_stub_instance = mock.Mock()
    mock_stub_instance.Check.side_effect = MockRpcError()

    with mock.patch('grpc_health.v1.health_pb2_grpc.HealthStub', return_value=mock_stub_instance):
        dd_run_check(check)

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


@pytest.mark.parametrize(
    "status, healthy_val, unhealthy_val, svc_status",
    [
        pytest.param(
            health_pb2.HealthCheckResponse.SERVING,
            1.0,
            0.0,
            AgentCheck.OK,
            id="serving",
        ),
        pytest.param(
            health_pb2.HealthCheckResponse.NOT_SERVING,
            0.0,
            1.0,
            AgentCheck.CRITICAL,
            id="not-serving",
        ),
    ],
)
def test_tags_do_not_leak_across_runs(dd_run_check, aggregator, status, healthy_val, unhealthy_val, svc_status):
    instance = {
        "grpc_server_address": "localhost:50051",
        "grpc_server_service": "grpc.test",
        "tags": ["tag_key1:value1", "tag_key2:value2"],
    }
    grpc_server = create_insecure_grpc_server(status)
    grpc_server.start()

    expected_tags = [
        "grpc_server_service:grpc.test",
        "grpc_server_address:localhost:50051",
        "status_code:OK",
        "tag_key1:value1",
        "tag_key2:value2",
    ]

    try:
        check = GrpcCheck("grpc_check", {}, [instance])
        for _ in range(5):
            dd_run_check(check)
            aggregator.assert_metric(
                "grpc_check.healthy",
                value=healthy_val,
                tags=expected_tags,
                hostname="",
                flush_first_value=False,
                metric_type=aggregator.GAUGE,
            )
            aggregator.assert_metric(
                "grpc_check.unhealthy",
                value=unhealthy_val,
                tags=expected_tags,
                hostname="",
                flush_first_value=False,
                metric_type=aggregator.GAUGE,
            )
            aggregator.assert_service_check(
                "grpc.healthy",
                status=svc_status,
                tags=expected_tags,
                count=1,
                hostname="",
                message="",
            )
            aggregator.assert_all_metrics_covered()
            aggregator.reset()
    finally:
        grpc_server.stop(None)


def test_instance_config_tags_not_mutated(dd_run_check, aggregator):
    user_tags = ["a:1", "b:2"]
    instance = {
        "grpc_server_address": "localhost:50051",
        "grpc_server_service": "grpc.test",
        "tags": user_tags,
    }
    grpc_server = create_insecure_grpc_server()
    grpc_server.start()

    expected_tags = [
        "grpc_server_service:grpc.test",
        "grpc_server_address:localhost:50051",
        "status_code:OK",
        "a:1",
        "b:2",
    ]

    try:
        check = GrpcCheck("grpc_check", {}, [instance])
        for _ in range(2):
            dd_run_check(check)
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
            aggregator.reset()
        assert instance["tags"] == ["a:1", "b:2"]
        assert instance["tags"] is user_tags
    finally:
        grpc_server.stop(None)


@pytest.mark.parametrize(
    "instance, server_factory, patch_target, wraps_target",
    [
        pytest.param(
            {
                "grpc_server_address": "localhost:50051",
                "grpc_server_service": "grpc.test",
                "tags": ["tag_key1:value1"],
            },
            create_insecure_grpc_server,
            "datadog_checks.grpc_check.check.grpc.insecure_channel",
            grpc.insecure_channel,
            id="insecure",
        ),
        pytest.param(
            {
                "grpc_server_address": "localhost:50052",
                "grpc_server_service": "grpc.test",
                "tags": ["tag_key1:value1"],
                "ca_cert": "tests/fixtures/ca.pem",
                "client_cert": "tests/fixtures/client.pem",
                "client_key": "tests/fixtures/client-key.pem",
            },
            create_secure_grpc_server,
            "datadog_checks.grpc_check.check.grpc.secure_channel",
            grpc.secure_channel,
            id="secure",
        ),
    ],
)
def test_channel_reused_across_runs(dd_run_check, aggregator, instance, server_factory, patch_target, wraps_target):
    grpc_server = server_factory()
    grpc_server.start()

    expected_tags = [
        "grpc_server_service:grpc.test",
        f"grpc_server_address:{instance['grpc_server_address']}",
        "status_code:OK",
        "tag_key1:value1",
    ]

    try:
        check = GrpcCheck("grpc_check", {}, [instance])
        with mock.patch(patch_target, wraps=wraps_target) as mock_channel:
            for _ in range(3):
                dd_run_check(check)
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
                aggregator.reset()
        assert mock_channel.call_count == 1
    finally:
        grpc_server.stop(None)


def test_cancel_creates_new_channel_on_next_run(dd_run_check, aggregator):
    instance = {
        "grpc_server_address": "localhost:50051",
        "grpc_server_service": "grpc.test",
        "tags": ["tag_key1:value1"],
    }
    grpc_server = create_insecure_grpc_server()
    grpc_server.start()

    expected_tags = [
        "grpc_server_service:grpc.test",
        "grpc_server_address:localhost:50051",
        "status_code:OK",
        "tag_key1:value1",
    ]

    try:
        check = GrpcCheck("grpc_check", {}, [instance])
        with mock.patch(
            "datadog_checks.grpc_check.check.grpc.insecure_channel", wraps=grpc.insecure_channel
        ) as mock_insecure_channel:
            dd_run_check(check)
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
            aggregator.reset()

            check.cancel()

            dd_run_check(check)
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

        assert mock_insecure_channel.call_count == 2
    finally:
        grpc_server.stop(None)


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
