## Overview

SpoofSentry by DomainSeal monitors your domains for email spoofing, DMARC failures, lookalike domain abuse, and phishing campaigns. This integration sends domain security events to Datadog for centralized logging, analysis, and alerting.

Events include:
- DMARC authentication failures with sender details
- Spoofing campaign detections with IP attribution
- Lookalike domain threats with risk scores
- DNS enforcement changes (SPF, DKIM, DMARC policy)
- Takedown orchestration lifecycle (created, dispatched, escalated, resolved)

## Setup

### In SpoofSentry

1. Log in to [SpoofSentry][1].
2. Go to **Settings > Integrations > SIEM**.
3. Select **Datadog**.
4. Enter your **Datadog API key** (from Datadog > Organization Settings > API Keys).
5. Select your **Datadog site** (US: `datadoghq.com`, EU: `datadoghq.eu`).
6. Click **Test Connection** to verify.

### In Datadog

Events appear automatically in **Logs** with `source:spoofsentry`. A prebuilt dashboard is installed with this integration.

### Validation

To confirm the integration is working:

1. In SpoofSentry, send a test event from **Settings > Integrations > SIEM > Datadog > Test Connection**.
2. In Datadog, navigate to **Logs** and filter by `source:spoofsentry`.
3. Verify that test events appear with the expected fields (`eventType`, `severity`, `domain`).

### Log Pipeline

The integration includes a log pipeline that:
- Maps `eventType` to `evt.name`
- Maps `severity` to log status
- Maps `domain` to `network.destination.domain`
- Categorizes severity levels

## Uninstallation

1. In SpoofSentry, go to **Settings > Integrations > SIEM** and remove the Datadog configuration.
2. In Datadog, uninstall the SpoofSentry integration from **Integrations > Integrations**.

## Data Collected

### Logs

SpoofSentry sends domain security events as JSON logs through the Datadog Logs API.

| Field | Description |
|-------|-------------|
| `eventType` | Event classification (for example, `SPOOF_THREAT_DETECTED`) |
| `severity` | `critical`, `high`, `medium`, `low`, `info` |
| `domain` | Target domain |
| `tenantId` | Customer tenant identifier |
| `message` | Human-readable event summary |

### Metrics

The SpoofSentry integration does not include any metrics.

### Service Checks

The SpoofSentry integration does not include any service checks.

### Events

The SpoofSentry integration does not include any events.

### Tags

All events include the following tags:
- `service:spoofsentry`
- `event_type:<type>`
- `severity:<level>`
- `domain:<domain>`

## Support

Need help? Contact [SpoofSentry support][2].

[1]: https://spoofsentry.com
[2]: mailto:hello@spoofsentry.com
