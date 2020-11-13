# Agent Check: appkeeper

## Overview

SIOS AppKeeper automatically restarts failed Amazon EC2 services when
notifications are received from Datadog such as Synthetics, removing
the need for expensive manual intervention.

When Datadog finds the alerts, it restarts the Service via AppKeeper Recovery API.

## Setup

### Step 1. Get the SIOS AppKeeper API Key

Get the SIOS AppKeeper API Key from AppKeeper GUI.

![snapshot][2]

### Step 2. Define the Webhook in the Datadog Integration Dashboard

![snapshot][3]

### Step 3. Define the PAYLOAD and CUSTOM HEADERS.

![snapshot][4]

1. Enter the **URL**: "https://api.appkeeper.sios.com/v2/integration/{AWS_account_ID}/actions/recover"
2. Enter the Instance ID and name of Services for the monitoring instance in the **Payload**
3. Register the AppKeeper API token in the **Custom Headers** "**appkeeper-integration-token**"

For more information on the AppKeeper's Integration, review the Appkeeper [documentation][5].

## Data Collected

### Metrics

## Troubleshooting

Need help? Contact [Datadog support][1].

[1]: https://docs.datadoghq.com/help/
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/appkeeper/images/get_token2.png
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/appkeeper/images/datadog_webhook.jpg
[4]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/appkeeper/images/payload_header.jpg
[5]: https://sioscoati.zendesk.com/hc/en-us/articles/900000978443-Integration
