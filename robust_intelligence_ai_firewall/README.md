# Agent Check: Robust Intelligence AI Firewall

## Overview

The [Robust Intelligence AI Firewall][1] is a protective layer for AI models.

The AI Firewall inspects incoming user prompts to block malicious payloads, including any that attempt prompt injection, prompt extraction, or PII detection. The AI Firewall scans LLM model output to ensure it's free of false information, sensitive data, and harmful content. Responses that fall outside your organization’s standards are blocked from the application.

This integration monitors the AI Firewall results through the Datadog Agent. It provides users with observability of their AI security issues including metrics for allowed data points, blocked data points, and insight on why each data point was blocked.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][3] for guidance on applying these instructions.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the Robust Intelligence AI Firewall check on your host. See [Use Community Integrations][2] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-robust-intelligence-ai-firewall==1.0.0
   ```

2. Configure your integration similar to core [integrations][3]. Refer to the Configuration section below for steps specific to this integration.

### Configuration

1. Edit the `robust_intelligence_ai_firewall.d/conf.yaml` file in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your Robust Intelligence AI Firewall performance data.
    ```yaml
    init_config:

    instances:
        ## @param metrics_endpoint - string - required
        ## The URL to Robust Intelligence AI Firewall 
        ## internal metrics per loaded plugin in Prometheus
        ## format.
        #
      - openmetrics_endpoint: http://localhost:8080/metrics
    ```
   See the [sample robust_intelligence_ai_firewall.d/conf.yaml][4] file for all available configuration options.

2. To configure the integration for AI Firewall running in a containerized environment, add the following annotation to pods:
   ```yaml
   apiVersion: v1
   kind: Pod
   # (...)
   metadata:
     name: '<POD_NAME>'
     annotations:
       ad.datadoghq.com/<CONTAINER_IDENTIFIER>.checks: |
         {
           "robust_intelligence_ai_firewall": {
             "init_config": {},
             "instances": [
               {
                 "openmetrics_endpoint": "http://%%host%%:8080/metrics"
               }
             ]
           }
         }
       # (...)
   ```

3. [Restart the Agent][5].

### Validation

[Run the Agent's status subcommand][6] and look for `robust_intelligence_ai_firewall` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this check.

### Service Checks

Robust Intelligence AI Firewall does not include any service checks.

### Events

Robust Intelligence AI Firewall does not include any events.

## Troubleshooting

Need Help? Contact [Robust Intelligence Support][9].

[1]: https://www.robustintelligence.com/platform/ai-firewall
[2]: https://app.datadoghq.com/account/settings/agent/latest
[3]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[4]: https://github.com/DataDog/integrations-extras/blob/master/robust_intelligence_ai_firewall/datadog_checks/robust_intelligence_ai_firewall/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/robust_intelligence_ai_firewall/metadata.csv
[8]: https://github.com/DataDog/integrations-extras/blob/master/robust_intelligence_ai_firewall/assets/service_checks.json
[9]: mailto:help@robustintelligence.com

