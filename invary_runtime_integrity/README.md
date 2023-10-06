# Invary Runtime Integrity

Visualize the Runtime Integrity of your Invary managed operating systems.

## Overview

Invary validates the Runtime Integrity of operating systems and detects rootkits that can deceive other systems.  This integration comes with a pre-built dashboard to visualize your Runtime Integrity, providing confidence in your runtime security or spotlighting endpoints that lack integrity and may be compromised.  The Invary dashboard also provides insights into your operating system inventory at runtime, including distributions and kernel versions in use. 


This integration utilizes the [Invary API][1].

## Setup

- Once this integration has been uninstalled, any previous authorizations are revoked. 
- Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the [API Keys page][3].

### Installation

The Invary integration allows for the forwarding of your endpoint and appraisal details from the Invary SaaS platform to your Datadog instance. No additional installation is needed on your server.

### Configuration

1. Complete the OAuth Authorization flow allowing Invary to communicate with your Datadog instance.
2. Review the "Invary Runtime Integrity" dashboard for an aggregate look at your Runtime Integrity.

### Validation

1. Review the "Invary Runtime Integrity" dashboard for timely and expected appraisal information.
2. Query your logs with the 'source:invary' base query.

## Data Collected

### Logs

Invary forwards your Runtime Integrity appraisal results with the 'source:invary' tag. 

## Troubleshooting

Need help? Contact [Invary Support][2].

[1]: https://developers.invary.com/
[2]: mailto:support@invary.com
[3]: https://app.datadoghq.com/organization-settings/api-keys

