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
