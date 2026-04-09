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

1. Log in to [SpoofSentry](https://spoofsentry.com)
2. Go to **Settings > Integrations > SIEM**
3. Select **Datadog**
4. Enter your **Datadog API key** (from Datadog > Organization Settings > API Keys)
5. Select your **Datadog site** (US: `datadoghq.com`, EU: `datadoghq.eu`)
6. Click **Test Connection** to verify

### In Datadog

Events appear automatically in **Logs** with `source:spoofsentry`. The pre-built dashboard is installed with this integration.

### Log Pipeline

A log pipeline is included that:
- Maps `eventType` to `evt.name`
- Maps `severity` to log status
- Maps `domain` to `network.destination.domain`
- Categorizes severity levels

## Data Collected

### Logs

SpoofSentry sends domain security events as JSON logs via the Datadog Logs API.

| Field | Description |
|-------|-------------|
| `eventType` | Event classification (e.g., `SPOOF_THREAT_DETECTED`) |
| `severity` | `critical`, `high`, `medium`, `low`, `info` |
| `domain` | Target domain |
| `tenantId` | Customer tenant identifier |
| `message` | Human-readable event summary |

### Tags

All events include these tags:
- `service:spoofsentry`
- `event_type:<type>`
- `severity:<level>`
- `domain:<domain>`

## Support

- Email: hello@spoofsentry.com
- Documentation: [https://spoofsentry.com/docs/integrations/datadog](https://spoofsentry.com/docs/integrations/datadog)
- Status: [https://spoofsentry.com/status](https://spoofsentry.com/status)
