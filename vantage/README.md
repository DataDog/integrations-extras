# Vantage

## Overview

Vantage is a cloud cost transparency and optimization platform. This integration allows Datadog users to import their Datadog costs into Vantage and track them alongside their other infrastructure spending, such as AWS, Snowflake, and Kubernetes.

## Setup

### Installation

Visit [Vantage][4] to sign up for free. Once registered, visit the Vantage integrations page and add a Datadog integration. This guides you through the Datadog OAUTH2 flow to grant Vantage access to your billing and usage data.

### Configuration

Once integrated, begin exploring your Datadog costs within Vantage. You can create filters for specific Datadog organizations and services alongside costs from any of the other supported Vantage providers.

### Uninstallation

To remove the Datadog integration from Vantage, visit the [integrations page][1] and click **remove**.

To ensure this integration is fully uninstalled, revoke authorization in the Configure tab of this tile or in [OAuth Apps][2] within Organization Settings in Datadog. 

Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the [API Keys management page][3].

## Support

Need help? Contact [Vantage support](mailto:support@vantage.sh).


[1]: https://console.vantage.sh/settings/integrations
[2]: https://app.datadoghq.com/organization-settings/oauth-applications
[3]: https://app.datadoghq.com/organization-settings/api-keys
[4]: https://console.vantage.sh
