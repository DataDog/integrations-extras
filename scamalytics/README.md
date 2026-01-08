## Overview

Scamalytics transforms raw IP traffic into actionable threat intelligence. The platform delivers real-time IP enrichment and provides a trustworthy, accurate risk score for every IP, offering instant context and evidence-based assessments for each connection. It detects anonymization methods such as VPNs, proxies, Tor nodes, and data center traffic, while attributing requests by geolocation, ASN, and ISP. Scamalytics also performs abuse and blacklist checks, giving organizations immediate insight into potentially malicious or high-risk IP activity in real time.

The Scamalytics Datadog integration extends these capabilities by enriching logs and network telemetry within Datadog, enhancing threat visibility, strengthening risk correlation, and providing deeper operational context across your environment.


## Setup

### 1. Update the configuration file

Inside conf.d/scamalytics.d/conf.yaml, add the Scamalytics API endpoint URL, as well as your API key:

init_config:

instances:
  - url: "https://api.scamalytics.com/?ip="
  - api_key: "<YOUR_API_KEY>" 
  - customer-id:
  "<YOUR_CUSTOMER-ID" 

### 2. Verify the integration is working

    Run: datadog-agent check scamalytics

The Scamalytics integration automatically detects and scans IP addresses found in Datadog's standard network attributes:

| Traffic Type | Standard Attribute | Description |
| :--- | :--- | :--- |
| **Inbound** | `network.client.ip` |
| **Outbound** | `network.destination.ip` |

## Troubleshooting

Need help? Contact [Scamalytics](dev@scamalytics.com).