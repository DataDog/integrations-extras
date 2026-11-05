# Agent Check: vLLM Production Stack

## Overview

[vLLM Production Stack][13] is the reference Kubernetes deployment for vLLM. Its router sits in front of a pool of vLLM engines, discovers them through Kubernetes or a static list, and spreads requests across them with round-robin, session, prefix-aware, or KV cache-aware routing.

This integration scrapes the Prometheus metrics exposed by the router and provides visibility into:

- Incoming requests, end-to-end latency, errors, and token counts as seen by the router.
- Per-backend load: requests per second, running, prefill, decoding, and swapped requests, average latency, and inter-token latency.
- Per-backend prefix cache hit rate and backend health.
- CPU, memory, and disk usage of the router.

To monitor the vLLM engines themselves, use the [vLLM integration][14] alongside this one.

## Setup

### Installation

If you are using Datadog Agent v6.8+, follow the instructions below to install the vLLM Production Stack check on your host. See the dedicated Agent guide for [installing community integrations][1] to install checks with the [Agent Manager][2] or in a [Docker environment][4].

1. [Download and launch the Datadog Agent][3].
2. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-vllm-production-stack==<INTEGRATION_VERSION>
   ```

3. Configure your integration in the same way as core [integrations][5].

### Configuration

The router serves metrics at `/metrics` on its HTTP port. In the `vllm-stack` Helm chart this is the router service on port `80` (container port `8000`).

1. Edit the `vllm_production_stack.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][6] to start collecting your vLLM Production Stack metrics. See the [sample vllm_production_stack.d/conf.yaml][7] for all available configuration options.

   ```yaml
   init_config:

   instances:
     - openmetrics_endpoint: http://localhost:8000/metrics
   ```

   On Kubernetes, you can use [Autodiscovery annotations][15] on the router pod instead:

   ```yaml
   ad.datadoghq.com/router-container.checks: |
     {
       "vllm_production_stack": {
         "instances": [{"openmetrics_endpoint": "http://%%host%%:8000/metrics"}]
       }
     }
   ```

2. [Restart the Agent][8].

The per-backend metrics are tagged with `backend` (the engine URL). `backend.inter_token_latency.avg` and `backend.decoding_length.avg` report `-1` when the router has no streaming data for a backend in the stats window, and token counts only include non-streaming requests.

### Validation

[Run the Agent's status subcommand][9] and look for `vllm_production_stack` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this integration.

### Service Checks

See [service_checks.json][11] for a list of service checks provided by this integration.

### Events

The vLLM Production Stack integration does not include any events.

## Support

Need help? Contact [Datadog support][12].

[1]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[2]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6v7#start-stop-and-restart-the-agent
[3]: /account/settings/agent/latest
[4]: https://docs.datadoghq.com/agent/guide/use-community-integrations/?tab=docker
[5]: https://docs.datadoghq.com/getting_started/integrations/
[6]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[7]: https://github.com/DataDog/integrations-extras/blob/master/vllm_production_stack/datadog_checks/vllm_production_stack/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[10]: https://github.com/DataDog/integrations-extras/blob/master/vllm_production_stack/metadata.csv
[11]: https://github.com/DataDog/integrations-extras/blob/master/vllm_production_stack/assets/service_checks.json
[12]: https://docs.datadoghq.com/help/
[13]: https://github.com/vllm-project/production-stack
[14]: https://docs.datadoghq.com/integrations/vllm/
[15]: https://docs.datadoghq.com/containers/kubernetes/integrations/
