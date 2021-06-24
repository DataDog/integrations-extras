# Rundeck Integration

## Overview

Rundeck further enhances Datadog notifications with automated workflow capabilities to help diagnose issues-and, optionally, to remediate them. 

Learn more about automating your runbooks to reduce incident time [on the Rundeck website][1].

Some example use cases are:

- If a Windows/Linux service is down, attempt to restart it
- If NTP sync is off, restart the NTP service on that machine
- Clean up logs and other file waste when disk space becomes full
- Restart services in response to hung work queues
- Provision capacity in response to high utilization

Use the instructions below to configure your Datadog/Rundeck integration.

## Setup

### Installation
Prepare at least one Rundeck job that you would like to trigger using a Datadog alert.

### Configuration

#### Rundeck

1. In your Rundeck Project, click the **Webhooks** navigation option.
2. Click **Add**.
3. Give the webhook a name.  (For example, *Datadog-Restart Service*)
4. Click the **Choose Webhook Plugin** button and select **Run Job***.
5. Select the job you'd like to run when this webhook is triggered.
6. [optional] In the **Options** line, enter the following text:
`-raw ${raw} -event_type ${data.event_type}`
(This makes the full Datadog payload available as part of the job input options.)
7. Click **Create Webhook**. The URL field is automatically populated after the webhook is created.

![rundeck-setup][2]

#### Datadog setup
1. Open Datadog and go to **Integrations** > **Integrations**.
2. Search for "webhooks".

    ![search-dd][3]

3. Click on the webhooks entry shown above. It opens the configuration window.

    ![webhooks-config][4]

4. Click the **New** button and fill out the form:
  - Give the webhook a name. (a)
  - Paste the URL from your Rundeck webhook in the URL line. This corresponds to Step 7 in the section above. (b)
  - Click **Save**. (c)

    ![webhook-fill][5]

Add this integration to any alert notification in Datadog by adding the recipient of `@webhook-Rundeck_Restart_Service`. The name varies based on what you name the webhook in step 4a. When the monitor triggers an alert, the webhook runs the associated job.

Other plugins, such as Advanced Run Job, can also be used, depending on your use case.


## Data Collected

### Metrics

The Rundeck integration does not provide any metrics.

### Service Checks

The Rundeck integration does not include any service checks.

### Events

The Rundeck integration does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][6].

[1]: https://www.rundeck.com
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/rundeck/images/rundeck-setup.png
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/rundeck/images/dd-search.png
[4]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/rundeck/images/webhooks-config.png
[5]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/rundeck/images/webhook-fill.png
[6]: https://docs.datadoghq.com/help/
