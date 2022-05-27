# DoControl

## Overview

This integration allows [DoControl](https://www.docontrol.io/) customers to forward their DoControl related logs and events to Datadog through automated security workflows.

## Setup

To set up this integration, you must have an active [DoControl account](https://www.docontrol.io/demo). You must also have proper admin permissions in Datadog.

### Installation

No installation is required on your host.

### Use Datadog actions in DoControls workflows

You need to create a Datadog API key and an application key to use as input parameters for Datadog actions in DoControl.

#### Create an API key in Datadog

After you create the API key, copy and save it because you are not able to access it later. For more information, see [API and Application Keys](https://docs.datadoghq.com/account_management/api-app-keys/#add-an-api-key-or-client-token).

1. Hover over your user name and select **Organization Settings**.

2. From the left panel, click **API Keys**.

3. Click **+ New Key**.

   ![Get_DD_API_Key](https://raw.githubusercontent.com/DataDog/integrations-extras/master/docontrol/images/Get_DD_API_Key.png)

4. Enter a meaningful name for the API key such as `DoControl` and click **Create Key**.

5. Copy the `Key` and save it. You need this key to create a Datadog integration in DoControl.

#### Create an application key in Datadog

After you create the application key, copy and save it because you are not able to access it later. For more information, see [API and Application Keys](https://docs.datadoghq.com/account_management/api-app-keys/#add-an-api-key-or-client-token).

1. Hover over your user name and select **Organization Settings**.
2. From the left panel, click **Application Keys**.
3. Click **+ New Key**.

![Get_DD_Application_Key](https://raw.githubusercontent.com/DataDog/integrations-extras/master/docontrol/images/Get_DD_Application_Key.png)

#### Create a Datadog integration in DoControl

1. Obtain Datadog API key and Application key from [Datadog portal](https://app.datadoghq.com/organization-settings/api-keys) as described above

2. In DoControl [Dashboard->Settings->Workflows->Secrets](https://app.docontrol.io/settings/workflows?tab=Secrets) add your Datadog API key as a new secret

   ![DC_Secrets](https://raw.githubusercontent.com/DataDog/integrations-extras/master/docontrol/images/DC_Secrets.png)

3. Create a new Workflow from a pre-established [**playbook**](https://app.docontrol.io/workflowV2/playbooks?filter=by_use_case&use_case=all) or create one from [**scratch**](https://app.docontrol.io/workflowV2/workflow/new/workflow-editor)
   ![DC_WF_Create](https://raw.githubusercontent.com/DataDog/integrations-extras/master/docontrol/images/DC_WF_Create.png)

4. Design and edit your business logic by dragging and dropping actions onto the canvas, configuring the steps and connecting them

5. From the Actions bar, under **Utilities**, drag and drop Datadog actions, **Send logs** or **Create Incident**

   ![DC_Utils](https://raw.githubusercontent.com/DataDog/integrations-extras/master/docontrol/images/DC_Utils.png)

6. Configure the actions with referring to the DD-API-KEY stored as secret (from step #2 above) and DD-APPLICATION-KEY obtained in step #1 above.

   ![DC_DD_conf](https://raw.githubusercontent.com/DataDog/integrations-extras/master/docontrol/images/DC_DD_conf.png)

7. Learn more [here](https://docs.docontrol.io/docontrol-user-guide/the-docontrol-console/workflows-beta/designing-and-editing-workflows/defining-workflow-and-action-settings#action-categories)

   

## Support

Need help? Contact [Datadog support][1].


[1]: https://docs.datadoghq.com/help/
