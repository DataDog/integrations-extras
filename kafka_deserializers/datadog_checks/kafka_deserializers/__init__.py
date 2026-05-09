# (C) Datadog, Inc. 2026-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
"""Plugin pack for the kafka_actions check.

This wheel does not register a runtime check. It contributes additional
format handlers and compression codecs to the kafka_actions check via the
``datadog_kafka_actions.formats`` and ``datadog_kafka_actions.compressions``
entry-point groups. Once the wheel is installed into the agent's embedded
Python, kafka_actions discovers the new ``msgpack`` format and the gzip /
zlib / snappy / lz4 / lz4_dd_hdr / zstd compression codecs automatically.
"""

from .__about__ import __version__

__all__ = ['__version__']
