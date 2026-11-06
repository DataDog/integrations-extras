# Agent Check: Xinference

## Overview

[Xinference][13] (Xorbits Inference) serves language, embedding, rerank, image, audio, and video models behind an OpenAI-compatible API, on a single machine or as a cluster of a supervisor and workers. Each model runs on an engine such as vLLM, SGLang, llama.cpp, MLX, or Transformers.

This integration scrapes the Prometheus metrics that Xinference exposes and provides visibility into:

- Model requests, failures, latency, and concurrency for every model type.
- Time to first token and input, output, and generated tokens for language models.
- Model load time and lifecycle status, number of loaded models, and online workers.
- Worker CPU and memory usage.
- API key usage by key, user, model, and result, and banned clients.
- Supervisor HTTP API requests and responses by path and status code.

## Setup

### Installation

If you are using Datadog Agent v6.8+, follow the instructions below to install the Xinference check on your host. See the dedicated Agent guide for [installing community integrations][1] to install checks with the [Agent Manager][2] or in a [Docker environment][4].

1. [Download and launch the Datadog Agent][3].
2. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-xinference==<INTEGRATION_VERSION>
   ```

3. Configure your integration in the same way as core [integrations][5].

### Configuration

Xinference exposes two kinds of metrics endpoints, both enabled by default (set `XINFERENCE_DISABLE_METRICS=1` to turn them off):

- The supervisor, or `xinference-local`, serves cluster, model status, API key, and HTTP API metrics at `/metrics` on the API port (`9997` by default).
- Each worker serves its model request and token metrics on a separate metrics server. Set its port with `--metrics-exporter-port` (for example, `xinference-local --metrics-exporter-port 9998` or `xinference-worker --metrics-exporter-port 9998`).

1. Edit the `xinference.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][6] to start collecting your Xinference metrics. Configure one instance per endpoint. See the [sample xinference.d/conf.yaml][7] for all available configuration options.

   ```yaml
   init_config:

   instances:
     - openmetrics_endpoint: http://localhost:9997/metrics
     - openmetrics_endpoint: http://localhost:9998/metrics
   ```

2. [Restart the Agent][8].

The metrics endpoints do not require authentication.

### Validation

[Run the Agent's status subcommand][9] and look for `xinference` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this integration.

### Service Checks

See [service_checks.json][11] for a list of service checks provided by this integration.

### Events

The Xinference integration does not include any events.

## Support

Need help? Contact [Datadog support][12].

[1]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[2]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6v7#start-stop-and-restart-the-agent
[3]: /account/settings/agent/latest
[4]: https://docs.datadoghq.com/agent/guide/use-community-integrations/?tab=docker
[5]: https://docs.datadoghq.com/getting_started/integrations/
[6]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[7]: https://github.com/DataDog/integrations-extras/blob/master/xinference/datadog_checks/xinference/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[10]: https://github.com/DataDog/integrations-extras/blob/master/xinference/metadata.csv
[11]: https://github.com/DataDog/integrations-extras/blob/master/xinference/assets/service_checks.json
[12]: https://docs.datadoghq.com/help/
[13]: https://github.com/xorbitsai/inference
