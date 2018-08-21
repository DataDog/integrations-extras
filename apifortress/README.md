## Overview

The API Fortress integration is designed to bring your API Fortress test results into Datadog with ease. The process, once set up, is automated. Users can specify either failures only or all test results. Tests that are executed via the scheduler or via external API call will then feed their data into Datadog.

## Setup

By setting up a connector and pushing the data to Datadog, all that remains is to assign the imported data (status.success, status.failure) to the desired dashboard and formatting.

**In Datadog**

You will need a Datadog API key in order to setup the connector.
Note: You must have Admin Datadog account access

Create an API key (also found under **Integrations->API**): <span class="hidden-api-key">${api_key}</span>

**In API Fortress**
1. Go to company settings (top right gear icon)
2. Click on Alert Groups
3. Create a new Alert Group (if necessary)
4. Add recipients to the Alert Group (if necessary)
5. Click on the Connectors icon
6. Choose one of the Datadog connectors from the dropdown
7. Add your Datadog API Key created previously and the Datadog host you wish the connector to pass data to

Once this process is complete, API Fortress starts passing data to Datadog where it can be charted in any way you like!

**Note: This connector shares events with Datadog, which are outages. If you would like to include performance metrics, such as latency and fetch, please contact API Fortress support to help setup a script.**

The official documentation for the Datadog connector can be [found here][1].

## Data Collected
### Metrics
Metrics are NOT collected by default, please contact API Fortress support to help setup metric submission for this integration.

See [metadata.csv][2] for a list of metrics provided by this integration.

### Events

All API Fortress deployment events are sent to your [Datadog Event Stream][3]

### Service Checks

The API Fortress integration does not include any service checks.

## Troubleshooting
Need help? Contact [Datadog Support][4].

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog][5].

[1]: http://apifortress.com/doc/setup-connectors-datadog/
[2]: https://github.com/Datadog/integrations-extras/blob/master/apifortress/metadata.csv
[3]: https://docs.datadoghq.com/graphing/event_stream/
[4]: http://docs.datadoghq.com/help/
[5]: https://www.datadoghq.com/blog/
