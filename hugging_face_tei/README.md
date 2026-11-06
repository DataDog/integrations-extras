# Agent Check: Hugging Face TEI

## Overview

[Hugging Face Text Embeddings Inference][13] (TEI) is a server for text embedding, re-ranker, and sequence classification models. It is often the embedding backend of retrieval-augmented generation (RAG) pipelines and semantic search.

This integration scrapes the Prometheus metrics exposed by TEI (`te_*`) and provides visibility into:

- Request throughput, successes, and failures by error type.
- End-to-end, tokenization, queue, and inference latency.
- Queue depth and dynamic batching (batch size and tokens per batch).
- Per-input metrics for embedding models and for re-ranker and classification models.

## Setup

### Installation

If you are using Datadog Agent v6.8+, follow the instructions below to install the Hugging Face TEI check on your host. See the dedicated Agent guide for [installing community integrations][1] to install checks with the [Agent Manager][2] or in a [Docker environment][4].

1. [Download and launch the Datadog Agent][3].
2. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-hugging-face-tei==<INTEGRATION_VERSION>
   ```

3. Configure your integration in the same way as core [integrations][5].

### Configuration

TEI exposes metrics at `/metrics` on the same port as its HTTP API, with no extra flag. For example, when running the container with `-p 8080:80`, metrics are available at `http://localhost:8080/metrics`. The endpoint does not require the API key, even when TEI runs with `--api-key`.

1. Edit the `hugging_face_tei.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][6] to start collecting your TEI metrics. See the [sample hugging_face_tei.d/conf.yaml][7] for all available configuration options.

   ```yaml
   init_config:

   instances:
     - openmetrics_endpoint: http://localhost:8080/metrics
   ```

2. [Restart the Agent][8].

### Validation

[Run the Agent's status subcommand][9] and look for `hugging_face_tei` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this integration.

The `embed.*` metrics are only reported by embedding models, and the `predict.*` metrics only by re-ranker and sequence classification models.

### Service Checks

See [service_checks.json][11] for a list of service checks provided by this integration.

### Events

The Hugging Face TEI integration does not include any events.

## Support

Need help? Contact [Datadog support][12].

[1]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[2]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6v7#start-stop-and-restart-the-agent
[3]: /account/settings/agent/latest
[4]: https://docs.datadoghq.com/agent/guide/use-community-integrations/?tab=docker
[5]: https://docs.datadoghq.com/getting_started/integrations/
[6]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[7]: https://github.com/DataDog/integrations-extras/blob/master/hugging_face_tei/datadog_checks/hugging_face_tei/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[10]: https://github.com/DataDog/integrations-extras/blob/master/hugging_face_tei/metadata.csv
[11]: https://github.com/DataDog/integrations-extras/blob/master/hugging_face_tei/assets/service_checks.json
[12]: https://docs.datadoghq.com/help/
[13]: https://huggingface.co/docs/text-embeddings-inference
