## Overview
[Resmo][1] is a continuous asset visibility, security, and compliance solution for cloud and SaaS. Integrate with your tools to start querying and securing your resources. Monitor them in one place, run security and compliance audits, and get alerted on violations.
Using our APIs, engineers are free to focus on building core functionality, rather than having to provision and maintain servers and cloud infrastructure.

What does Resmo offer to Datadog users?
- Collect and monitor all your Datadog assets on a single platform.
- Query your Datadog monitors, roles, permissions, API Keys, and more.
- Set up rules to continuously assess your Datadog resources.
- Set up and receive rule notifications based on your Datadog resource configurations.


## Setup

1. Go to https://resmo.com, log in and navigate to **Integrations**.<br/>

![Resmo Screenshot][2]

2. Click **Add Integration** and select **Datadog**. Write a descriptive name, and optionally a description.<br />

![Resmo Screenshot][3]

3. Go to your Datadog account and create a new organization [API key][12] and a user [Application key][13].<br />

4. Return to your Resmo account and enter the copied keys into the Organization API Key and User App Key fields. <br />

![Resmo Screenshot][7]

5. Select a site from the dropdown menu on the last field.

![Resmo Screenshot][8]

6. Click the **create** button, and you're ready to query your Datadog resources.
## Data Collected

See [Resmo Datadog Resources][9] for the list of resources collected from your Datadog account.

## Uninstallation

- **In Resmo**: Go to **Settings > Integrations** and select the Datadog integration you wish to uninstall. <br />

- You have two options:
  1. To temporarily pause the integration, click the **Disable** button.
  2. To permanently remove the integration, click the **Delete** button.

## Support
Need help? Contact [Resmo support][10] or [Datadog support][11].

[1]: https://resmo.com
[2]: https://github.com/DataDog/integrations-extras/master/resmo/images/integrations.png
[3]: https://github.com/DataDog/integrations-extras/master/resmo/images/setup-integration.png
[4]: https://github.com/DataDog/integrations-extras/master/resmo/images/datadog-application-keys.png
[5]: https://github.com/DataDog/integrations-extras/master/resmo/images/datadog-new-key.png
[6]: https://github.com/DataDog/integrations-extras/master/resmo/images/datadog-created-key.png
[7]: https://github.com/DataDog/integrations-extras/master/resmo/images/resmo-key-setup.png
[8]: https://github.com/DataDog/integrations-extras/master/resmo//images/resmo-site-setup.png
[9]: https://docs.resmo.com/resources/datadog
[10]: https://www.resmo.com/contact
[11]: https://docs.datadoghq.com/help/
[12]: https://docs.datadoghq.com/account_management/api-app-keys/#add-an-api-key-or-client-token
[13]: https://docs.datadoghq.com/account_management/api-app-keys/#add-application-keys
