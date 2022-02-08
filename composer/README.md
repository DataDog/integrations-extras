# Agent Check: composer

## Overview

This check monitors [composer][1] through the Datadog Agent.

## Setup

Please, unzip the file, and place the validate license into the bin folder.

### Starting Composer

1. Open a terminal cd path/to/Datadog_Composer/bin

2. Run `java -jar DatadogComposer.jar` to start the composer

3. open the browser and type the following localhost:9191, enter, the composer start page appears


### Configuration

1. click Datadog on the left menu

2. give a name for the configuration, click "+"

3. find out the appkey and apikey, in the datadog environment

4. fill out the form and save it


### Validation

Please, place a validate license under the bin folder.

## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this check.

### Events

The composer integration does not include any events.

### Service Checks

The composer integration does not include any service checks.

See [service_checks.json][8] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][9].
compser@performetriks.com

[1]: **LINK_TO_INTEGRATION_SITE**
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[4]: https://github.com/DataDog/integrations-core/blob/master/check/datadog_checks/check/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-core/blob/master/check/metadata.csv
[8]: https://github.com/DataDog/integrations-core/blob/master/check/assets/service_checks.json
[9]: https://docs.datadoghq.com/help/
