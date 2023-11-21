# Invary

## Overview

Visualize the Runtime Integrity of your Invary managed operating systems.

Invary validates the Runtime Integrity of operating systems and detects rootkits that can deceive other systems. This integration allows Invary Runtime Integrity appraisals to be streamed to Datadog and stored as logs. Invary appraisal events contain the overall status of your endpoints' integrity, along with details on what specific sections of your endpoint's kernel have been compromised, if any.  A detailed example of an Invary appraisal event can be found at: [developers.invary.com][1].

This integration also comes with an out-of-the-box dashboard that visualizes the Runtime Integrity of your endpoints managed by Invary.  The dashboard highlights endpoints that currently lack integrity and the trend of the integrity of your endpoints over time.  In addition, the Invary dashboard provides insights into your operating system inventory at runtime, including distributions and kernel versions in use.

This integration uses the [Invary API][1].

## Setup

### Installation

The Invary integration allows you to forward details about your endpoint and appraisal from the Invary SaaS platform to your Datadog instance. No additional installation is needed on your server.

### Configuration

1. Complete the OAuth Authorization flow allowing Invary to communicate with your Datadog instance.
2. Review the "Invary Runtime Integrity" dashboard for an aggregate look at your Runtime Integrity.

### Validation

1. Review the "Invary Runtime Integrity" dashboard for timely and expected appraisal information.
2. Query your logs with the `source:invary` base query.

### Uninstallation

- Once this integration has been uninstalled, any previous authorizations are revoked. 
- Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the [API Keys page][2].

## Data Collected

### Logs

Invary forwards your Runtime Integrity appraisal results with the `source:invary` tag. 

### Metrics
The Invary Runtime Integrity integration does not include any metrics.

### Service Checks
The Invary Runtime Integrity integration does not include any service checks.

### Events
The Invary Runtime Integrity integration does not include any events.

## Troubleshooting

Need help? Contact [Invary Support][3].

[1]: https://developers.invary.com/
[2]: https://app.datadoghq.com/organization-settings/api-keys
[3]: mailto:support@invary.com

