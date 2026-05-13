# (C) Datadog, Inc. 2026-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import json
import logging

import msgpack
import pytest
from datadog_checks.kafka_deserializers.handlers import MsgpackHandler


@pytest.fixture
def handler():
    return MsgpackHandler()


@pytest.fixture
def log():
    return logging.getLogger('test')


def test_msgpack_simple_dict(handler, log):
    payload = msgpack.packb({'a': 1, 'b': 'two', 'c': [1, 2, 3]})
    out = handler.deserialize(payload, None, log=log, uses_schema_registry=False)
    assert json.loads(out) == {'a': 1, 'b': 'two', 'c': [1, 2, 3]}


def test_msgpack_nested(handler, log):
    payload = msgpack.packb({'outer': {'inner': [None, True, False]}})
    out = handler.deserialize(payload, None, log=log, uses_schema_registry=False)
    assert json.loads(out) == {'outer': {'inner': [None, True, False]}}


def test_msgpack_bytes_field_base64_encoded(handler, log):
    payload = msgpack.packb({'data': b'\x00\x01\x02'})
    out = handler.deserialize(payload, None, log=log, uses_schema_registry=False)
    parsed = json.loads(out)
    assert parsed['data'] == 'AAEC'  # base64 of \x00\x01\x02


def test_msgpack_empty_returns_none(handler, log):
    assert handler.deserialize(b'', None, log=log, uses_schema_registry=False) is None


def test_msgpack_invalid_raises(handler, log):
    with pytest.raises(ValueError, match="Failed to deserialize msgpack"):
        handler.deserialize(b'\xff\xff\xff\xff', None, log=log, uses_schema_registry=False)


# --- ProtobufMsgpackHandler ---------------------------------------------------


def _build_envelope_descriptor_b64():
    """Hand-build a FileDescriptorSet for Envelope { bytes message=1; int32 org_id=2; }."""
    import base64 as _b64

    from google.protobuf import descriptor_pb2

    fd = descriptor_pb2.FileDescriptorProto()
    fd.name = 'envelope.proto'
    fd.syntax = 'proto3'
    fd.package = 'test'
    msg = fd.message_type.add()
    msg.name = 'Envelope'
    f = msg.field.add()
    f.name = 'message'
    f.number = 1
    f.type = descriptor_pb2.FieldDescriptorProto.TYPE_BYTES
    f.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    f = msg.field.add()
    f.name = 'org_id'
    f.number = 2
    f.type = descriptor_pb2.FieldDescriptorProto.TYPE_INT32
    f.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL

    fds = descriptor_pb2.FileDescriptorSet()
    fds.file.append(fd)
    return _b64.b64encode(fds.SerializeToString()).decode('ascii')


def _encode_envelope(inner_bytes: bytes, org_id: int) -> bytes:
    out = bytearray()
    out.append((1 << 3) | 2)  # field 1, length-delimited
    out.append(len(inner_bytes))
    out += inner_bytes
    out.append((2 << 3) | 0)  # field 2, varint
    out.append(org_id & 0x7F)
    return bytes(out)


def _host_available() -> bool:
    try:
        import datadog_checks.kafka_actions  # noqa: F401
    except ImportError:
        return False
    return True


_skip_without_host = pytest.mark.skipif(
    not _host_available(),
    reason='ProtobufMsgpackHandler requires the kafka_actions host package; '
    'skip when running extras tests in isolation.',
)


@pytest.fixture
def proto_msgpack_handler():
    from datadog_checks.kafka_deserializers.handlers import ProtobufMsgpackHandler

    return ProtobufMsgpackHandler()


@_skip_without_host
def test_protobuf_msgpack_decodes_inner_field(proto_msgpack_handler, log):
    import msgpack

    schema_b64 = _build_envelope_descriptor_b64()
    inner = {'service': 'orders', 'env': 'prod', 'count': 3}
    inner_bytes = msgpack.packb(inner, use_bin_type=True)
    payload = _encode_envelope(inner_bytes, org_id=42)

    schema_str = json.dumps({'schema': schema_b64, 'msgpack_fields': ['test.Envelope.message']})
    schema = proto_msgpack_handler.build_schema(schema_str)

    out = proto_msgpack_handler.deserialize(payload, schema, log=log, uses_schema_registry=False)
    parsed = json.loads(out)
    assert parsed['org_id'] == 42
    assert parsed['message'] == inner


@_skip_without_host
def test_protobuf_msgpack_missing_field_is_silently_ok(proto_msgpack_handler, log):
    schema_b64 = _build_envelope_descriptor_b64()
    payload = _encode_envelope(b'', org_id=1)  # empty bytes field
    schema_str = json.dumps({'schema': schema_b64, 'msgpack_fields': ['test.Envelope.message']})
    schema = proto_msgpack_handler.build_schema(schema_str)

    out = proto_msgpack_handler.deserialize(payload, schema, log=log, uses_schema_registry=False)
    parsed = json.loads(out)
    assert parsed['org_id'] == 1
    assert 'message' not in parsed


@_skip_without_host
def test_protobuf_msgpack_invalid_inner_raises(proto_msgpack_handler, log):
    schema_b64 = _build_envelope_descriptor_b64()
    payload = _encode_envelope(b'\xff\xff\xff', org_id=1)  # not valid msgpack
    schema_str = json.dumps({'schema': schema_b64, 'msgpack_fields': ['test.Envelope.message']})
    schema = proto_msgpack_handler.build_schema(schema_str)

    with pytest.raises(ValueError, match="Failed to deserialize protobuf_msgpack"):
        proto_msgpack_handler.deserialize(payload, schema, log=log, uses_schema_registry=False)


def _build_nested_descriptor_b64():
    """test.Outer { bytes payload=1; test.Inner inner=2; } / test.Inner { bytes details=1; }"""
    import base64 as _b64

    from google.protobuf import descriptor_pb2

    fd = descriptor_pb2.FileDescriptorProto()
    fd.name = 'nested.proto'
    fd.syntax = 'proto3'
    fd.package = 'test'

    outer = fd.message_type.add()
    outer.name = 'Outer'
    f = outer.field.add()
    f.name = 'payload'
    f.number = 1
    f.type = descriptor_pb2.FieldDescriptorProto.TYPE_BYTES
    f.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    f = outer.field.add()
    f.name = 'inner'
    f.number = 2
    f.type = descriptor_pb2.FieldDescriptorProto.TYPE_MESSAGE
    f.type_name = '.test.Inner'
    f.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL

    inner = fd.message_type.add()
    inner.name = 'Inner'
    f = inner.field.add()
    f.name = 'details'
    f.number = 1
    f.type = descriptor_pb2.FieldDescriptorProto.TYPE_BYTES
    f.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL

    fds = descriptor_pb2.FileDescriptorSet()
    fds.file.append(fd)
    return _b64.b64encode(fds.SerializeToString()).decode('ascii')


def _encode_nested(payload_bytes: bytes, details_bytes: bytes) -> bytes:
    # Outer { payload=payload_bytes, inner=Inner{details=details_bytes} }
    inner_msg = bytearray()
    inner_msg.append((1 << 3) | 2)
    inner_msg.append(len(details_bytes))
    inner_msg += details_bytes

    out = bytearray()
    out.append((1 << 3) | 2)
    out.append(len(payload_bytes))
    out += payload_bytes
    out.append((2 << 3) | 2)
    out.append(len(inner_msg))
    out += inner_msg
    return bytes(out)


@_skip_without_host
def test_protobuf_msgpack_nested_fields_decoded(proto_msgpack_handler, log):
    """msgpack_fields targets a field on the outer message AND on a nested submessage."""
    import msgpack

    schema_b64 = _build_nested_descriptor_b64()
    payload_inner = {'service': 'orders'}
    details_inner = {'count': 7, 'tags': ['a', 'b']}
    raw = _encode_nested(
        msgpack.packb(payload_inner, use_bin_type=True),
        msgpack.packb(details_inner, use_bin_type=True),
    )
    schema_str = json.dumps(
        {
            'schema': schema_b64,
            'msgpack_fields': ['test.Outer.payload', 'test.Inner.details'],
        }
    )
    schema = proto_msgpack_handler.build_schema(schema_str)

    out = proto_msgpack_handler.deserialize(raw, schema, log=log, uses_schema_registry=False)
    parsed = json.loads(out)
    assert parsed['payload'] == payload_inner
    assert parsed['inner']['details'] == details_inner
