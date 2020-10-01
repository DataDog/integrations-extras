## Overview

Botprise's Datadog integration allows you to send generated [Botprise][7] events to Datadog using webhook. It helps to monitor your applications and to ensure Botprise is working as expected.

![image-datadog-botprise-events][9]

## Setup

To use the Botprise-Datadog integration, you must be a customer of Botprise. For more information about Botprise, visit us at [https://www.botprise.com/][10].

### Installation


### Configuration
1. Install the Datadog Agent on your lab devices.
2. After successful installation, your devices start sending data to Datadog. View the data on the [Datadog host list][3].
3. In Datadog, create a monitor for each of the hosts. Datadog generates alerts based on the monitor rules.
4. Configure each monitor for [metrics][4] and the respective threshold value.
5. Modify the monitor configuration to create a [ServiceNow][6] ticket for each of the incoming alerts.
6. Generate an [API key and an Application key][5] to call Datadog Rest APIs.


## Data Collected

### Metrics

The Botprise integration does not provide metrics.

### Service Checks

The Botprise integration does not include any service checks.

### Events

All events are sent to the Datadog event stream.

### Configuration
To use the Datadog API, you need to enter an [API key and an application key][5].

## Troubleshooting

Need help? Contact [Datadog support][1].

[1]: https://docs.datadoghq.com/help/
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://app.datadoghq.com/infrastructure/map
[4]: https://docs.datadoghq.com/metrics/
[5]: https://docs.datadoghq.com/account_management/api-app-keys/
[6]: https://developer.servicenow.com/dev.do#!/home
[7]: https://www.botprise.com/
[8]: https://demoapp.botprise.com/botprise/maindashboard
[9]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/botprise/images/datadog-botprise-events.png