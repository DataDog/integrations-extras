# Agent Check: appkeeper

## Overview

SIOS AppKeeper automatically restarts failed Amazon EC2 services when notifications are received from Datadog, removing the need for expensive manual intervention. When Datadog triggers an alert, it restarts the EC2 service via the AppKeeper Recovery API.

## Setup

### Agent Installation

The AppKeeper check is not included in the [Datadog Agent][14] package, so you need to install it yourself.
See [the official community integration installation instructions][15].

### Agent Configuration

1. Edit the `appkeeper.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory.
   Change the parameter values as follows:
   * account: your AWS account
   * integrationToken: The token you got in Setup step.1 above.

2. [Restart the Agent][16].

### AppKeeper Setting
#### Step 1. Get the SIOS AppKeeper API Key

Get the SIOS AppKeeper API key from AppKeeper GUI.

1. Click **Account Information**, and open the modal dialog.
2. Click **Get Token**.
3. Copy the token.

![snapshot][1]

#### Step 2. Define the Webhook in the Datadog Integration Dashboard

1. In the Datadog app, navigate to the [Webhooks integration][2] and install the integration.
2. Select the **Configuration** tab.
3. Under the **Webhooks** header, click **New**.
4. Enter the following URL: "https://api.appkeeper.sios.com/v2/integration/{AWS_account_ID}/actions/recover"
5. Enter the `id` and name of `name` for the monitoring instance in the **Payload** section.
3. Register the AppKeeper API token in the **Custom Headers** section.

![snapshot][3]

#### Step 3. Define the payload and custom headers

1. Create a new Datadog [Synthetic test][4]. Click **New Test** in the top right corner.
2. In the **Define requests** step, enter the URL you want to monitor.
3. In the **Define assertions** step, click **New Assertion** and add the following parameters: When `status code` is `200`. This will trigger an alert when the status code is **not** 200. If the request requires notification based on a different status, replace 200 with your status code.
4. Click **New Assertion** again and add a second set of parameters: And `response time` is less than `2000` ms. This will trigger an alert when the response time is longer than 2000ms. If you require a longer or shorter duration, replace `2000` with your duration.
5. In the **Notify your team** step, add the webhook, formatted as `@webhook-name_of_the_webhook`. Include a message for the notification. **Note**: The minimum monitoring interval for the **renotify if the monitor has not been resolved** setting in this step is `Every 10 Minutes`. Setting to **Never** inhibits the webhook to call on AppKeeper's recovery API.

![snapshot][5]

#### Step 4. Integrate with Datadog monitoring

As an example, create a new synthetic test and set up the integration with AppKeeper.

1. Navigate to UX Monitoring. Select **Synthetic Test**.
2. Click the **New Test** for creating the Synthetics as new

![snapshot][6]

For more information on the AppKeeper's Integration, review the AppKeeper [documentation][7].

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
