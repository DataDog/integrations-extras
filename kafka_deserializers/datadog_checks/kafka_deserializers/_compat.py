# (C) Datadog, Inc. 2026-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
"""Compatibility layer for kafka_actions plugin base classes.

When this wheel is installed alongside ``datadog-kafka-actions>=2.7.0``
(the version that introduced the plugin API), the real base classes are
imported from there and our handlers/codecs subclass them — making the
plugin discoverable through the entry-point loader's isinstance check.

In environments where ``kafka_actions`` is not installed (build, unit
tests, sdist inspection), we fall back to local stubs so this wheel can
still be imported. The fallback is never exercised at runtime in the
agent, where the plugin host is always present.
"""

from __future__ import annotations

try:
    from datadog_checks.kafka_actions.compression.base import CompressionCodec  # type: ignore[import-not-found]
    from datadog_checks.kafka_actions.formats.base import FormatHandler  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover — used only when kafka_actions is absent
    from abc import ABC, abstractmethod
    from typing import Any

    class FormatHandler(ABC):  # type: ignore[no-redef]
        name: str = ''

        def build_schema(self, schema_str: str) -> Any:
            return None

        def build_schema_from_registry(self, schema_str: str, dep_schemas: list) -> Any:
            return self.build_schema(schema_str)

        @abstractmethod
        def deserialize(self, message: bytes, schema: Any, *, log, uses_schema_registry: bool):
            raise NotImplementedError

    class CompressionCodec(ABC):  # type: ignore[no-redef]
        name: str = ''

        @abstractmethod
        def decompress(self, data: bytes) -> bytes:
            raise NotImplementedError


__all__ = ['CompressionCodec', 'FormatHandler']
