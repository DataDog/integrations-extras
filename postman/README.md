# Agent Check: Postman

## Overview

[Postman][1] is an API platform that simplifies the steps of building an API and streamlines 
collaboration so you can create better APIs-faster.

This integration helps you stay on top of your monitors' health. It enables you to:

- Analyze the metrics of Postman Monitoring runs in Datadog

- Generate events for successful and failed monitoring runs.

## Setup

You can find detailed instructions in [Postman's documentation][3]. Postman Integrations require a Postman [Team, Business, or Enterprise plan][8].

### Configuration

1. Generate a Datadog [API key][6].
2. Sign in to your Postman account and navigate to the [Datadog integration][7].
3. Select "Add Integration."
4. To send your monitor metrics and events to Datadog:
   - Name your new integration.
   - Select the monitor whose data you would like to send to Datadog.
   - Enter your Datadog API key.
   - Select the Datadog region you would like to use.
   - Optionally choose if you want to send events, metrics or both for each run.
5. Then select "Add Integration" to finish setting up the integration.

![Configure Integration][4]

## Data Collected

### Metrics

See [metadata.csv][5] for a list of metrics provided by this integration.

### Service Checks

Postman does not include any service checks.

### Events

An event is generated each time a monitor runs in Postman. The severity of the event is based on the tests in the Postman monitor:

| Severity | Description                                                           |
|----------|-----------------------------------------------------------------------|
| `Low`    | If all the tests pass                                                 |
| `Normal` | If some tests fail, or an error occurs in the execution of any event. |

## Troubleshooting

Need help? Contact [Postman Support][2].

[1]: https://www.postman.com/
[2]: https://www.postman.com/support/
[3]: https://learning.postman.com/docs/integrations/available-integrations/datadog/
[4]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/postman/images/add-integration-datadog.jpeg
[5]: https://github.com/DataDog/integrations-extras/blob/master/postman/metadata.csv
[6]: https://app.datadoghq.com/organization-settings/api-keys
[7]: https://go.postman.co/integrations/service/datadog
[8]: https://www.postman.com/pricing/
