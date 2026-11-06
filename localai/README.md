# Agent Check: LocalAI

## Overview

[LocalAI][13] is an open source, OpenAI-compatible API server that runs language, embedding, image, and audio models locally through pluggable backends such as llama.cpp, vLLM, and whisper.cpp. It also exposes Anthropic- and Ollama-compatible routes.

This integration scrapes the Prometheus metrics that LocalAI exposes at `/metrics` and provides visibility into:

- API request latency by route and HTTP method.
- Prompt and completion tokens by model and user, and billed requests by model and route.
- Requests that finished without a usage record.
- Model failover chains: target health and switches between targets.
- Chat context compression: attempts by result, compression ratio, and duration.

## Setup

### Installation

If you are using Datadog Agent v6.8+, follow the instructions below to install the LocalAI check on your host. See the dedicated Agent guide for [installing community integrations][1] to install checks with the [Agent Manager][2] or in a [Docker environment][4].

1. [Download and launch the Datadog Agent][3].
2. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-localai==<INTEGRATION_VERSION>
   ```

3. Configure your integration in the same way as core [integrations][5].

### Configuration

LocalAI serves `/metrics` on the API port (`8080` by default). The endpoint is enabled unless LocalAI was started with `--disable-metrics-endpoint` (or `LOCALAI_DISABLE_METRICS_ENDPOINT=true`).

1. Edit the `localai.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][6] to start collecting your LocalAI metrics. See the [sample localai.d/conf.yaml][7] for all available configuration options.

   ```yaml
   init_config:

   instances:
     - openmetrics_endpoint: http://localhost:8080/metrics
   ```

   If LocalAI runs with API keys (`--api-keys` or authentication enabled), pass a key with the `headers` option, for example `Authorization: Bearer <API_KEY>`.

2. [Restart the Agent][8].

The check requests `/metrics` without compression (`Accept-Encoding: identity`): with gzip, LocalAI compresses the metrics response twice and it cannot be parsed.

The failover and compression metrics are only reported when a model uses a [failover chain][14] or [context compression][15]. The `endpoint` label of the token usage metrics is renamed to `api_endpoint`, because `endpoint` is the tag the Agent uses for the scraped URL.

### Validation

[Run the Agent's status subcommand][9] and look for `localai` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this integration.

### Service Checks

See [service_checks.json][11] for a list of service checks provided by this integration.

### Events

The LocalAI integration does not include any events.

## Support

Need help? Contact [Datadog support][12].

[1]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[2]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6v7#start-stop-and-restart-the-agent
[3]: /account/settings/agent/latest
[4]: https://docs.datadoghq.com/agent/guide/use-community-integrations/?tab=docker
[5]: https://docs.datadoghq.com/getting_started/integrations/
[6]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[7]: https://github.com/DataDog/integrations-extras/blob/master/localai/datadog_checks/localai/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[10]: https://github.com/DataDog/integrations-extras/blob/master/localai/metadata.csv
[11]: https://github.com/DataDog/integrations-extras/blob/master/localai/assets/service_checks.json
[12]: https://docs.datadoghq.com/help/
[13]: https://localai.io/
[14]: https://localai.io/features/model-failover/
[15]: https://localai.io/features/context-compression/
