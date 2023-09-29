# Agent Check: Robust Intelligence AI Firewall

## Overview

[Robust Intelligence’s AI Firewall][1] wraps a protective layer around your AI models. It helps:
1. **Block malicious inputs in real time.** Attacks on AI systems are increasing in frequency and sophistication. The nature of large language models (LLMs) make them a disproportionally high target, but all model types are at risk. AI Firewall inspects every input and automatically blocks malicious payloads before they can do damage to your model. Risks includes prompt injection, prompt extraction, and PII detection.
2. **Validate model outputs in real time.** AI models will inevitably generate undesired responses due to both malicious and inadvertent user actions. AI Firewall scans model outputs to ensure they are absent of sensitive information, hallucinations, or otherwise harmful content. Responses that fall outside your organization’s standards will be blocked from the application. This includes sensitive data from fine-tuning or connected databases used for retrieval-augmented generation.

This integration monitors the AI Firewall results through the Datadog Agent. This includes metrics for allowed datapoints, blocked datapoints, reasons data points were blocked.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][3] for guidance on applying these instructions.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the Robust Intelligence AI Firewall check on your host. See [Use Community Integrations][2] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-robust-intelligence-ai-firewall==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][3].

### Configuration

1. Edit the `robust_intelligence_ai_firewall.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your Robust Intelligence AI Firewall performance data.
    ```yaml
    init_config:

    instances:
        ## @param metrics_endpoint - string - required
        ## The URL to Robust Intelligence AI Firewall 
        ## internal metrics per loaded plugin in Prometheus
        ## format.
        #
      - metrics_endpoint: http://localhost:8080/metrics
    ```
   See the [sample robust_intelligence_ai_firewall.d/conf.yaml][4] file for all available configuration options.

2. [Restart the Agent][5].

### Validation

[Run the Agent's status subcommand][6] and look for `robust_intelligence_ai_firewall` under the Checks section.

## Data Collected

### Metrics

Robust Intelligence AI Firewall does not include any metrics.

### Service Checks

Robust Intelligence AI Firewall does not include any service checks.

### Events

Robust Intelligence AI Firewall does not include any events.

## Troubleshooting

Need Help? Contact [Robust Intelligence Support][9].

[1]: https://www.robustintelligence.com/
[2]: https://app.datadoghq.com/account/settings/agent/latest
[3]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[4]: https://github.com/DataDog/integrations-extras/blob/master/robust_intelligence_ai_firewall/datadog_checks/robust_intelligence_ai_firewall/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/robust_intelligence_ai_firewall/metadata.csv
[8]: https://github.com/DataDog/integrations-extras/blob/master/robust_intelligence_ai_firewall/assets/service_checks.json
[9]: mailto:help@robustintelligence.com

