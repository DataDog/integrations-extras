# Agent Check: Amixr

## Overview

Use Amixr to manage alerts with a Slack integration:

- Collect & analyze alerts and other events from Datadog
- Set up on-call rotations with Google calendar or in Slack
- Configure automatic escalation chains
- Receive alerts with phone calls and SMS
- Orchestrate incident management with GitOps

![Amixr_Interface][1]

## Setup

### Installation

No additional installation is needed on your server.

### Configuration

In Amixr:

1. Go to *Settings > Connect New Monitorings > Datadog > How to connect*
2. Copy Datadog webhook URL

In Datadog:

1. Navigate to the **Integrations** page from the sidebar.
2. Search for **webhook** in the search bar.
3. Enter a name for the integration, for example: `amixr-alerts-prod`.
4. Paste the webhook URL from the above step.
5. Click the save button.

### Validation

In Datadog:

1. Navigate to the **Events** page from the sidebar.
2. Type `@webhook-<integration name><YOUR TEXT HERE>`, for example: `@webhook-amixr-alerts-prod test alert`.
3. Click the post button.

In Amixr:

1. Navigate to **Incidents** from the sidebar to check if the alert was received.

## Data Collected

### Metrics

The Amixr integration does not include any metrics.

### Service Checks

The Amixr integration does not include any service checks.

### Events

The Amixr integration does not include any events.

## Troubleshooting

Need help? Contact [Amixr support][2].

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/amixr/images/amixr-interface.png
[2]: https://amixr.io/support/
