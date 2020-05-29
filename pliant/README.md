# Agent Check: pliant

## Overview

Pliant.io enhances Datadog notifications with low-code automated workflows, creating a true close-loop-automation solution. This can help with troubleshooting, diagnosis and automated remediation.  

For more integration information, check out the [Pliant][1] site..

Examples include:

- Service restart
- Load balancer configuration
- System provisioning
- Clear disk / reprovision storage
- Provision aditional VMs or container nodes in response to load.
- De-comission resources when load is low


## Setup

### Installation

Create one or more workflows that you would like to trigger from a Datadog notification.

### Configuration

#### Pliant Setup
**Create a Pliant API Key.**
1. Log in to Pliant and click on your username at the top right of the screen to reveal a menu. Click "API Keys".

![API Key Menu step1][8]

2. From the API keys screen, click "+ Create" at the top right of the screen and title your new API key. Click save and note the the API key will be added to the table.

![Create API Key step2][9]

**Create a Pliant workflow to trigger from Datadog**

1. Navigate to the workflows tab in Pliant. Click "+ Create"  and "Create Flow" to create a new workflow. Title the workflow in the popup and click "Create" to launch the editor into our new workflow.

![Create Flow step1-a-][10]

2. Populate the flow with actions to take upon receiving the Datadog trigger. 


In this example, the workflow is called "RestartHost" and triggers a host restart from the information Datadog passes to this workflow when it is triggered.

  - To add Input variables which populated with data sent from Datadog, click the "Expand" icon on at the start of the workflow to open the Variable panel.  To create matching **Input** variables, set all of these input variables to equal empty quotes: `""`. By default, Datadog sends information for the following data:
`body`
`last_updated`
`event_type`
`title`
`date`
`org`
`id`


![Expand][11]

3. To get the endpoint of the Pliant workflow, used to trigger from Datadog with an HTTP request, click the "Expand" icon at the start of the workflow.

Click "cUrl" > "Temporary Bearer Token" and instead select the API key we just created.

![curl][12]

![select key][13]

Your endpoint looks like this: ***https://<YOUR_PLIANT_INSTANCE>/api/v1/trigger/<YOUR_PLIANT_USERNAME>/User/<PATH_TO_WORKFLOW>/<WORKFLOW_NOW>?sync=true&api_key=<YOUR_API_KEY>***

![endpoint][14]

Copy this endpoin, starting with ***https*** and ending with the full API Key. Do not include any quotes.

#### Datadog setup
1. Open Datadog and from the left sidebar, click to **Integrations** > **Integrations**.
![integrations][15]

2. Enter "webhooks" in the search bar and click on the **webhooks** entry to reveal a configuration window.
![webhookSearch][16]


3. Scroll to "webhooks". Click **New** to add a new webhook to link to the Pliant workflow. First, give the webhook a name in the "name" field. This example uses the name *RestartHost*.
![webhooksConfig2][17]

Now, paste the URL copied from step 4. For example: 

***https://<YOUR_PLIANT_INSTANCE>/api/v1/trigger/<YOUR_PLIANT_USERNAME>/User/<PATH_TO_WORKFLOW>/<WORKFLOW_NOW>?sync=true&api_key=<YOUR_API_KEY>***

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
[8]: https://www.pliant.io/wp-content/uploads/2020/05/step1.png
[9]: https://www.pliant.io/wp-content/uploads/2020/05/step2.png
[10]: https://www.pliant.io/wp-content/uploads/2020/05/step1-a-.png
[11]: https://www.pliant.io/wp-content/uploads/2020/05/expand.png
[12]: https://www.pliant.io/wp-content/uploads/2020/05/curl.png
[13]: https://www.pliant.io/wp-content/uploads/2020/05/selectDDkey.png
[14]: https://www.pliant.io/wp-content/uploads/2020/05/endpoint.png
[15]: https://www.pliant.io/wp-content/uploads/2020/05/integrations_.png
[16]: https://www.pliant.io/wp-content/uploads/2020/05/webhook_Search.png
[17]: https://www.pliant.io/wp-content/uploads/2020/05/webhooksConfig3.png
[18]: https://www.pliant.io/wp-content/uploads/2020/05/webhookForm.png
