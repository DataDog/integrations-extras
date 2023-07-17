# Sym Log Destination

## Overview

Sym is a platform for defining simple automations that turn just-in-time access policies into easy-to-operate workflows, executed in Slack. Define access flows in Terraform, customize and integrate with other systems in code, and then use our API or Slack App to request and approve/deny access. Simple!

This integration enables customers to send Sym audit logs directly to Datadog via a Sym Log Destination. 
These logs are sent in real time for every Event processed by the Sym platform, such as `request` or `approve`.

## Setup

### Installation

To set up the Sym integration:
1. Go to your [Datadog Integrations page](https://app.datadoghq.com/integrations) and click on the Sym tile.
2. Click on "Install Integration".
3. Datadog will redirect you to Sym to begin the OAuth authorization flow. Enter your Sym Org ID here to continue to log in to Sym.
4. After authenticating, Sym will redirect you to Datadog to authorize Sym with the `api_keys_write` scope. After you authorize Sym, Sym will create an API Key in your Datadog organization, which will be used to send logs to Datadog directly.
5. If Sym successfully connects with Datadog, a `sym_log_destination` Terraform resource will be displayed that should be copied into your Sym Terraform Configuration.

### Configuration

Check out the [Sym Docs](https://docs.symops.com/docs/datadog) for detailed instructions on how to configure your Datadog Log Destination in Terraform.

### Validation

After you have Terraformed your Datadog Log Destination, you can confirm its existence with:
```
 symflow resources list sym_log_destination
```

## Troubleshooting

Need help? Contact us at support@symops.com.


