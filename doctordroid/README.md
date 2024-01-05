# Doctor Droid

## Overview

Doctor Droid is an observability analytics platform that analyzes alerts history and fetches metrics from upstream and downstream services. Use the integration to:
- Decide better thresholds for alerts
- Identify alerting coverage for your services
- Enrich alerts for faster diagnosis

## Setup

### Installation
Visit [Doctor Droid](https://alertops-app.drdroid.io/)  to sign up for free. Once registered, visit the [integrations page](https://alertops-app.drdroid.io/integrations)  and add a Datadog integration. This guides you through the Datadog OAUTH2 flow to grant Doctor Droid access to your API Keys to query APM & Infra metrics for you.

### Configuration
After you add the integration, explore your alerts history within Doctor Droid to discover trends. You can create reports and playbooks to enrich your generated alerts data.

## Uninstallation

To remove the Datadog integration from Doctor Droid:
1. Navigate to the [Doctor Droid integrations page][2].
1. Click  **Delete**. 
1. Click the  **Uninstall Integration**  button to uninstall this integration from Datadog. 

After you uninstall this integration, any previous authorizations are revoked.

Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the  [API Keys management page][3].

## Support

Need help? Contact  [Doctor Droid support](mailto:support@drdroid.io).

[1]: https://alertops-app.drdroid.io/
[2]: https://alertops-app.drdroid.io/integrations
[3]: https://app.datadoghq.com/organization-settings/api-keys?filter=DoctorDroid