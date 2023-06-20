# Agent Check: appkeeper

## Overview

SIOS AppKeeper automatically restarts failed Amazon EC2 services when notifications are received from Datadog, removing the need for expensive manual intervention. When Datadog triggers an alert, it restarts the EC2 service using the AppKeeper Recovery API.

## Setup

### Get the SIOS AppKeeper API key

Get the SIOS AppKeeper API key from AppKeeper GUI.

1. Click **Account Information**, and open the modal dialog.
2. Click **Get Token**.
3. Copy the token.

![snapshot][1]

### Install and configure the Webhooks integration

1. On the Datadog site, navigate to the [Webhooks integration][2] and install the integration.
2. Select the **Configuration** tab.
3. Under the **Webhooks** header, click **New**.
4. Enter the following URL: "https://api.appkeeper.sios.com/v2/integration/{AWS_account_ID}/actions/recover"
5. Enter the `id` and name of `name` for the monitoring instance in the **Payload** section.
3. Register the AppKeeper API token in the **Custom Headers** section.

![snapshot][3]

### Integrate with Datadog monitoring

1. Create a new Datadog [Synthetic test][4]. Click **New Test** in the top right corner.
2. In the **Define requests** step, enter the URL you want to monitor.
3. In the **Define assertions** step, click **New Assertion** and add the following parameters: When `status code` is `200`. This triggers an alert when the status code is **not** 200. If the request requires notification based on a different status, replace 200 with your status code.
4. Click **New Assertion** again and add a second set of parameters: And `response time` is less than `2000` ms. This triggers an alert when the response time is longer than 2000ms. If you require a longer or shorter duration, replace `2000` with your duration.
5. In the **Notify your team** step, add the webhook, formatted as `@webhook-name_of_the_webhook`. Include a message for the notification. **Note**: The minimum monitoring interval for the **renotify if the monitor has not been resolved** setting in this step is `Every 10 Minutes`. Setting to **Never** inhibits the webhook to call on AppKeeper's recovery API.

![snapshot][5]

Results of recoveries by AppKeeper are listed in AppKeeper's GUI.

![snapshot][6]

For more information see the [AppKeeper's Integration documentation][7].

## Data Collected

### Metrics

See [metadata.csv][8] for a list of metrics provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][9].

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/appkeeper/images/get_token.jpg
[2]: https://app.datadoghq.com/account/settings#integrations/webhooks
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/appkeeper/images/payload_header.jpg
[4]: https://app.datadoghq.com/synthetics/list
[5]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/appkeeper/images/synthetic_test_params.png
[6]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/appkeeper/images/history.jpg
[7]: https://sioscoati.zendesk.com/hc/en-us/articles/900000978443-Integration
[8]: https://github.com/DataDog/integrations-extras/blob/master/appkeeper/metadata.csv
[9]: https://docs.datadoghq.com/help/
