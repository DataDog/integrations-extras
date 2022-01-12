# Agent Check: pliant

## Overview

Pliant.io enhances Datadog notifications with low-code automated workflows, creating a true close-loop-automation solution. This can help with troubleshooting, diagnosis, and automated remediation.

For more integration information, check out the [Pliant][1] site.

Examples include:

- Service restart
- Load balancer configuration
- System provisioning
- Clear disk / reprovision storage
- Provision additional VMs or container nodes in response to load
- De-commission resources when load is low

## Setup
### Installation

Create one or more workflows that you would like to trigger from a Datadog notification.

### Configuration
#### Pliant

1. **Create a Pliant API key** - Log in to Pliant and click on your username at the top right of the screen to reveal a menu. Click "API Keys".

![API Key Menu step1][8]

2. From the API keys screen, click "+ Create" at the top right of the screen and title your new API key. Click save and make note of the API key, which will be added to the table.

![Create API Key step2][9]

**Create a Pliant workflow to trigger from Datadog**

1. Navigate to the workflows tab in Pliant. Click "+ Create" and "Create Flow" to create a new workflow. Title the workflow in the popup and click "Create" to launch the editor into the new workflow.

![Create Flow step1-a-][10]

2. Populate the workflow with actions to take upon receiving the Datadog trigger. 

This example workflow is called "RestartHost" and restarts a host from the data Datadog triggers this workflow with.

This workflow runs with its input variables initially assigned based on the request body you trigger it with. The workflow can trigger/perform any desired infrastructure automation actions, using information from its input. In this example, restart a host with SSH under certain circumstances when Datadog triggers the automation workflow with certain parameters.

  - To add Input variables which populate with data sent from Datadog, click the "Expand" icon on at the start of the workflow to open the Variable panel. To create matching **Input** variables, set all of these input variables to equal empty quotes: `""`. By default, Datadog sends the following data:
    ```
    body
    last_updated
    event_type
    title
    date
    org
    id
    ```

There are also have additional output variables (`host`, `meta`, and `ip`) that are initialized. The workflow assigns these output variables and outputs the resulting values upon completion. It may also specify variables which are neither input nor output variables to use internally within the workflow's logic.

![Expand][11]

3. To get the endpoint of the Pliant workflow, used to trigger from Datadog with an HTTP request, click the "Expand" icon at the start of the workflow.

Click "cURL" > "Temporary Bearer Token" and select the API key you just created.

![curl][12]

![select key][13]

Your endpoint is enclosed in double quotes and resembles: ***https://<YOUR_PLIANT_INSTANCE>/api/v1/trigger/<YOUR_PLIANT_USERNAME>/User/<PATH_TO_WORKFLOW>/<WORKFLOW_NOW>?sync=true&api_key=<YOUR_API_KEY>***

![endpoint][14]

Copy the entire URL enclosed in the double quotes (which may include additional query parameters), starting with ***https***. Do not include the double quotes.

#### Datadog setup
1. Open Datadog and from the left sidebar, click to **Integrations** > **Integrations**.
![integrations][15]

2. Enter "webhooks" in the search bar and click on the **webhooks** entry to reveal a configuration window.
![webhookSearch][16]


3. Scroll to "webhooks". Click **New** to add a new webhook to link to the Pliant workflow. First, give the webhook a name in the "name" field. This example uses the name *RestartHost*.
![webhooksConfig2][17]

Paste the URL copied from step 4. For example:

```
https://<YOUR_PLIANT_INSTANCE>/api/v1/trigger/<YOUR_PLIANT_USERNAME>/User/<PATH_TO_WORKFLOW>/<WORKFLOW_NOW>?sync=true&api_key=<YOUR_API_KEY>
```

Paste this into the ***URL*** field of the webhook form.

![webhookForm][18]

The request payload is pre-configured. Check the "ENCODE AS FORM" box and click save.

Add this integration to any alert notification in Datadog by adding the recipient of `@webhook-RestartHost`. When the monitor triggers an alert, the webhook triggers your Pliant workflow, and the input variables are sent to Pliant from Datadog.

## Data Collected

### Metrics

The Pliant integration does not provide metrics.

### Service Checks

The Pliant integration does not include any service checks.

### Events

The Pliant integration does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][7].

[1]: https://pliant.io/
[2]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[3]: https://github.com/DataDog/integrations-core/blob/master/pliant/datadog_checks/pliant/data/conf.yaml.example
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://docs.datadoghq.com/help/
[8]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/pliant/images/step1.png
[9]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/pliant/images/step2.png
[10]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/pliant/images/step1-a-.png
[11]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/pliant/images/expand.png
[12]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/pliant/images/curl.png
[13]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/pliant/images/selectDDkey.png
[14]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/pliant/images/endpoint.png
[15]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/pliant/images/integrations_.png
[16]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/pliant/images/webhook_Search.png
[17]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/pliant/images/webhooksConfig3.png
[18]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/pliant/images/webhookForm.png
