# Uptycs

## Overview

Uptycs mitigates risk by prioritizing your responses to threats, vulnerabilities, misconfigurations, sensitive data exposure, and compliance requirements across your modern attack surface - all accessible through a single user interface and data model. This includes the capability to correlate threat activity as it traverses on-prem and cloud boundaries, providing a more comprehensive enterprise-wide security posture. Looking for acronym coverage? We've got you covered with CNAPP, CWPP, CSPM, KSPM, CIEM, CDR, and XDR. Start with your Detection Cloud, utilize Google-like search, and the attack surface coverage you need today. Stay prepared for what lies ahead.

For more, please visit [the Uptycs website][1]

The Uptycs integration enables you to ingest your Uptycs alerts and detection into Datadog events.

### Alert Details

Each alert contains the following main components:
   1. Title
   2. Description
   3. Id: Uptycs alert ID.
   4. Uptycs alert code.
   5. Alert severity.
   6. Alert key and value.
   7. Asset details: Asset ID and host name.
   8. Uptycs URL to navigate to the Uptycs platform.

### Detection Details

Each detection contains the following main components:
   1. Title or Name
   2. Id: Uptycs detection ID.
   3. Score: Uptycs calculated score.
   4. Alerts: List of Alerts associated with the detection.
   5. Events: List of Events associated with the detection.
   5. Attack Matrix: Techniques associated with the alerts and events.
   7. Asset details: Asset ID and host name.
   8. Uptycs URL to navigate to the Uptycs platform.

## Setup

To set up this integration, you must have an Uptycs account. If you are not an Uptycs customer, please [Contact Us][2] for an Uptycs account.
You'll also need Datadog API keys.

### Configuration

1. Create a [Datadog API key][3].
2. Create a Datadog Integration Destination on the Uptycs platform using your Datadog API key:
   1. Go to Configuration > Destinations.
   2. Click on New destination.
   3. Select **Datadog** destination type.
   4. Provide a name for the destination, your Datadog domain, and your API Key. You can also add custom templates for alerts or detections in the template field.

      ![Integration setup part 1](https://raw.githubusercontent.com/DataDog/integrations-extras/master/uptycs/images/integration_setup_1.png)

   5. Click **Save**.
3. Once the destination is set up, create a forwarding rule for it.
   1. Go to Configuration > Detection Forwarding Rules > New rule
   2. Provide a name and description, then choose the relevant criteria for the rule.
   3. In the 'Destinations' options, select the newly created destination.

      ![Integration setup part 2](https://raw.githubusercontent.com/DataDog/integrations-extras/master/uptycs/images/integration_setup_2.png)

   4. Select Enable Rule and click **Save**.
4. The created destination can be used for alert forwarding.
   1. Go to Configuration > Alert Rules.
   2. Select an Alert Rule or bulk select several rules.
   3. In the 'Destinations' options, select the newly created destination.
   4. Select the options for 'Notify on Every Alert' and 'Close After Delivery'.

      ![Integration Setup part 3](https://raw.githubusercontent.com/DataDog/integrations-extras/master/uptycs/images/integration_setup_3.png)

   5. Click **Save**.
6. Once Uptycs generates an alert or detection, it will be delivered as a Datadog Event.

## Troubleshooting

Need help? Contact [support@uptycs.com](mailto:support@uptycs.com).

[1]: https://www.uptycs.com
[2]: https://www.uptycs.com/about/contact/
[3]: https://docs.datadoghq.com/account_management/api-app-keys/#add-an-api-key-or-client-token
