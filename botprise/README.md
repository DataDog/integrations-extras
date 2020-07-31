# Agent Check: botprise

## Overview

We have been using datadog Rest APIs to get usage metrics from devices. As part of integration we have installed datadog agent on few lab devices. With the help of agent we retrieve usage data from the devices and raise alert if usage cross threshold value. We have setup few monitors to check alerts for each host. For every alert we have been creating Service Now ticket which comes in botprise system with webhook integration.
Later while resolving those tickets we use datadog rest API to get usage metrics and host details. Also APIs are being used for querying process details

## Setup

### Installation

The botprise check is included in the [Datadog Agent][2] package.
No additional installation is needed on your server.

### Configuration
1. Installed datadog agent on lab devices
2. After successful installation devices got listed on datadog host list
3. Created monitor for each of the host
4. Configured monitor for metric and respective threshold value. Once threshold value would cross for the metric alert will be generated.
5. Modified configuration to create ServiceNow ticket for each of the incoming alert
6. Generated API key and Application key to trigger Rest API

### Validation

<Steps to validate integration is functioning as expected>

## Data Collected

### Metrics
Botprise uses datadog metric API to get usage metrics from added devices. Also APIs are being used for querying process/infrastructure details

For getting datadog API invoke we need to enter API key and application key

Input a Datadog API Key []:xxxx9232ad913d1a864828a2df15xxxx
Input a Datadog Application Key []:xxxxcb1798718f7a2da141071e7305599d60xxxx

### Service Checks

botprise does not include any service checks.

### Events

botprise does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][1].

[1]: https://docs.datadoghq.com/help/
