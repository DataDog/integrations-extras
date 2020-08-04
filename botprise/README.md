# Agent Check: botprise

## Overview

Botprise's Datadog integration allows you to send Botprise events to the event stream in Datadog. It submits Datadog events into the system over email.

## Setup


### Installation


### Configuration
1. Install datadog agent on lab devices
2. After successful installation devices will get listed on datadog host list(https://app.datadoghq.com/infrastructure/map)
3. Create monitor for each of the host
4. Configure monitor for metric and respective threshold value. 
5. Datadog generates alert based on the monitor rules.
6. Modify monitor configuration to create ServiceNow ticket for each of the incoming alert
7. Generate API key and Application key to call Datadog Rest APIs


## Data Collected

### Metrics

The Botprise integration does not provide metrics.

### Service Checks

The Botprise integration does not include any service checks.

### Events

All events are sent to the Datadog event stream.

### Configuration
For getting datadog API invoke we need to enter API key and application key

Input a Datadog API Key []:xxxx9232ad913d1a864828a2df15xxxx
Input a Datadog Application Key []:xxxxcb1798718f7a2da141071e7305599d60xxxx

## Troubleshooting

Need help? Contact [Datadog support][1].

[1]: https://docs.datadoghq.com/help/
[2]: https://app.datadoghq.com/account/settings#agent
