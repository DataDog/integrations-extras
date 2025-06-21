# Agent Check: stonebranch_universal_controller

## Overview

This check monitors [stonebranch_universal_controller][1].

Include a high level overview of what this integration does:
- This integration will allow the user to collect metric data from the Universal Controller.
- The customer is able to create advanced monitoring dashboards and create alerts for the most important tasks and processes running on the Universal Controller
- For example: Monitor your important automated workflows for errors and allow yourself to have an overview of all your most important tasks.

## Setup

### Installation

To install the stonebranch_universal_controller check on your host:


1. Install the [developer toolkit]
(https://docs.datadoghq.com/developers/integrations/python/)
 on any machine.

2. Run `ddev release build stonebranch_universal_controller` to build the package.

3. [Download the Datadog Agent][2].

4. Upload the build artifact to any host with an Agent and
 run `datadog-agent integration install -w
 path/to/stonebranch_universal_controller/dist/<ARTIFACT_NAME>.whl`.

### Configuration

Create a config.yaml based on the example you can find in the conf.d/stonebranch_universal_controller inside of the datadog agent.
Inside of the config.yaml add a user that has the permissions to access your metric endpoint.
If you did not already, enable [OpenTelemetry in your Universal Controller][10] 
### Validation

To check if the integration has been successfully enabled, run the command `datadog-agent check stonebranch_universal_controller` there will be a confirmation message in your console.

## Data Collected

### Metrics

To view all collected metrics including labels visit our [Metrics Documentation][11], there is also the option of enabling custom labels for a more in-depth look into the collected metrics. How to enable them and what they will add can be found [here][12].

## Troubleshooting

Need help? Contact [Datadog support][3].

[1]: **LINK_TO_INTEGRATION_SITE**
[2]: https://app.datadoghq.com/account/settings/agent/latest
[3]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[4]: https://github.com/DataDog/integrations-extras/blob/master/stonebranch_universal_controller/datadog_checks/stonebranch_universal_controller/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/stonebranch_universal_controller/metadata.csv
[8]: https://github.com/DataDog/integrations-extras/blob/master/stonebranch_universal_controller/assets/service_checks.json
[9]: https://docs.datadoghq.com/help/
[10]: https://stonebranchdocs.atlassian.net/wiki/spaces/UC78/pages/1086463674/Integrating+OpenTelemetry
[11]: https://stonebranchdocs.atlassian.net/wiki/spaces/UA78/pages/1086492473/Provided+Metrics
[12]: https://stonebranchdocs.atlassian.net/wiki/spaces/UC78/pages/1086484929/Properties#Properties-Overview