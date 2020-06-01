# Agent Check: Amixr

## Overview

Developer-friendly Alert Management with brilliant Slack integration

- Collect & analyze alerts and other events from DataDog
- Set up On-call rotations with google calendar or right in Slack
- Configure automatic escalation chains
- Never miss alerts with Phone Calls & SMS
- Orchestrate the whole Incident Management with GitOps

![Amixr_Interface][1]

## Setup
In Amixr:
1. Go to **Settings->Connect New Monitorings->Datadog->How to connect**
2. Copy DataDog webhook url

In Datadog:
1. Go to Integrations
2. Search for **webhook** in the search bar
3. Enter name for the integration, e.g. amixr-alerts-prod
4. Paste webhook url from the above step
5. Click Save button


### Installation

### Configuration

### Validation

In Datadog:
1. Go to **Events** in the sidebar
2. Type `@webhook-<integration name>` and some text, in our example `@webhook-amixr-alerts-prod test alert`
3. Click Post button

In Amixr:
1. Go to **Incidents** in the sidebar and check if the alert was received

## Data Collected

### Metrics

Amixr does not include any metrics.

### Service Checks

Amixr does not include any service checks.

### Events

Amixr does not include any events.

## Troubleshooting

Need help? Contact [Amixr support][2].

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/amixr/images/amixr-interface.png
[2]: https://amixr.io/support/
