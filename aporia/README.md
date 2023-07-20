# Agent Check: Aporia

## Overview

Aporia is the ML observability platform, empowering ML teams with vigilant model monitoring and real-time alerts for drift, bias, performance, and data integrity while providing seamless metric tracking through tailor-made dashboards. Aporia's Production Investigation Room serves as a collaborative notebook, streamlining root cause analysis and explainability to unlock actionable insights for optimizing model performance.


This integration allows Datadog users to report their Aporia alerts to Datadog for a unified monitoring system. Datadog users can receive, view, and track live ML alerts from Aporia within their Datadog account. Users are able to know exactly which model and monitor fired the alert, with specific configuration details and additional information about the alert. Users can also view and track alerts over time by severity within their Datadog account.


## Setup

### Installation

First you'll need an Aporia account. Visit [Aporia][1] for more information and to book a demo.

Next, [login to your Aporia account][2], visit the Aporia integrations page, and add a Datadog integration. This guides you through the Datadog OAuth2 flow to grant Aporia the necessary permissions to your Datadog account.


### Configuration

Once integrated, you can configure monitors in Aporia to send their Alerts to Datadog as well. You can track these alerts in Datadog and define follow-up actions as you see fit.

### Validation

Once integrated, go to the Datadog integration page in Aporia and send a validation event to make sure the integration works properly.


## Uninstallation

To remove the Datadog integration from Aporia, navigate to the Aporia integrations page and go to your Datadog integration. Click **Remove**. Additionally, uninstall this integration from Datadog by clicking the **Uninstall Integration** button on the integration tile. 

Once you uninstall this integration, any previous authorizations are revoked. Ensure that all API keys associated with this integration have been disabled by searching for the integration name on the [API Keys management page][3].


## Troubleshooting

Need help? Contact [Aporia support](mailto:support@aporia.com).

[1]: https://aporia.com
[2]: https://platform.aporia.com
[3]: https://app.datadoghq.com/organization-settings/api-keys?filter=Aporia
[4]: https://docs.datadoghq.com/help/
