# Sym Log Destination

## Overview

[Sym][1] is a platform that allows you to define simple automations that turn just-in-time access policies into easy-to-operate workflows, executed in Slack. Define access flows in Terraform, customize and integrate with other systems in code, and use our API or Slack App to request and approve/deny access.

This integration enables customers to send Sym audit logs directly to Datadog using a Sym Log Destination. 

These logs are sent in real time for every event processed by the Sym platform, such as `request` or `approve`.

## Setup

### Installation

To set up the Sym integration:
1. From the Sym Datadog Integration tile, click on "Connect Accounts".
2. Datadog will redirect you to Sym to begin the OAuth authorization flow. Enter your Sym Org ID here to continue to log in to Sym.
3. After successfully authorizing, a `sym_log_destination` Terraform resource will display. Copy and paste this into your Sym Terraform Configuration.

### Configuration

For more information about configuring your Datadog Log Destination in Terraform, see the [Sym documentation][3].

### Validation

After you have Terraformed your Datadog Log Destination, you can confirm its existence with the following `symflow` CLI command:
```
 symflow resources list sym_log_destination
```

## Uninstallation

- Uninstall the integration by clicking the Uninstall button on the integration tile.
- Once this integration has been uninstalled, any previous authorizations are revoked.
- Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the API Keys page.

## Troubleshooting

Need help? Contact us at [support@symops.com][2].

[1]: https://symops.com/
[2]: mailto:support@symops.com
[3]: https://docs.symops.com/docs/datadog
