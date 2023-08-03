# BlinkOps Integration

## Overview

[Blink][1] is a low-code/no-code (LCNC) platform that enables automated incident response, cloud-native operations, and security operations workflows. Blink transforms manual tasks into interactive automations backed by the security and reliability of a cloud-native platform. Every script or ticket becomes a fully-managed automation.

The user interface and [automation library][2] come with premade Datadog-based automations and use-cases. Blink helps you achieve better cloud efficiency and more competitive SLA's, with fewer operational bottlenecks.

This out-of-the-box integration enables you to:

- Trigger event-based Blink automations using Datadog incidents.
- Create and update Datadog incidents automatically from within Blink.
- View incidents or events from the Datadog Events Explorer in Blink.
- Automatically enrich and remediate Datadog incidents using Blink automations.

For more information about Blink, see the [Blink documentation][3].

## Setup

Visit [our documentation][4] for details on how to connect your Datadog workspace to Blink.

## Uninstallation

To uninstall the integration, simply delete the corresponding Datadog connection in your Blink workspace.

Once deleted, any previous authorizations or access tokens are revoked. Ensure that all API keys associated with this integration have been disabled by searching for the integration name on the Datadog [API Keys][5] page.

## Data Collected

### Events

This integration sends events and incidents to Datadog where you can search and update any relevant incidents within Blink. 

### Monitors

You can view, modify, and create Datadog monitors in Blink.

### Metrics

Blink does not include any metrics, however you can query and list metrics from your Datadog environment for use in Blink automations.

## Troubleshooting

Need help? Contact [Blink support][6].

[1]: https://www.blinkops.com/
[2]: https://library.blinkops.com/automations?vendors=Datadog
[3]: https://www.docs.blinkops.com/docs/integrations/datadog/actions
[4]: https://www.docs.blinkops.com/docs/integrations/datadog
[5]: https://app.datadoghq.com/organization-settings/api-keys
[6]: mailto:support@blinkops.com
