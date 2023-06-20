# HCP Vault Integration

## Overview

The HCP Vault integration provides an overview of your Vault clusters so you can monitor performance and cluster health.

HCP Vault metrics streaming is available for all production grade cluster tiers. The feature is not available for Development tier clusters.

For details on metrics scope and interpretation, see the [HCP Vault Metrics Guidance][1]

## Setup

### Installation

Follow the Configuration instructions below.

### Prerequisites
- A production grade HCP Vault cluster
- Your Datadog region and your [Datadog API key][2]
- An account with Admin or Contributor [role assigned in HCP][3]

### Configuration

To enable metrics streaming:

1. From the HCP Vault cluster Overview, select the Metrics view.

   ![Metrics Streaming][4]

2. If you have not yet configured metrics streaming, click Enable streaming.

3. From the Stream Vault metrics view, select Datadog as the provider.

4. Under Datadog configuration, enter your API Key and select the Datadog site region that matches your Datadog environment.

   ![Choose Provider][5]

5. Click Save. 
**Note**: HCP Vault supports metrics streaming to only one metrics endpoint at a time.

6. Navigate to Datadog, and enable the integration by clicking Install on the integration tile. This installs a HCP Vault dashboard with widgets that make the most of your HCP Vault telemetry. You can find the dashboard by searching for "HCP Vault Overview" in the dashboard list. 

## Data Collected

### Metrics

For details on metrics scope and interpretation, see the [HCP Vault Metrics Guidance][1].

### Service Checks

The HCP Vault integration does not include any service checks.

### Events

The HCP Vault integration does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][6].

[1]: https://learn.hashicorp.com/collections/vault/cloud
[2]: https://docs.datadoghq.com/account_management/api-app-keys/
[3]: https://cloud.hashicorp.com/docs/hcp/access-control
[4]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/hcp_vault/images/metrics-streaming.png
[5]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/hcp_vault/images/choose-provider.png
[6]: https://docs.datadoghq.com/help/
