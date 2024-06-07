# Onepane

## Overview

Onepane is a powerful addition to your existing Datadog, Cloud, and DevOps tools, providing seamless out-of-the-box integrations. It adopts an agentless approach and features automatic asset discovery, allowing you to get value in a matter of hours, not days or weeks. Onepane comprehends your unique landscape, generating a dynamic service map of your operational environment by harnessing data from various systems. This map assists your teams in swiftly resolving incidents and streamlines the audit process. Opt for Onepane to leverage additional ROI on your existing investments. 

- Show changes and infrastructure events alongside errors to pinpoint potential root causes.
- Enable root cause investigation by correlating incidents with change data and infrastructure data.

## Setup

In Onepane:

Here's how to connect your Datadog account to Onepane 

- Access Onepane Console: Head over to the Onepane console at [console.onepane.ai][2]

- Locate Integrations: In the left-hand menu, find the "Integrations" section. Click the "Add Integration" button in the top right corner.

- Choose Datadog: From the list of available integrations, select "Datadog".

- Provide Credentials: Enter the required details for your Datadog account:
    - Datadog Site URL
    - Datadog API Key
    - Datadog Application Key

    ![Integration][4]

- Verify Connection: To ensure everything is configured correctly, click the "Test Credentials" button. This validates your entered information.

- Finalize Integration: Once satisfied, click "Create" to establish the Datadog connector. It will be deployed shortly.

    ![Deploying][5]

- View Host Resources: After successful deployment, you'll be able to see a list of host resources from your Datadog account within Onepane.

    ![Host Resource][6]

- Map Resources: Onepane allows you to map these Datadog resources to your existing Onepane resources for unified view of incidents and events across your infrastructure

    ![Onepane Mapping][7]

With these steps complete, you'll have successfully integrated Datadog with Onepane

For more details, refer to the [Onepane documentation][2]

## Uninstallation

Here's how to delete the Datadog integration from your Onepane console:

- Access Integrations: Navigate to the "Integrations" section within the Onepane console.

- Locate Datadog: Find the Datadog integration from the list.

- Initiate Deletion: Click the three dots menu (ellipsis) in the top right corner of the Datadog integration tile. Select "Delete" from the options.

- Confirm Deletion: A confirmation dialog might appear. If you're certain you want to proceed, click "Confirm" to remove the Datadog integration.

By following these steps, you'll successfully disconnect your Datadog account from Onepane.

## Data Collected

### Events

This integration sends events into Datadog.

## Troubleshooting

Need help? Contact [Datadog support][1].

[1]: https://docs.datadoghq.com/help/
[2]: https://console.onepane.ai/
[3]: https://www.onepane.ai/docs/en/articles/9220032-datadog-connector-prerequisites
[4]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/onepane/images/integration.png
[5]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/onepane/images/deploying.png
[6]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/onepane/images/host_resources.png
[7]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/onepane/images/onepane_mapping.png

