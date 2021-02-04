# Agent Check: appkeeper

## Overview

SIOS AppKeeper automatically restarts failed Amazon EC2 services when
notifications are received from Datadog such as Synthetics, removing
the need for expensive manual intervention.

When Datadog finds the alerts, it restarts the Service via AppKeeper Recovery API.

![snapshot][1]

![snapshot][2]

## Setup

### Step 1. Get the SIOS AppKeeper API Key

Get the SIOS AppKeeper API Key from AppKeeper GUI.

1. Click **Account Information**, and open the modal dialog
2. Click **Get Token**
3. Copy the token

![snapshot][3]

### Step 2. Define the Webhook in the Datadog Integration Dashboard

1. Click on the Integration
2. Click the webhooks (*If you did not install the webhook, please install the webhook.)

![snapshot][4]

### Step 3. Define the payload and custom headers

1. Enter the **URL**: "https://api.appkeeper.sios.com/v2/integration/{AWS_account_ID}/actions/recover"
2. Enter the Instance ID and name of Services for the monitoring instance in the **Payload**
3. Register the AppKeeper API token in the **Custom Headers** "**appkeeper-integration-token**"

![snapshot][5]

### Step 4. Integrate with Datadog monitoring

As an example, create a new synthetic test and set up the integration with AppKeeper.

1. Navigate to UX Monitoring. Select **Synthetic Test**.
2. Click the **New Test** for creating the Synthetics as new

![snapshot][6]

3. Set the monitoring fields.

![snapshot][7]

4. Add the webhook that set in Step 2 and Step 3 in the Notification settings(Notify your team).

![snapshot][8]

5. Datadog has the functionality to suppress notifications when an alert is raised repeatedly.
If you set it, AppKeeper's recovery API will not be called by webhook. **Don't set it to inhibit**.

![snapshot][9]

6. Results of recoveries by AppKeeper are listed in AppKeeper's GUI.

![snapshot][10]


For more information on the AppKeeper's Integration, review the Appkeeper [documentation][11].

### Agent Installation

The AppKeeper check is not included in the [Datadog Agent][14] package, so you need to install it yourself.
See [the official community integration installation instructions][15].

### Agent Configuration

1. Edit the `appkeeper.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory.
   Change the parameter values as follows:
   * account: your AWS account
   * integrationToken: The token you got in Setup step.1 above.
     
2. [Restart the Agent][16].

## Data Collected

### Metrics

See [metadata.csv][13] for a list of metrics provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][12].

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/appkeeper/images/integration.jpg
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/appkeeper/images/integration2.jpg
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/appkeeper/images/get_token.jpg
[4]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/appkeeper/images/datadog_webhook.jpg
[5]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/appkeeper/images/payload_header.jpg
[6]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/appkeeper/images/synthetic_test.jpg
[7]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/appkeeper/images/synthetic_test2.jpg
[8]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/appkeeper/images/synthetic_test3.jpg
[9]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/appkeeper/images/synthetic_test4.jpg
[10]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/appkeeper/images/history.jpg
[11]: https://sioscoati.zendesk.com/hc/en-us/articles/900000978443-Integration
[12]: https://docs.datadoghq.com/help/
[13]: https://github.com/DataDog/integrations-extras/blob/master/appkeeper/metadata.csv
[14]: https://app.datadoghq.com/account/settings#agent
[15]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/
[16]: https://docs.datadoghq.com/agent/guide/agent-commands/#restart-the-agent
