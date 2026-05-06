import collections

import grpc
from grpc_health.v1 import health_pb2, health_pb2_grpc

from datadog_checks.base import AgentCheck, ConfigurationError


class _GenericClientInterceptor(
    grpc.UnaryUnaryClientInterceptor,
    grpc.UnaryStreamClientInterceptor,
    grpc.StreamUnaryClientInterceptor,
    grpc.StreamStreamClientInterceptor,
):
    def __init__(self, interceptor_function):
        self._fn = interceptor_function

    def intercept_unary_unary(self, continuation, client_call_details, request):
        new_details, new_request_iterator, postprocess = self._fn(client_call_details, iter((request,)), False, False)
        response = continuation(new_details, next(new_request_iterator))
        return postprocess(response) if postprocess else response

    def intercept_unary_stream(self, continuation, client_call_details, request):
        new_details, new_request_iterator, postprocess = self._fn(client_call_details, iter((request,)), False, True)
        response_it = continuation(new_details, next(new_request_iterator))
        return postprocess(response_it) if postprocess else response_it

    def intercept_stream_unary(self, continuation, client_call_details, request_iterator):
        new_details, new_request_iterator, postprocess = self._fn(client_call_details, request_iterator, True, False)
        response = continuation(new_details, new_request_iterator)
        return postprocess(response) if postprocess else response

    def intercept_stream_stream(self, continuation, client_call_details, request_iterator):
        new_details, new_request_iterator, postprocess = self._fn(client_call_details, request_iterator, True, True)
        response_it = continuation(new_details, new_request_iterator)
        return postprocess(response_it) if postprocess else response_it


def create_generic_client_interceptor(intercept_call):
    return _GenericClientInterceptor(intercept_call)


class _ClientCallDetails(
    collections.namedtuple("_ClientCallDetails", ("method", "timeout", "metadata", "credentials")),
    grpc.ClientCallDetails,
):
    pass


def header_adder_interceptor(header, value):
    def intercept_call(client_call_details, request_iterator, request_streaming, response_streaming):
        metadata = []
        if client_call_details.metadata is not None:
            metadata = list(client_call_details.metadata)
        metadata.append(
            (
                header,
                value,
            )
        )
        client_call_details = _ClientCallDetails(
            client_call_details.method,
            client_call_details.timeout,
            metadata,
            client_call_details.credentials,
        )
        return client_call_details, request_iterator, None

    return create_generic_client_interceptor(intercept_call)


class GrpcCheck(AgentCheck):
    def __init__(self, name, init_config, instances):
        super(GrpcCheck, self).__init__(name, init_config, instances)
        self.grpc_server_address = self.instance.get("grpc_server_address", "")
        self.grpc_server_service = self.instance.get("grpc_server_service", "")
        self.timeout = self.instance.get("timeout", 1000) / 1000
        self.rpc_header = self.instance.get("rpc_header", [])
        self.client_cert = self.instance.get("client_cert", "")
        self.client_key = self.instance.get("client_key", "")
        self.ca_cert = self.instance.get("ca_cert", "")
        self.secure_channel = self.instance.get("secure_channel", False)
        self._validate_configuration()
        self._base_tags = list(self.instance.get("tags", []))
        self._base_tags.append("grpc_server_address:{}".format(self.grpc_server_address))
        self._base_tags.append("grpc_server_service:{}".format(self.grpc_server_service))

        self._channel = None
        self._intercept_channel = None
        self._header_adder_interceptors = self._parse_rcp_headers(self.rpc_header)

    def cancel(self):
        if self._channel is not None:
            try:
                self._channel.close()
            except Exception as e:
                self.log.warning("failed to close gRPC channel: %s", e)
            finally:
                self._channel = None
                self._intercept_channel = None

    def _get_channel(self):
        if self._channel is None:
            self._channel = self._create_channel(self.instance)
        return self._channel

    def _get_intercept_channel(self):
        if self._intercept_channel is None:
            self._intercept_channel = grpc.intercept_channel(self._get_channel(), *self._header_adder_interceptors)
        return self._intercept_channel

    def _validate_configuration(self):
        if not self.grpc_server_address:
            raise ConfigurationError("grpc_server_address must be specified")
        if self.timeout <= 0:
            raise ConfigurationError("timeout must be greater than zero")
        _all = all([self.ca_cert != "", self.client_cert != "", self.client_key != ""])
        nothing = all([self.ca_cert == "", self.client_cert == "", self.client_key == ""])
        if (_all or nothing) is False:
            raise ConfigurationError("ca_cert, client_cert or client_key is missing")

    def _parse_rcp_headers(self, rpc_headers):
        header_adder_interceptors = []
        for rpc_header in rpc_headers:
            header_value = rpc_header.split(":")
            if len(header_value) <= 1:
                self.log.debug("'%s' was invalid rpc_header format", rpc_header)
                continue
            header_adder_interceptors.append(header_adder_interceptor(header_value[0], header_value[1].strip()))
        return header_adder_interceptors

    def _create_channel(self, instance):
        if self.client_cert != "" and self.client_key != "" and self.ca_cert != "":
            cert = open(self.client_cert, "rb").read()
            key = open(self.client_key, "rb").read()
            ca = open(self.ca_cert, "rb").read()
            credentials = grpc.ssl_channel_credentials(ca, key, cert)
            self.log.debug(
                "creating a secure channel with client_cert=%s, client_key=%s, ca_cert=%s",
                cert,
                key,
                ca,
            )
            return grpc.secure_channel(self.grpc_server_address, credentials)
        if self.secure_channel:
            grpc_server = self.grpc_server_address.split(":")[0]
            return grpc.secure_channel(
                self.grpc_server_address,
                grpc.ssl_channel_credentials(),
                options=(('grpc.ssl_target_name_override', grpc_server), ('grpc.default_authority', grpc_server)),
            )
        self.log.debug("creating an insecure channel")
        return grpc.insecure_channel(self.grpc_server_address)

    def _send_healthy(self, tags):
        self.gauge("grpc_check.healthy", 1, tags=tags)
        self.gauge("grpc_check.unhealthy", 0, tags=tags)
        self.service_check("grpc.healthy", AgentCheck.OK, tags=tags)

    def _send_unhealthy(self, tags):
        self.gauge("grpc_check.healthy", 0, tags=tags)
        self.gauge("grpc_check.unhealthy", 1, tags=tags)
        self.service_check("grpc.healthy", AgentCheck.CRITICAL, tags=tags)

    def check(self, instance):
        self.log.debug(
            "grpc_server_address=%s, grpc_server_service=%s: trying to connect",
            self.grpc_server_address,
            self.grpc_server_service,
        )
        status_code = grpc.StatusCode.UNKNOWN
        response = None
        try:
            intercept_channel = self._get_intercept_channel()
            health_stub = health_pb2_grpc.HealthStub(intercept_channel)
            request = health_pb2.HealthCheckRequest(service=self.grpc_server_service)
            response = health_stub.Check(request, timeout=self.timeout)
        except grpc.RpcError as e:
            status_code = e.code()
            details = e.details()
            if status_code == grpc.StatusCode.DEADLINE_EXCEEDED:
                self.log.error(
                    "grpc_server_address=%s, grpc_server_service=%s: timeout after %s seconds",
                    self.grpc_server_address,
                    self.grpc_server_service,
                    str(self.timeout),
                )
            if status_code == grpc.StatusCode.NOT_FOUND:
                self.log.error(
                    "grpc_server_service '%s' was not found: %s",
                    self.grpc_server_service,
                    details,
                )
            else:
                self.log.error(
                    "grpc_server_address=%s, grpc_server_service=%s: request failure: %s",
                    self.grpc_server_address,
                    self.grpc_server_service,
                    details,
                )
        except Exception as e:
            self.log.exception("failed to check: %s", e)

        if response is None:
            tags = list(self._base_tags)
            tags.append("status_code:{}".format(status_code.name))
            self._send_unhealthy(tags)
            return

        tags = list(self._base_tags)
        tags.append("status_code:{}".format(grpc.StatusCode.OK.name))
        if response.status == health_pb2.HealthCheckResponse.SERVING:
            self.log.debug(
                "grpc_server_address=%s, grpc_server_service=%s: healthy",
                self.grpc_server_address,
                self.grpc_server_service,
            )
            self._send_healthy(tags)
        elif response.status == health_pb2.HealthCheckResponse.NOT_SERVING:
            self.log.warning(
                "grpc_server_address=%s, grpc_server_service=%s: unhealthy",
                self.grpc_server_address,
                self.grpc_server_service,
            )
            self._send_unhealthy(tags)
        else:
            self.log.warning(
                "grpc_server_address=%s, grpc_server_service=%s: health check response was unknown",
                self.grpc_server_address,
                self.grpc_server_service,
            )
            self._send_unhealthy(tags)
