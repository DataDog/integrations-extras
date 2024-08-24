# Onepane

## Overview

Onepane is a GenAI tool that enhances incident resolution through automated root cause analysis (RCA) by integrating seamlessly with monitoring tools like Datadog.
By integrating Onepane with Datadog, customers gain rapid incident correlation with changes and infrastructure events, significantly reducing troubleshooting time and improving operational efficiency.
The integration tracks incident data, infrastructure events, and change data (such as code updates), providing valuable insights that help teams quickly identify root causes and prevent future issues.


## Setup

**In Datadog:**

- Navigate to **Integrations**, select the **Onepane** tile, click **Install Integration**.

- Click **Connect Accounts** to begin authorizing the integration. You will be redirected to [console.onepane.ai][2].

**In Onepane:**

- Log in if you're not already logged in with **Onepane**.

- Review the  the permissions and click the **Connect with datadog** button in the prompt.

    ![Onepane_prompt][10]

- You will be redirected back into Datadog to complete the authorization.

- Click the **Authorize** button to complete the setup and be redirected back to the Onepane site.

- Provide a name for your Datadog connector.

- Click **Create** to complete the integration. The Datadog connector will be deployed shortly.

    ![Deploying][5]

- View Host Resources: After successful deployment, you'll be able to see a list of host resources from your Datadog account within Onepane.

- Map Resources: Onepane allows you to map these Datadog resources to your existing Onepane resources for unified view of incidents and events across your infrastructure.

With these steps complete, you'll have successfully integrated Datadog with Onepane.

For more details, refer to the [Onepane documentation][9]

## Uninstallation

**In Onepane:**

- Log in and navigate to **Integrations**.

- Find the Datadog integration you want to uninstall in the integrations list. 

- Click the three-dot menu (ellipsis) in the top right corner of the Datadog integration tile and select **Delete** from the options.

    ![Uninstall][3]

- If a confirmation dialog appears, click **Confirm** to proceed and remove the Datadog integration.

    ![Confirmation][8]

**In Datadog:**

- Go to Integrations, select the Onepane tile and click Uninstall Integration.

- Once this integration has been uninstalled, any previous authorizations are revoked.

Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the Datadog API Keys page.

## Data Collected

### Events

This integration sends events into Datadog.

## Troubleshooting

Need help? Contact [Onepane support][1].

[1]: https://www.onepane.ai/docs
[2]: https://console.onepane.ai/
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/onepane/images/uninstall.png
[4]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/onepane/images/integration.png
[5]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/onepane/images/deploying.png
[8]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/onepane/images/confirmation.png
[9]: https://docs.onepane.ai/docs/en/articles/9419170-integrating-onepane-with-datadog-for-enhanced-incident-management
[10]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/onepane/images/onepane_prompt.png

