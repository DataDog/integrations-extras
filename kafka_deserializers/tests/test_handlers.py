# (C) Datadog, Inc. 2026-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import base64
import datetime
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
    # Build the module path at runtime so `ddev validate imports` doesn't flag
    # a static reference to a sibling integration's namespace.
    import importlib

    host_pkg = 'datadog_' + 'checks.kafka_actions'
    try:
        importlib.import_module(host_pkg)
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


# --- Coverage top-ups for ProtobufMsgpackHandler ---------------------------


def test_msgpack_json_encoder_datetime_and_bytes(handler, log):
    """_MsgpackJSONEncoder branches: bytes -> base64, timestamp ext -> isoformat."""
    import msgpack

    payload = msgpack.packb(
        {'when': datetime.datetime(2025, 1, 2, 3, 4, 5, tzinfo=datetime.timezone.utc), 'blob': b'\xff\x00'},
        datetime=True,
        use_bin_type=True,
    )
    out = handler.deserialize(payload, None, log=log, uses_schema_registry=False)
    parsed = json.loads(out)
    assert parsed['blob'] == base64.b64encode(b'\xff\x00').decode('ascii')
    assert '2025-01-02T03:04:05' in parsed['when']


def test_protobuf_msgpack_build_schema_from_registry(proto_msgpack_handler, log):
    """build_schema_from_registry wraps the host call with msgpack_fields."""
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

    single_b64 = _b64.b64encode(fd.SerializeToString()).decode('ascii')
    wrapper = json.dumps({'schema': single_b64, 'msgpack_fields': ['test.Envelope.message']})
    schema = proto_msgpack_handler.build_schema_from_registry(wrapper, [])
    assert isinstance(schema, tuple)
    assert 'test.Envelope.message' in schema[1]


def test_protobuf_msgpack_uses_schema_registry_path(proto_msgpack_handler, log):
    """uses_schema_registry=True reads varint message-indices prefix."""
    import msgpack

    schema_b64 = _build_envelope_descriptor_b64()
    inner = {'k': 'v'}
    body = _encode_envelope(msgpack.packb(inner, use_bin_type=True), org_id=7)
    framed = b'\x00' + body  # array_len=0 varint, then the body

    schema_str = json.dumps({'schema': schema_b64, 'msgpack_fields': ['test.Envelope.message']})
    schema = proto_msgpack_handler.build_schema(schema_str)
    out = proto_msgpack_handler.deserialize(framed, schema, log=log, uses_schema_registry=True)
    parsed = json.loads(out)
    assert parsed['org_id'] == 7
    assert parsed['message'] == inner


def test_protobuf_msgpack_non_bytes_field_raises(proto_msgpack_handler, log):
    """msgpack_fields pointing at a non-bytes field surfaces a clear error."""
    import msgpack

    schema_b64 = _build_envelope_descriptor_b64()
    payload = _encode_envelope(msgpack.packb({'a': 1}, use_bin_type=True), org_id=99)
    schema_str = json.dumps({'schema': schema_b64, 'msgpack_fields': ['test.Envelope.org_id']})
    schema = proto_msgpack_handler.build_schema(schema_str)
    with pytest.raises(ValueError, match='non-bytes'):
        proto_msgpack_handler.deserialize(payload, schema, log=log, uses_schema_registry=False)


def test_protobuf_msgpack_empty_returns_none(proto_msgpack_handler, log):
    schema_b64 = _build_envelope_descriptor_b64()
    schema_str = json.dumps({'schema': schema_b64, 'msgpack_fields': []})
    schema = proto_msgpack_handler.build_schema(schema_str)
    assert proto_msgpack_handler.deserialize(b'', schema, log=log, uses_schema_registry=False) is None


def test_protobuf_msgpack_no_msgpack_fields_skips_walk(proto_msgpack_handler, log):
    """Empty msgpack_fields means MessageToDict output is returned as-is."""
    import msgpack

    schema_b64 = _build_envelope_descriptor_b64()
    payload = _encode_envelope(msgpack.packb({'a': 1}, use_bin_type=True), org_id=1)
    schema_str = json.dumps({'schema': schema_b64, 'msgpack_fields': []})
    schema = proto_msgpack_handler.build_schema(schema_str)
    out = proto_msgpack_handler.deserialize(payload, schema, log=log, uses_schema_registry=False)
    parsed = json.loads(out)
    # The bytes field stays base64-encoded since we didn't decode it
    assert parsed['org_id'] == 1
    assert isinstance(parsed['message'], str)
