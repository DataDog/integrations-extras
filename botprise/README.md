## Overview

Botprise's Datadog integration allows you to send Botprise events to the event stream in Datadog. It submits Datadog events into the system over email.
Botprise Links: 
https://www.botprise.com/
https://demoapp.botprise.com/botprise/maindashboard

## Setup


### Installation


### Configuration
1. Install the Datadog Agent on your lab devices.
2. After successful installation, your devices start sending data to Datadog. View the data on the [Datadog host list][3].
3. In Datadog, create a monitor for each of the hosts. Datadog generates alerts based on the monitor rules.
4. Configure each monitor for [metrics][4] and the respective threshold value.
5. Modify the monitor configuration to create a ServiceNow ticket for each of the incoming alerts.
6. Generate an [API key and an Application key][5] to call Datadog Rest APIs.


## Data Collected

### Metrics

The Botprise integration does not provide metrics.

### Service Checks

The Botprise integration does not include any service checks.

### Events

All events are sent to the Datadog event stream.

### Configuration
To use the Datadog API, you need to enter an [API key and an application key][5]:

Input a Datadog API Key []:xxxx9232ad913d1a864828a2df15xxxx
Input a Datadog Application Key []:xxxxcb1798718f7a2da141071e7305599d60xxxx

## Troubleshooting

Need help? Contact [Datadog support][1].

[1]: https://docs.datadoghq.com/help/
[2]: https://app.datadoghq.com/account/settings#agent
[3] https://app.datadoghq.com/infrastructure/map
[4]: https://docs.datadoghq.com/metrics/
[5]: https://docs.datadoghq.com/account_management/api-app-keys/
