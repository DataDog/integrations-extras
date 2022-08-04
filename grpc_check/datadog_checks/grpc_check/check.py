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
        new_details, new_request_iterator, postprocess = self._fn(
            client_call_details, iter((request,)), False, False)
        response = continuation(new_details, next(new_request_iterator))
        return postprocess(response) if postprocess else response

    def intercept_unary_stream(self, continuation, client_call_details, request):
        new_details, new_request_iterator, postprocess = self._fn(
            client_call_details, iter((request,)), False, True)
        response_it = continuation(new_details, next(new_request_iterator))
        return postprocess(response_it) if postprocess else response_it

    def intercept_stream_unary(self, continuation, client_call_details, request_iterator):
        new_details, new_request_iterator, postprocess = self._fn(
            client_call_details, request_iterator, True, False)
        response = continuation(new_details, new_request_iterator)
        return postprocess(response) if postprocess else response

    def intercept_stream_stream(self, continuation, client_call_details, request_iterator):
        new_details, new_request_iterator, postprocess = self._fn(
            client_call_details, request_iterator, True, True)
        response_it = continuation(new_details, new_request_iterator)
        return postprocess(response_it) if postprocess else response_it


def create_generic_client_interceptor(intercept_call):
    return _GenericClientInterceptor(intercept_call)


class _ClientCallDetails(
    collections.namedtuple("_ClientCallDetails",
                           ("method", "timeout", "metadata", "credentials")),
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
        self.timeout = self.instance.get("timeout", 0) / 1000
        self.rpc_header = self.instance.get("rpc_header", [])
        self.client_cert = self.instance.get("client_cert", "")
        self.client_key = self.instance.get("client_key", "")
        self.ca_cert = self.instance.get("ca_cert", "")
        self._validate_configuration()
        self.tags = self.instance.get("tags", [])
        self.tags.append("grpc_server_address:{}".format(
            self.grpc_server_address))
        self.tags.append("grpc_server_service:{}".format(
            self.grpc_server_service))

    def _validate_configuration(self):
        if not self.grpc_server_address:
            raise ConfigurationError("grpc_server_address must be specified")
        if self.timeout <= 0:
            raise ConfigurationError("timeout must be greater than zero")
        _all = all([self.ca_cert != "", self.client_cert !=
                   "", self.client_key != ""])
        nothing = all([self.ca_cert == "", self.client_cert ==
                      "", self.client_key == ""])
        if (_all or nothing) is False:
            raise ConfigurationError(
                "ca_cert, client_cert or client_key is missing")

    def _parse_rcp_headers(self, rpc_headers):
        header_adder_interceptors = []
        for rpc_header in rpc_headers:
            header_value = rpc_header.split(":")
            if len(header_value) <= 1:
                self.log.debug(
                    "'%s' was invalid rpc_header format", rpc_header)
                continue
            header_adder_interceptors.append(header_adder_interceptor(
                header_value[0], header_value[1].strip()))
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
            return grpc.secure_channel(instance.get("grpc_server_address"), credentials)

        self.log.debug("creating an insecure channel")
        return grpc.insecure_channel(instance.get("grpc_server_address"))

    def _send_healthy(self):
        self.gauge("grpc_check.healthy", 1, tags=self.tags)
        self.gauge("grpc_check.unhealthy", 0, tags=self.tags)
        self.service_check("grpc.healthy", AgentCheck.OK, tags=self.tags)

    def _send_unhealthy(self):
        self.gauge("grpc_check.healthy", 0, tags=self.tags)
        self.gauge("grpc_check.unhealthy", 1, tags=self.tags)
        self.service_check("grpc.healthy", AgentCheck.CRITICAL, tags=self.tags)

    def check(self, instance):
        self.log.debug(
            "grpc_server_address=%s, grpc_server_service=%s: trying to connect",
            self.grpc_server_address,
            self.grpc_server_service,
        )
        status_code = grpc.StatusCode.UNKNOWN
        response = None
        try:
            with self._create_channel(instance) as channel:
                header_adder_interceptors = self._parse_rcp_headers(
                    self.rpc_header)
                intercept_channel = grpc.intercept_channel(
                    channel, *header_adder_interceptors)
                health_stub = health_pb2_grpc.HealthStub(intercept_channel)
                request = health_pb2.HealthCheckRequest(
                    service=self.grpc_server_service)
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
            self.log.error("failed to check: %s", str(e))

        if not response:
            self.tags.append("status_code:{}".format(status_code.name))
            self._send_unhealthy()
            return

        self.tags.append("status_code:{}".format(grpc.StatusCode.OK.name))
        if response.status == health_pb2.HealthCheckResponse.SERVING:
            self.log.info(
                "grpc_server_address=%s, grpc_server_service=%s: healthy",
                self.grpc_server_address,
                self.grpc_server_service,
            )
            self._send_healthy()
        elif response.status == health_pb2.HealthCheckResponse.NOT_SERVING:
            self.log.warning(
                "grpc_server_address=%s, grpc_server_service=%s: unhealthy",
                self.grpc_server_address,
                self.grpc_server_service,
            )
            self._send_unhealthy()
        else:
            self.log.warning(
                "grpc_server_address=%s, grpc_server_service=%s: health check response was unknown",
                self.grpc_server_address,
                self.grpc_server_service,
            )
            self._send_unhealthy()
