# Cequence

## Overview

This integration provides Cequence Security customers with a preconfigured dashboard to view all of their API Runtime Inventory and Threat Detection log data within Datadog. This enables in-depth insights into your API Security posture. The log data export configuration must take place within your [Cequence Security Unified Platform][3].

## Setup

No configuration is needed to install the Cequence Datadog dashboard.

1. Log in to Datadog.
2. Navigate to [Integrations][7].
3. Search for Cequence.
4. Highlight the integration and Click **+ Install**.

### Installation

Navigate to Datadog Integrations and select Cequence. Then select Install.

### Cequence Configuration

1. Generate a new Integration API Key in your [Datadog portal][4].
2. Use the following integration [article][3] to configure your Cequence Platform to Export Logs to Datadog 
 - Be sure to configure your Data Export to use the following datadog API ingest url. This is critical for the functionality of this integration
   https://http-intake.logs.datadoghq.com/api/v2/logs?ddsource=cequence


### Datadog Configuration

The following configuration must take place within the Datadog Portal.

1. Login to your Datadog portal.
2. Navigate to [Integrations][7]
3. Search for Cequence
4. Highlight the integration and Click + Install.

## Data Collected
All Datadog accesss and export data is configured on the Cequence UAP Platform. The Cequence Platform will export these logs into the Datadog repository.

### API Sentinel Detection Events

API Sentinel can be configured to export all API Runtime events from the Cequence Platform to Datadog.

### API Spartan Detection Events

API Spartan can be configured to export all Detection events from the Cequence Platform to Datadog.

### API Spartan Mitigation Events

API Spartan can be configured to export all Mitigation events from the Cequence Platform to Datadog.

## Troubleshooting

Need help? Contact [Cequence support][8].

[1]: https://docs.datadoghq.com/help/
[2]: https://www.cequence.ai/
[3]: https://helpdesk.cequence.ai/hc/en-us/articles/8614818269079-Cequence-UAP-Logging-to-Datadog-Log-Management-Overview
[4]: https://app.datadoghq.com/organization-settings/api-keys
[5]: mailto:support@cequence.ai
[6]: https://helpdesk.cequence.ai/hc/en-us/articles/8614818269079-Cequence-UAP-Logging-to-Datadog-Log-Management-Overview6
[7]: https://app.datadoghq.com/integrations
[8]: https://helpdesk.cequence.ai/hc/en-us
