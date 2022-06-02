# DoControl

## Overview

This integration allows [DoControl](https://www.docontrol.io/) customers to forward their DoControl-related logs and events to Datadog through automated security workflows.

## Setup

To set up this integration, you must have an active [DoControl account](https://www.docontrol.io/demo). You must also have proper admin permissions in Datadog.

### Installation

No installation is required on your host.

### Use Datadog actions in DoControl's workflows

You must create a Datadog API key and an application key to use as input parameters for Datadog actions in DoControl.

#### Create an API key in Datadog

1. Use Datadog's [Add an API key][2] documentation to create an API key. Give the key a meaningful name such as `DoControl`.

2. Copy the `Key` and save it. This key is not accessible after exiting the page.


#### Create an application key in Datadog

1. Use Datadog's [Add application keys][3] documentation to create an application key. 
2. Copy and save your application key. This key is not accessible after exiting the page.

![Get_DD_Application_Key](https://raw.githubusercontent.com/DataDog/integrations-extras/master/docontrol/images/Get_DD_Application_Key.png)


#### Create a Datadog integration in DoControl

1. In DoControl, navigate to [Dashboard->Settings->Workflows->Secrets][4], and add your Datadog API key as a new secret.
   
   ![DC_Secrets](https://raw.githubusercontent.com/DataDog/integrations-extras/master/docontrol/images/DC_Secrets.png)

2. Create a new Workflow from a pre-established [**playbook**][5] or from [**scratch**][6].
   
   ![DC_WF_Create](https://raw.githubusercontent.com/DataDog/integrations-extras/master/docontrol/images/DC_WF_Create.png)

3. Design and edit your business logic by dragging and dropping actions onto the canvas, configuring the steps, and connecting them.

4. From the Actions bar, under **Utilities**, you can drag and drop Datadog actions into your Workflow, such as **Send logs** or **Create incident**.

   ![DC_Utils](https://raw.githubusercontent.com/DataDog/integrations-extras/master/docontrol/images/DC_Utils.png)
   
5. Configure the actions to refer to the DD-API-KEY stored as a secret in Step 1 above, and the DD-APPLICATION-KEY obtained in [Create an application key in Datadog](#create-an-application-key-in-datadog). 

![DC_DD_conf](https://raw.githubusercontent.com/DataDog/integrations-extras/master/docontrol/images/DC_DD_conf.png)

6. Learn more about DoControl in the [DoControl documentation][7].


   

## Support

Need help? Contact [Datadog support][1] or [DoControl support][8].


[1]: https://docs.datadoghq.com/help/
[2]: https://docs.datadoghq.com/account_management/api-app-keys/#add-an-api-key-or-client-token
[3]: https://docs.datadoghq.com/account_management/api-app-keys/#add-application-keys
[4]: https://app.docontrol.io/settings/workflows?tab=Secrets
[5]: https://app.docontrol.io/workflowV2/playbooks?filter=by_use_case&use_case=all
[6]: https://app.docontrol.io/workflowV2/workflow/new/workflow-editor
[7]: https://docs.docontrol.io/docontrol-user-guide/the-docontrol-console/workflows-beta/designing-and-editing-workflows/defining-workflow-and-action-settings#action-categories
[8]: mailto:support@docontrol.io
