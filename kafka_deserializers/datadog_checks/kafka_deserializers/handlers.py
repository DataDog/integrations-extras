# (C) Datadog, Inc. 2026-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
"""MessagePack format handler.

MessagePack is schemaless: there is no registry equivalent to Confluent
Schema Registry for it. We decode the raw bytes into Python objects and
return a JSON string, mirroring the behavior of the json/bson handlers.
"""

from __future__ import annotations

import base64
import datetime
import json

from ._compat import (
    FormatHandler,
    HostProtobufHandler,
    host_get_protobuf_message_class,
    host_read_protobuf_message_indices,
)


class _MsgpackJSONEncoder(json.JSONEncoder):
    """JSON encoder for types msgpack may emit (bytes, datetime via timestamp ext type)."""

    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()
        if isinstance(obj, bytes):
            return base64.b64encode(obj).decode('ascii')
        return super().default(obj)


class MsgpackHandler(FormatHandler):
    name = 'msgpack'

    def deserialize(self, message, schema, *, log, uses_schema_registry):
        if not message:
            return None
        import msgpack

        try:
            decoded = msgpack.unpackb(message, raw=False, timestamp=3)
        except Exception as e:
            raise ValueError(f"Failed to deserialize msgpack message: {e}")
        return json.dumps(decoded, cls=_MsgpackJSONEncoder)


class ProtobufMsgpackHandler(FormatHandler):
    """Protobuf envelope where one or more ``bytes`` fields carry msgpack payloads.

    Same shape as dd-go ``RawPipelineStats``: a protobuf message with a
    ``bytes`` field (``message`` by default) whose contents are msgpack.
    Nested messages are supported — any field on any descendant message can be
    flagged as msgpack.

    The ``schema_str`` is a JSON wrapper:

        {
          "schema": "<base64 FileDescriptorSet>",
          "msgpack_fields": ["pkg.OuterMsg.payload", "pkg.InnerMsg.details"]
        }

    Each entry in ``msgpack_fields`` is the fully-qualified protobuf path of a
    ``bytes`` field: ``<package>.<MessageType>.<field_name>``. When the message
    type has no package, omit the leading dot.
    """

    name = 'protobuf_msgpack'

    def build_schema(self, schema_str):
        if HostProtobufHandler is None:
            raise RuntimeError("datadog-kafka-actions host package is required for protobuf_msgpack")
        wrapper = json.loads(schema_str)
        proto_schema = HostProtobufHandler().build_schema(wrapper['schema'])
        return (proto_schema, set(wrapper.get('msgpack_fields') or []))

    def build_schema_from_registry(self, schema_str, dep_schemas):
        if HostProtobufHandler is None:
            raise RuntimeError("datadog-kafka-actions host package is required for protobuf_msgpack")
        wrapper = json.loads(schema_str)
        proto_schema = HostProtobufHandler().build_schema_from_registry(wrapper['schema'], dep_schemas)
        return (proto_schema, set(wrapper.get('msgpack_fields') or []))

    def deserialize(self, message, schema, *, log, uses_schema_registry):
        if host_get_protobuf_message_class is None or host_read_protobuf_message_indices is None:
            raise RuntimeError("datadog-kafka-actions host package is required for protobuf_msgpack")
        from google.protobuf.json_format import MessageToDict

        if not message:
            return None
        proto_schema, msgpack_paths = schema

        if uses_schema_registry:
            message_indices, message = host_read_protobuf_message_indices(message)
            if not message_indices:
                message_indices = [0]
        else:
            message_indices = [0]

        try:
            message_class = host_get_protobuf_message_class(proto_schema, message_indices)
            instance = message_class()
            consumed = instance.ParseFromString(message)
            if consumed != len(message):
                raise ValueError(
                    f"Not all bytes were consumed during Protobuf decoding! "
                    f"Read {consumed} bytes, but message has {len(message)} bytes."
                )

            result = MessageToDict(instance, preserving_proto_field_name=True)
            if msgpack_paths:
                self._apply_msgpack_fields(instance, result, msgpack_paths)
            return json.dumps(result, cls=_MsgpackJSONEncoder)
        except Exception as e:
            raise ValueError(f"Failed to deserialize protobuf_msgpack message: {e}")

    @staticmethod
    def _apply_msgpack_fields(instance, result_dict, msgpack_paths):
        """Walk ``instance`` + ``result_dict`` in lockstep; replace any field whose
        full path is in ``msgpack_paths`` with its msgpack-decoded value.
        """
        import msgpack
        from google.protobuf.descriptor import FieldDescriptor

        def walk(msg, out):
            msg_full = msg.DESCRIPTOR.full_name
            for field_desc, value in msg.ListFields():
                full_path = f"{msg_full}.{field_desc.name}"
                key = field_desc.name
                is_repeated = field_desc.is_repeated
                if full_path in msgpack_paths:
                    if field_desc.type != FieldDescriptor.TYPE_BYTES:
                        raise ValueError(f"msgpack_fields path '{full_path}' refers to a non-bytes field")
                    if is_repeated:
                        out[key] = [msgpack.unpackb(bytes(b), raw=False, timestamp=3) for b in value]
                    else:
                        out[key] = msgpack.unpackb(bytes(value), raw=False, timestamp=3)
                    continue
                if field_desc.message_type is None:
                    continue
                sub_out = out.get(key)
                if sub_out is None:
                    continue
                if is_repeated:
                    for sub_msg, sub_d in zip(value, sub_out):
                        walk(sub_msg, sub_d)
                else:
                    walk(value, sub_out)

        walk(instance, result_dict)
