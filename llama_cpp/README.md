# Agent Check: llama.cpp

## Overview

[llama.cpp][13] runs large language models in GGUF format on CPUs and GPUs. Its HTTP server, `llama-server`, provides an OpenAI-compatible API and is often used to self-host models on workstations, edge devices, and Kubernetes clusters.

This integration scrapes the Prometheus metrics exposed by `llama-server` (`llamacpp:*`) and provides visibility into:

- Prompt processing and token generation throughput.
- Prompt cache reuse.
- Requests being processed and requests deferred because every slot is busy.
- Speculative decoding draft and acceptance counts.

## Setup

### Installation

If you are using Datadog Agent v6.8+, follow the instructions below to install the llama.cpp check on your host. See the dedicated Agent guide for [installing community integrations][1] to install checks with the [Agent Manager][2] or in a [Docker environment][4].

1. [Download and launch the Datadog Agent][3].
2. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-llama-cpp==<INTEGRATION_VERSION>
   ```

3. Configure your integration in the same way as core [integrations][5].

### Configuration

The metrics endpoint is disabled by default. Start `llama-server` with the `--metrics` flag, or set the `LLAMA_ARG_ENDPOINT_METRICS=1` environment variable, to expose metrics at `http://<HOST>:8080/metrics`:

```shell
llama-server -m model.gguf --metrics --host 0.0.0.0 --port 8080
```

1. Edit the `llama_cpp.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][6] to start collecting your llama.cpp metrics. See the [sample llama_cpp.d/conf.yaml][7] for all available configuration options.

   ```yaml
   init_config:

   instances:
     - openmetrics_endpoint: http://localhost:8080/metrics
   ```

   If the server was started with `--api-key`, the metrics endpoint also requires it. Pass it with the `headers` option, for example `Authorization: Bearer <API_KEY>`.

2. [Restart the Agent][8].

### Validation

[Run the Agent's status subcommand][9] and look for `llama_cpp` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this integration.

### Service Checks

See [service_checks.json][11] for a list of service checks provided by this integration.

### Events

The llama.cpp integration does not include any events.

## Support

Need help? Contact [Datadog support][12].

[1]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[2]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6v7#start-stop-and-restart-the-agent
[3]: /account/settings/agent/latest
[4]: https://docs.datadoghq.com/agent/guide/use-community-integrations/?tab=docker
[5]: https://docs.datadoghq.com/getting_started/integrations/
[6]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[7]: https://github.com/DataDog/integrations-extras/blob/master/llama_cpp/datadog_checks/llama_cpp/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[10]: https://github.com/DataDog/integrations-extras/blob/master/llama_cpp/metadata.csv
[11]: https://github.com/DataDog/integrations-extras/blob/master/llama_cpp/assets/service_checks.json
[12]: https://docs.datadoghq.com/help/
[13]: https://github.com/ggml-org/llama.cpp
