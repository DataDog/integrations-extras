# CHANGELOG - Kafka Deserializers

## 0.1.0 / 2026-05-08

***Added***:

* Initial release. Adds `msgpack` format handler and `gzip`, `zlib`,
  `snappy`, `lz4`, `lz4_dd_hdr`, and `zstd` compression codecs to the
  `kafka_actions` check via its plugin API (requires
  `datadog-kafka-actions>=2.7.0`).
