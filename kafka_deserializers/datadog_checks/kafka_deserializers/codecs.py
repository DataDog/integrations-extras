# (C) Datadog, Inc. 2025-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
"""App-level compression codecs registered for the kafka_actions plugin API.

Coverage is driven by patterns observed in Datadog's dd-go and dd-source
producers. ``lz4_dd_hdr`` covers the DataDog/golz4 framing used by
xray-converter (4-byte little-endian uncompressed-size header followed by
raw LZ4 block bytes), which is *not* the standard LZ4 frame format.
"""

from __future__ import annotations

import gzip
import struct
import zlib

from datadog_checks.kafka_actions.compression.base import CompressionCodec


class GzipCodec(CompressionCodec):
    name = 'gzip'

    def decompress(self, data: bytes) -> bytes:
        return gzip.decompress(data)


class ZlibCodec(CompressionCodec):
    name = 'zlib'

    def decompress(self, data: bytes) -> bytes:
        return zlib.decompress(data)


class SnappyCodec(CompressionCodec):
    name = 'snappy'

    def decompress(self, data: bytes) -> bytes:
        import snappy

        return snappy.decompress(data)


class Lz4Codec(CompressionCodec):
    """Standard LZ4 frame format (https://github.com/lz4/lz4/blob/dev/doc/lz4_Frame_format.md)."""

    name = 'lz4'

    def decompress(self, data: bytes) -> bytes:
        import lz4.frame

        return lz4.frame.decompress(data)


class Lz4DdHdrCodec(CompressionCodec):
    """DataDog/golz4 framing: 4-byte little-endian uncompressed size + raw LZ4 block.

    Used by ``cloud-integrations/aws/xray-converter``. Not interchangeable
    with the standard LZ4 frame format.
    """

    name = 'lz4_dd_hdr'

    def decompress(self, data: bytes) -> bytes:
        import lz4.block

        if len(data) < 4:
            raise ValueError("lz4_dd_hdr payload too short for length header")
        (uncompressed_size,) = struct.unpack('<I', data[:4])
        return lz4.block.decompress(data[4:], uncompressed_size=uncompressed_size)


class ZstdCodec(CompressionCodec):
    name = 'zstd'

    def decompress(self, data: bytes) -> bytes:
        import zstandard

        return zstandard.ZstdDecompressor().decompress(data)
