# (C) Datadog, Inc. 2026-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import gzip
import struct
import zlib

import lz4.block
import lz4.frame
import pytest
import snappy
import zstandard

from datadog_checks.kafka_deserializers.codecs import (
    GzipCodec,
    Lz4Codec,
    Lz4DdHdrCodec,
    SnappyCodec,
    ZlibCodec,
    ZstdCodec,
)

PAYLOAD = b'{"a":1,"b":[1,2,3,4,5,6,7,8,9,10]}'


def test_gzip_round_trip():
    assert GzipCodec().decompress(gzip.compress(PAYLOAD)) == PAYLOAD


def test_zlib_round_trip():
    assert ZlibCodec().decompress(zlib.compress(PAYLOAD)) == PAYLOAD


def test_snappy_round_trip():
    assert SnappyCodec().decompress(snappy.compress(PAYLOAD)) == PAYLOAD


def test_lz4_frame_round_trip():
    assert Lz4Codec().decompress(lz4.frame.compress(PAYLOAD)) == PAYLOAD


def test_lz4_dd_hdr_round_trip():
    """Reproduce DataDog/golz4 framing: 4-byte LE length + raw lz4 block."""
    block = lz4.block.compress(PAYLOAD, store_size=False)
    framed = struct.pack('<I', len(PAYLOAD)) + block
    assert Lz4DdHdrCodec().decompress(framed) == PAYLOAD


def test_lz4_dd_hdr_too_short():
    with pytest.raises(ValueError, match="too short"):
        Lz4DdHdrCodec().decompress(b'\x01\x02')


def test_zstd_round_trip():
    compressed = zstandard.ZstdCompressor().compress(PAYLOAD)
    assert ZstdCodec().decompress(compressed) == PAYLOAD
