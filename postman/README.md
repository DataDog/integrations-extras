# Agent Check: Postman

## Overview

[Postman][1] is a collaboration platform for API development. 
Postman's features simplify each step of building an API and streamline collaboration so you can create better APIs—faster.
This Integration helps you 
1. Analyze the metric from the Postman Monitor runs in Datadog
2. Generate events on each monitor run and failure for you to remain on top of your monitor health
## Setup

For the detailed instructions, follow the [Postman documentation][3].

### Installation


### Configuration

1. Generate an API key from the Datadog Integrations> API tab
2. Log into your Postman Account
3. Go to Home > Integrations > Browse All Integrations
4. Click on the Datadog Integration
5. Choose the Postman Monitor for which the metrics need to be analysed
6. Choose if you want to send metric, events or both
7. Complete other details and add the Integration to complete the configuration

![Configure Integration][4]

### Validation



## Data Collected

### Metrics

See [metadata.csv][5] for a list of metrics provided by this integration.

### Service Checks

Postman does not include any service checks.

### Events

An event is generated each time a monitor runs in Postman. The severity of the event is Low if all the Tests in the Postman 
Monitor pass and Normal in case a few of them fail or if there is error in execution of any  event.

## Troubleshooting

Need help? Contact [Postman Support][2].

[1]: https://www.postman.com/
[2]: https://www.postman.com/support/
[3]: https://learning.postman.com/docs/integrations/available-integrations/datadog/
[4]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/postman/images/add-integration-datadog.jpeg
[5]: https://github.com/DataDog/integrations-extras/blob/master/postman/metadata.csv
