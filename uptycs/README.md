# Uptycs

## Overview

Uptycs mitigates risk by prioritizing your responses to threats, vulnerabilities, misconfigurations, sensitive data exposure, and compliance requirements across your modern attack surface — all accessible through a single user interface and data model. This includes the capability to correlate threat activity as it traverses on-prem and cloud boundaries, providing a more comprehensive enterprise-wide security posture. Looking for acronym coverage? We've got you covered with CNAPP, CWPP, CSPM, KSPM, CIEM, CDR, and XDR. Start with your Detection Cloud, utilize Google-like search, and the attack surface coverage you need today. Stay prepared for what lies ahead.

For more, please visit: [Uptycs][1]

The [Uptycs][1] integration enables you to ingest your Uptycs alerts and detection into Datadog events. 
### Alert Details

Each alert contains the following main components:
   1. Title
   2. Description
   3. Id: Uptycs alert ID.
   4. Uptycs alert code.
   5. Alert severity.
   6. Alert key and value.
   7. Asset details: Asset id and host name.
   8. Uptycs URL to navigate to the Uptycs platform.

### Detection Details

Each detection contains the following main components:
   1. Title or Name
   2. Id: Uptycs detection ID.
   3. Score: Uptycs calculated score.
   4. Alerts: List of Alerts associated with the detection.
   5. Events: List of Events associated with the detection.
   5. Attack Matrix: Techniques associated with the alerts and events.
   7. Asset details: Asset id and host name.
   8. Uptycs URL to navigate to the Uptycs platform.

## Setup

To set up this integration, you must have an Uptycs account. If you are not an Uptycs customers, please [Contact Us][2] for an Uptycs account.
You'll also need Datadog API keys.
### Configuration

1. Create a [Datadog API key][3].
2. Create a Datadog Integration Destination on Uptycs platform with Datadog API keys.
   1. Go to the Configuration > Destinations.
   2. Click on New destination.
   3. Select Webhook destination type.
   3. Provide a name, the DataDog Log collection URL, the API Key as a header.

      ![my screenshot](https://raw.githubusercontent.com/DataDog/integrations-extras/master/uptycs/images/integration_setup_1.png)

   4. Provide your own custom template for alert or detection in the template field.

      ![my screenshot](https://raw.githubusercontent.com/DataDog/integrations-extras/master/uptycs/images/integration_setup_2.png)

   5. Click **save**.
3. Now that the destination is set up, let's create forwarding rule for it.
   1. Go to Configuration > Detection Forwarding Rules > New rule
   2. Provide a name, description, and choose the relevant criteria for the rule.
   3. Select the created destination in the Destinations options.

      ![my screenshot](https://raw.githubusercontent.com/DataDog/integrations-extras/master/uptycs/images/integration_setup_3.png)

   4. Select Enable Rule and click **save**.
4. The Created destination can be used for alert forwarding.
   1. Go to Configuration > Alert Rules.
   2. Select an Alert Rule or bulk select several rules.
   3. Select the created destination in the 'Destinations' options.
   4. Select options 'Notify on Every Alert', 'Close After Delivery'.

      ![my screenshot](https://raw.githubusercontent.com/DataDog/integrations-extras/master/uptycs/images/integration_setup_4.png)

   5. Click **save**.
6. Once Uptycs generates an alert or detection, it will be delivered as a DataDog Event.

### Service Checks

Uptycs does not include any service checks.

## Troubleshooting

Need help? Contact [support@uptycs.com](mailto:support@uptycs.com).

[1]: https://www.uptycs.com
[2]: https://www.uptycs.com/about/contact/
[3]: https://docs.datadoghq.com/account_management/api-app-keys/#add-an-api-key-or-client-token
