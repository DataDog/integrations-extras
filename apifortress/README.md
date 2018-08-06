## Overview

The API Fortress integration is designed to bring your API Fortress test results into DataDog with ease. The process, once set up, is automated. Users can specify either failures only or all test results. Tests that are executed via the scheduler or via external API call will then feed their data into DataDog for visualization.

## Setup

By setting up a connector and pushing the data to DataDog, all that remains is to assign the imported data (status.success, status.failure) to the desired dashboard and formatting.

**In Datadog**
You will need a Datadog API key in order to setup the connector.
Note: You must have Admin DataDog account access

Create an API key (also found under **Integrations->API**): <span class="hidden-api-key">${api_key}</span>

**In API Fortress**
1. Go to company settings (top right gear icon)
2. Click on Alert Groups
3. Create a new Alert Group (if necessary)
4. Add recipients to the Alert Group (if necessary)
5. Click on the Connectors icon
6. Choose one of the DataDog connectors from the dropdown
7. Add your DataDog API Key created previously and the DataDog host you wish the connector to pass data to

Once this process is complete, API Fortress will begin passing data to DataDog where it can be charted in any way you like!

Note: This connector shares events with Datadog, which are outages. If you would like to include performance metrics, such as latency and fetch, please let us know and we can help set that up. It requires a small script.

The official documentation for the DataDog connecter can be [found here][1].

## Data Collected
### Metrics
See [metadata.csv][2] for a list of metrics provided by this integration.

### Events

All API Fortress deployment events are sent to your [Datadog Event Stream][3]

### Service Checks

The API Fortress integration does not include any service checks at this time.

## Troubleshooting
Need help? Contact [Datadog Support][4].

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog][5].

[1]: http://apifortress.com/doc/setup-connectors-datadog/
[2]: https://github.com/DataDog/integrations-extras/blob/master/apifortress/metadata.csv
[3]: https://docs.datadoghq.com/graphing/event_stream/
[4]: http://docs.datadoghq.com/help/
[5]: https://www.datadoghq.com/blog/
