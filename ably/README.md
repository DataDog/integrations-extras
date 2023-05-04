## Overview
The [Ably][1] platform is used to power real-time use cases such as multiplayer, chat, data synchronization, data broadcast, and notifications for highly scalable web and mobile applications around the world. Using our APIs, engineers are free to focus on building core functionality, rather than having to provision and maintain servers and cloud infrastructure.

The Ably Datadog Integration sends [Ably statistics][2] metrics directly to your Datadog account.

Using Ably's Datadog Integration, you can:
- Use [Ably statistics][2] alongside other key metrics in Datadog
- Correlate Ably message, channel, and connection usage for collaborative analysis in Datadog dashboards
- View and track Ably usage statistics in Datadog

## Setup

- **In Datadog**: Go to **Integrations**, select the Ably tile and click **Install Integration**.

- Click **Connect Accounts** to begin authorization of this integration. You will be redirected to [Ably][1].

- **In Ably**: Log in and navigate to **Your Apps**.

![Ably Screenshot][3]

- Select the **Ably App** you would like to set up the **Datadog Integration** for and click **Integrations**.

![Ably Screenshot][4]

- Click the **Connect to Datadog** button to begin authorization of this integration.

- You will be redirected to the Datadog authorization page.

- Click the **Authorise** button to complete setup and be redirected back to the Ably site.

![Ably Screenshot][5]

Your Ably App statistics now appear in Datadog.

## Data Collected

For further details on the Ably statistics, read the [Application Statistics documentation][8].

### Metrics

See [metadata.csv][7] for a list of metrics provided by this integration.

### Events

The Ably integration does not include any events.

### Service Checks

The Ably integration does not include any service checks.

## Uninstallation

- **In Ably**: Go to https://ably.com, log in and navigate to **Your Apps**.

- Select the Ably App you would like to uninstall the **Datadog Integration** for.

- Click the **Remove** button in the **Datadog Integration** section.

![Ably Screenshot][6]

Your Ably App statistics are no longer sent to Datadog.

- **In Datadog**: Go to **Integrations**, select the Ably tile and click **Uninstall Integration**.

Once this integration has been uninstalled, any previous authorizations are revoked.

Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the [API Keys page][9].

## Support
Need help? Contact [Ably support][10].

[1]: https://ably.com
[2]: https://ably.com/docs/general/statistics
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/ably/images/your-apps.png
[4]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/ably/images/integrations.png
[5]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/ably/images/setup-integration.png
[6]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/ably/images/uninstall-integration.png
[7]: https://github.com/DataDog/integrations-extras/blob/master/ably/metadata.csv
[8]: https://ably.com/docs/general/statistics
[9]: https://app.datadoghq.com/organization-settings/api-keys?filter=Ably
[10]: https://ably.com/support
