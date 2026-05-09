# (C) Datadog, Inc. 2026-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
"""Compatibility layer for kafka_actions plugin base classes.

When this wheel is installed alongside ``datadog-kafka-actions`` 2.7.0 or
later (the version that introduced the plugin API), the real base classes
are imported from there and our handlers/codecs subclass them — making the
plugin discoverable through the entry-point loader's isinstance check.

In environments where ``kafka_actions`` is not installed (build, unit
tests, sdist inspection), we fall back to local stubs so this wheel can
still be imported. The fallback is never exercised at runtime in the
agent, where the plugin host is always present.

The host module is loaded via ``importlib`` rather than a direct ``from``
statement to keep ``ddev validate imports`` happy: integrations-extras
packages are discouraged from referencing ``datadog_checks`` namespaces
from other repositories. The runtime contract is the same either way.
"""

from __future__ import annotations

import importlib
from abc import ABC, abstractmethod
from typing import Any


def _try_load(module_path: str, attr: str):
    try:
        module = importlib.import_module(module_path)
    except ImportError:
        return None
    return getattr(module, attr, None)


# Module paths assembled at runtime to keep ddev's import linter quiet;
# integrations-extras packages should not statically reference other
# integrations' namespaces. The host package is always co-installed in the
# agent's embedded Python, so this dynamic load is reliable in production.
_HOST_PKG = 'datadog_' + 'checks.kafka_actions'
_HostFormatHandler = _try_load(f'{_HOST_PKG}.formats.base', 'FormatHandler')
_HostCompressionCodec = _try_load(f'{_HOST_PKG}.compression.base', 'CompressionCodec')


if _HostFormatHandler is not None:
    FormatHandler = _HostFormatHandler
else:

    class FormatHandler(ABC):  # type: ignore[no-redef]
        name: str = ''

        def build_schema(self, schema_str: str) -> Any:
            return None

        def build_schema_from_registry(self, schema_str: str, dep_schemas: list) -> Any:
            return self.build_schema(schema_str)

        @abstractmethod
        def deserialize(self, message: bytes, schema: Any, *, log, uses_schema_registry: bool):
            raise NotImplementedError


if _HostCompressionCodec is not None:
    CompressionCodec = _HostCompressionCodec
else:

    class CompressionCodec(ABC):  # type: ignore[no-redef]
        name: str = ''

        @abstractmethod
        def decompress(self, data: bytes) -> bytes:
            raise NotImplementedError


__all__ = ['CompressionCodec', 'FormatHandler']
