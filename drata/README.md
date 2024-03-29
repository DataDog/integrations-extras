# Drata

## Overview

Drata is a security and compliance automation platform that continuously monitors and collects evidence of a company's security controls, while streamlining compliance workflows end-to-end to ensure audit readiness.

This integration allows [Drata][5] customers to forward their compliance-related logs and events from Datadog to Drata through an API integration.

## Setup

To set up this integration, you must have an active [Drata account][6]. You must also have proper [admin permissions][7] in Datadog.

### Installation

1. To install this integration, you need to create an API and App key.
2. We recommend creating a Service Account in Datadog and applying the "Datadog Read Only" Role to give this connection limited permissions.
3. Navigate to your organization settings to [create an API key][2] in Datadog. Give the key a meaningful name such as `Drata`.
4. Copy and save your API `Key`.
5. Within your organization settings, [create an application key][3]. 
6. Copy and save your application key.
7. Paste your API key and application key into the Drata connection drawer for Datadog.
8. Drata will begin syncing user and configuration data from the Datadog API's and notify you if any compliance monitors are failing.


## Support

Need help? Contact [Datadog support][1] or [support@drata.com][4].


[1]: https://docs.datadoghq.com/help/
[2]: https://docs.datadoghq.com/account_management/api-app-keys/#add-an-api-key-or-client-token
[3]: https://docs.datadoghq.com/account_management/api-app-keys/#add-application-keys
[4]: mailto:support@drata.com
[5]: https://www.drata.com
[6]: https://drata.com/demo
[7]: https://docs.datadoghq.com/account_management/rbac/permissions/