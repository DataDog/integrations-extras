## Overview
The [Ably][1] platform is used to power realtime use cases such as multiplayer, chat, data synchronisation, data broadcast and notifications, for high-scale web and mobile applications around the world.

Using our APIs, engineers are free to focus on building core functionality, rather than having to provision and maintain servers and cloud infrastructure.

Using Ably’s Datadog Integration, you can:
- Monitor realtime application metrics across your Ably applications
- Track messages, channels and connection usage
- Identify unexpected activity and troubleshoot potential issues


## Setup

- **In Datadog**: Go to **Integrations**, select the Ably tile and click **Install Integration**.

- **In Ably**: Go to https://ably.com, login and navigate to **Your Apps**.<br/>

![Ably Screenshot][2]

- Select the **Ably App** you would like to setup the **Datadog Integration** for and click **Integrations**.<br />

![Ably Screenshot][3]

- Click the **Connect to Datadog** button. <br />

![Ably Screenshot][4]

Your Ably App statistics data will now appear in Datadog.

## Uninstallation

- **In Ably**: Go to https://ably.com, login and navigate to **Your Apps**.<br/>

- Select the Ably App you would like to uninstall the **Datadog Integration** for.<br />

- Click the **Remove** button in the vDatadog Integration** section.<br />

![Ably Screenshot][5]

Your Ably App statistics data will now stop being sent to Datadog.

- **In Datadog**: Go to **Integrations**, select the Ably tile and click **Uninstall Integration**.

Once this integration has been uninstalled, any previous authorizations are revoked.

Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the API Keys page.

### Metrics

See [metadata.csv][6] for a list of metrics provided by this integration.

For further details on the Ably statitics take a look at our [Application Statistics documentation][7]

## Support
Need help? Contact [Ably support][8] or [Datadog support][9]

[1]: https://ably.com
[2]: https://github.com/DataDog/integrations-extras/blob/master/ably/images/your-apps.png
[3]: https://github.com/DataDog/integrations-extras/blob/master/ably/images/integrations.png
[4]: https://github.com/DataDog/integrations-extras/blob/master/ably/images/setup-integration.png
[5]: https://github.com/DataDog/integrations-extras/blob/master/ably/images/uninstall-integration.png
[6]: https://github.com/DataDog/integrations-extras/blob/master/ably/metadata.csv
[7]: https://ably.com/docs/general/statistics
[8]: https://ably.com/support
[9]: https://docs.datadoghq.com/help/
