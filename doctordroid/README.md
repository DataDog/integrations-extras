# Doctor Droid

## Overview
Doctor Droid is an alert enrichment & investigation tool that will help your team streamline debugging & diagnosis workflows:
* When an alert is triggered, it automatically fetches metrics from Datadog, Cloud Provider & other observability tools and _surfaces relevant data back to your team_.
* Publishes investigation insights on Datadog dashboard and respective monitors within seconds, allowing for easy access and review within the existing workflow.
* Capability to customize basis your team's requirements and application's architecture.

Our Datadog integration fetches metrics, traces and/or events basis the features you are using within Datadog & the type of investigation required.

## Setup

### Installation
1. Navigate to the [Doctor Droid integration tile][5] in Datadog.
1. In the *Configure* tab click **Connect Accounts**. This takes you to the Integrations page within [Doctor Droid][1].
1. In Doctor Droid, navigate to the [integrations page][2] and add the Datadog integration. 
1. Follow the instructions for the Datadog OAuth flow to grant Doctor Droid access to query APM and infrastructure metrics from your Datadog account.

### Configuration
After you add the integration, explore your alerts history within Doctor Droid to discover trends. You can create reports and playbooks to enrich your generated alerts data.

## Uninstallation

To remove the Datadog integration from Doctor Droid:
1. Navigate to the [Doctor Droid integrations page][2].
1. Click  **Delete**. 
1. Navigate to the [Datadog integrations page][4]. Find and select the integration tile for Doctor Droid. 
1. From the Doctor Droid integration tile, click the  **Uninstall Integration**  button to uninstall from Datadog. 

After you uninstall this integration, any previous authorizations are revoked.

Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the [API Keys management page][3].

## Support

Need help? Contact  [Doctor Droid support](mailto:support@drdroid.io).

[1]: https://alertops-app.drdroid.io/
[2]: https://alertops-app.drdroid.io/integrations
[3]: https://app.datadoghq.com/organization-settings/api-keys?filter=Doctor%20Droid
[4]: https://app.datadoghq.com/integrations
[5]: https://app.datadoghq.com/integrations?integrationId=doctordroid