# Drata

## Overview

This integration allows [Drata][5] customers to forward their compliance-related logs and events from Datadog to Drata via an API integration.

## Setup

To set up this integration, you must have an active [Drata account][6]. You must also have proper [admin permissions][7] in Datadog.

### Installation

No installation is required on your host.


#### Create an API key in Datadog

1. Use Datadog's [Add an API key][2] documentation to create an API key. Give the key a meaningful name such as `Drata`.
2. Copy the `Key` and save it.


#### Create an application key in Datadog

1. Use Datadog's [Add application keys][3] documentation to create an application key.
2. Copy and save your application key.

![Get_DD_Application_Key](https://raw.githubusercontent.com/DataDog/integrations-extras/master/drata/images/Get_DD_Application_Key.png)



## Support

Need help? Contact [Datadog support][1] or [Drata support][4].


[1]: https://docs.datadoghq.com/help/
[2]: https://docs.datadoghq.com/account_management/api-app-keys/#add-an-api-key-or-client-token
[3]: https://docs.datadoghq.com/account_management/api-app-keys/#add-application-keys
[4]: mailto:support@drata.com
[5]: https://www.drata.com
[6]: https://drata.com/demo
[7]: https://docs.datadoghq.com/account_management/rbac/permissions/
