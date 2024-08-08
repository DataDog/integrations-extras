# Onepane

## Overview

Onepane is a GenAI tool that enhances incident resolution through automated Root Cause Analysis (RCA) by integrating seamlessly with monitoring tools like Datadog.
By integrating Onepane with Datadog, customers gain rapid incident correlation with changes and infrastructure events, significantly reducing troubleshooting time and improving operational efficiency.
The integration tracks incident data, infrastructure events, and change data (like code updates), providing valuable insights that help teams quickly identify root causes and prevent future issues.


## Setup

In Datadog:

- Generate an Application Key:

    - Access your personal settings in Datadog.

    - Navigate to the Application keys section under Organization settings.

    - Select "New Key" to generate a new Application key.

    - Name the key and create it.

    - Copy the generated Application key for future use.

In Onepane:

Here's how to connect your Datadog account to Onepane 

- Access Onepane Console: Head over to the Onepane console at [console.onepane.ai][2]

- Locate Integrations: In the left-hand menu, find the "Integrations" section. Click the "Add Integration" button in the top right corner.

- Choose Datadog: From the list of available integrations, select "Datadog".

- When you select Datadog, you will be redirected to the Datadog login page. 

- Authenticate with OAuth.

    - Log in using your Datadog credentials.

    - Upon successful authentication, Datadog will create an API key for you.

- Provide a name for your Datadog connector.

- Input the site URL and Application key obtained from the ![prerequisite steps][8].

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

When deleting the Datadog integration, the OAuth-generated API keys and other credentials will be soft-deleted and permanently deleted after 7 days.

By following these steps, you'll successfully disconnect your Datadog account from Onepane.

## Data Collected

### Events

This integration sends events into Datadog.

## Troubleshooting

Need help? Contact [Onepane support][1].

[1]: https://www.onepane.ai/docs
[2]: https://console.onepane.ai/
[3]: https://www.onepane.ai/docs/en/articles/9220032-datadog-connector-prerequisites
[4]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/onepane/images/integration.png
[5]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/onepane/images/deploying.png
[6]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/onepane/images/host_resources.png
[7]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/onepane/images/onepane_mapping.png
[8]: https://docs.onepane.ai/docs/en/articles/9419170-integrating-onepane-with-datadog-for-enhanced-incident-management

