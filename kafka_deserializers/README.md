# Kafka Deserializers

## Overview

`kafka_deserializers` is a plugin pack for the [`kafka_actions`][kafka_actions]
check. It does not run on its own — installing the wheel into the Datadog Agent's
embedded Python contributes additional capabilities to `kafka_actions` via Python
entry points.

What it adds:

| Kind        | Names                                                    |
|-------------|----------------------------------------------------------|
| Format      | `msgpack`                                                |
| Compression | `gzip`, `zlib`, `snappy`, `lz4`, `lz4_dd_hdr`, `zstd`    |

Once installed, `kafka_actions` instances can set `value_format: msgpack` (or
`key_format: msgpack`) and `value_compression`/`key_compression` to one of the
codec names above. Compression runs **before** format dispatch, so a payload
compressed with gzip and serialized with msgpack is configured as
`value_compression: gzip, value_format: msgpack`.

The `lz4_dd_hdr` codec is the Datadog-specific framing used by
`DataDog/golz4` (4-byte little-endian uncompressed-size header followed by
raw LZ4 block bytes). It is **not** the standard LZ4 frame format. Use
`lz4` for the standard frame format.

## Setup

```
agent integration install -t datadog-kafka-deserializers==<version>
```

Requires `datadog-kafka-actions>=2.7.0` (the version that introduced the
plugin API).

## Writing your own plugin

Any wheel can register handlers or codecs with the same entry-point groups:

```toml
[project.entry-points."datadog_kafka_actions.formats"]
myformat = "my_pkg:MyHandler"

[project.entry-points."datadog_kafka_actions.compressions"]
mycodec = "my_pkg:MyCodec"
```

Subclass `datadog_checks.kafka_actions.formats.base.FormatHandler` or
`datadog_checks.kafka_actions.compression.base.CompressionCodec` and ship
the wheel.

## Support

This package is owned by the Data Streams Monitoring team. Internal
contact: `#data-streams-monitoring` on Slack.

[kafka_actions]: https://github.com/DataDog/integrations-core/tree/master/kafka_actions
