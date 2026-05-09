# (C) Datadog, Inc. 2025-present
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

from datadog_checks.kafka_actions.formats.base import FormatHandler


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
