# (C) Datadog, Inc. 2026-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
"""Stub the kafka_actions host package so plugin tests run without it installed.

In production the kafka_actions wheel is co-installed and provides the real
FormatHandler / CompressionCodec base classes plus the protobuf decode helpers.
integrations-extras CI cannot resolve datadog-kafka-actions from PyPI, so we
register lightweight stand-ins in ``sys.modules`` before _compat.py runs its
``importlib.import_module`` calls. The stubs implement just enough surface to
exercise ProtobufMsgpackHandler end-to-end.
"""

from __future__ import annotations

import base64
import sys
import types
from abc import ABC, abstractmethod

_HOST_PKG = 'datadog_' + 'checks.kafka_actions'


def _install_host_stub() -> None:
    if _HOST_PKG in sys.modules:
        return

    from google.protobuf import descriptor_pb2, descriptor_pool, message_factory

    pkg = types.ModuleType(_HOST_PKG)
    pkg.__path__ = []  # mark as package

    formats_pkg = types.ModuleType(f'{_HOST_PKG}.formats')
    formats_pkg.__path__ = []

    formats_base = types.ModuleType(f'{_HOST_PKG}.formats.base')

    class FormatHandler(ABC):
        name: str = ''

        def build_schema(self, schema_str):
            return None

        def build_schema_from_registry(self, schema_str, dep_schemas):
            return self.build_schema(schema_str)

        @abstractmethod
        def deserialize(self, message, schema, *, log, uses_schema_registry):
            raise NotImplementedError

    formats_base.FormatHandler = FormatHandler

    compression_pkg = types.ModuleType(f'{_HOST_PKG}.compression')
    compression_pkg.__path__ = []

    compression_base = types.ModuleType(f'{_HOST_PKG}.compression.base')

    class CompressionCodec(ABC):
        name: str = ''

        @abstractmethod
        def decompress(self, data):
            raise NotImplementedError

    compression_base.CompressionCodec = CompressionCodec

    def _preload_well_known_types(pool):
        from google.protobuf import any_pb2, duration_pb2, empty_pb2, struct_pb2, timestamp_pb2, wrappers_pb2

        for module in (any_pb2, duration_pb2, empty_pb2, struct_pb2, timestamp_pb2, wrappers_pb2):
            name = module.DESCRIPTOR.name
            try:
                pool.FindFileByName(name)
                continue
            except KeyError:
                pass
            fd_proto = descriptor_pb2.FileDescriptorProto()
            module.DESCRIPTOR.CopyToProto(fd_proto)
            pool.Add(fd_proto)

    def _read_varint(data):
        shift = 0
        result = 0
        bytes_read = 0
        for byte in data:
            bytes_read += 1
            result |= (byte & 0x7F) << shift
            if (byte & 0x80) == 0:
                return result, bytes_read
            shift += 7
        raise ValueError("Incomplete varint")

    def read_protobuf_message_indices(payload):
        array_len, n = _read_varint(payload)
        payload = payload[n:]
        indices = []
        for _ in range(array_len):
            idx, n = _read_varint(payload)
            indices.append(idx)
            payload = payload[n:]
        return indices, payload

    def get_protobuf_message_class(schema_info, indices):
        pool, descriptor_set = schema_info
        file_descriptor = descriptor_set.file[0]
        proto = file_descriptor.message_type[indices[0]]
        package = file_descriptor.package
        parts = [proto.name]
        current = proto
        for i in indices[1:]:
            current = current.nested_type[i]
            parts.append(current.name)
        full = f"{package}.{'.'.join(parts)}" if package else '.'.join(parts)
        return message_factory.GetMessageClass(pool.FindMessageTypeByName(full))

    message_deserializer = types.ModuleType(f'{_HOST_PKG}.message_deserializer')
    message_deserializer.read_protobuf_message_indices = read_protobuf_message_indices
    message_deserializer.get_protobuf_message_class = get_protobuf_message_class

    formats_builtins = types.ModuleType(f'{_HOST_PKG}.formats.builtins')

    class ProtobufHandler(FormatHandler):
        name = 'protobuf'

        def build_schema(self, schema_str):
            schema_bytes = base64.b64decode(schema_str)
            descriptor_set = descriptor_pb2.FileDescriptorSet()
            descriptor_set.ParseFromString(schema_bytes)
            pool = descriptor_pool.DescriptorPool()
            _preload_well_known_types(pool)
            for fd_proto in descriptor_set.file:
                pool.Add(fd_proto)
            return (pool, descriptor_set)

        def build_schema_from_registry(self, schema_str, dep_schemas):
            pool = descriptor_pool.DescriptorPool()
            _preload_well_known_types(pool)
            descriptor_set = descriptor_pb2.FileDescriptorSet()
            for dep_name, dep_b64 in dep_schemas:
                try:
                    pool.FindFileByName(dep_name)
                    continue
                except KeyError:
                    pass
                dep_proto = descriptor_pb2.FileDescriptorProto()
                dep_proto.ParseFromString(base64.b64decode(dep_b64))
                dep_proto.name = dep_name
                pool.Add(dep_proto)
            fd_proto = descriptor_pb2.FileDescriptorProto()
            fd_proto.ParseFromString(base64.b64decode(schema_str))
            descriptor_set.file.append(fd_proto)
            pool.Add(fd_proto)
            return (pool, descriptor_set)

        def deserialize(self, message, schema, *, log, uses_schema_registry):
            raise NotImplementedError

    formats_builtins.ProtobufHandler = ProtobufHandler

    sys.modules[_HOST_PKG] = pkg
    sys.modules[f'{_HOST_PKG}.formats'] = formats_pkg
    sys.modules[f'{_HOST_PKG}.formats.base'] = formats_base
    sys.modules[f'{_HOST_PKG}.formats.builtins'] = formats_builtins
    sys.modules[f'{_HOST_PKG}.compression'] = compression_pkg
    sys.modules[f'{_HOST_PKG}.compression.base'] = compression_base
    sys.modules[f'{_HOST_PKG}.message_deserializer'] = message_deserializer


_install_host_stub()
