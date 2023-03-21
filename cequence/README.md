# Cequence

## Overview

This integration provides Cequence Security customers with a preconfigured dashboard to view all of their Cequence Platform related logs in Datadog. This integration provides all of the necessary pipeline and dashboard configuration to provide Cequence Security customers with a seamless Datadog Dashboard integration.

## Setup

All configuration is automated by this Datadog Integration. All customers need to do is click +Install to install the Cequence Datadog Dashboard and all of the necessary components will be deployed in Datadog.

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

Sentinel can be configured to export all information needed.

### API Spartan Detection Events

Spartan can be configured to export all information needed.

### API Spartan Mitigation Events

Spartan can be configured to export all information needed.

## Troubleshooting

Need help with Datadog? Contact [Datadog support][1].
Need help with Cequence? Contact [Cequence support][8].

[1]: https://docs.datadoghq.com/help/
[2]: https://www.cequence.ai/
[3]: https://helpdesk.cequence.ai/hc/en-us/articles/8614818269079-Cequence-UAP-Logging-to-Datadog-Log-Management-Overview
[4]: https://app.datadoghq.com/organization-settings/api-keys
[5]: mailto:support@cequence.ai
[6]: https://helpdesk.cequence.ai/hc/en-us/articles/8614818269079-Cequence-UAP-Logging-to-Datadog-Log-Management-Overview6
[7]: https://app.datadoghq.com/integrations
[8]: https://helpdesk.cequence.ai/hc/en-us
