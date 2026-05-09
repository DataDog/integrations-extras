# Kafka Deserializers

## Overview

Plugin pack for the [kafka_actions](https://github.com/DataDog/integrations-core/tree/master/kafka_actions) check.
Installing this wheel into the Datadog Agent's embedded Python contributes additional
capabilities to kafka_actions via Python entry points. It does not run on its own.

This pack adds:

- The msgpack format handler.
- Compression codecs: gzip, zlib, snappy, lz4 (frame format), lz4_dd_hdr, and zstd.

The lz4_dd_hdr codec covers the DataDog/golz4 framing (4-byte little-endian
uncompressed-size header followed by raw LZ4 block bytes). It is not interchangeable
with the standard LZ4 frame format.

## Setup

Install via the agent integration command:

    agent integration install -t datadog-kafka-deserializers==0.1.0

Requires datadog-kafka-actions 2.7.0 or later.

## Support

Owned by the Data Streams Monitoring team.
