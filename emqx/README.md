# Agent Check: EMQX

## Overview

[EMQX][1] is a highly scalable, open-source MQTT broker designed for IoT (Internet of Things). MQTT stands for Message Queuing Telemetry Transport, which is a lightweight, publish-subscribe network protocol that transports messages between devices.

**Key features of EMQX:**
- Scalability: EMQX can handle millions of concurrent MQTT connections, making it suitable for IoT applications that require handling a large number of devices.
- Reliability: It provides stable and reliable message delivery, ensuring that data is successfully transferred between devices and servers.
- Low latency: Designed for scenarios requiring low-latency communication.
- High throughput: Capable of processing a high volume of messages efficiently.
- Clustering: EMQX can be deployed in a distributed cluster to enhance performance and reliability.


The integration of EMQX with Datadog enriches monitoring capabilities, providing valuable insights into the performance and health of MQTT brokers. This is especially beneficial in IoT applications where efficient, reliable, and real-time data transmission is critical.

**Types of data sent to Datadog:**
- Metrics: This includes performance metrics like message throughput (messages sent/received per second), number of connected clients and more.

- Node performance: Monitoring individual node performance in a cluster, such as latency, load, and operational metrics.

- Operational health: Data about the health of the MQTT broker, including, error rates, and other critical indicators.


## Setup

### Installation

Manually install the EMQX check (note that [instructions may change based on your environment][2]):

Run `datadog-agent integration install -t datadog-emqx==1.1.0`.

### Configuration

1. Edit the `emqx/conf.yaml` file, located in the `conf.d/` folder at the root of your Agent's configuration directory, to start collecting your EMQX performance data.
   
2. [Restart the Agent][4].

### Validation

[Run the Agent's status subcommand][5] and look for `emqx` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][6] for a list of metrics provided by this integration.

### Service Checks

See [service_checks.json][7] for a list of service checks provided by this integration.

### Events

EMQX does not include any events.

## Troubleshooting

Need help? Contact [EMQX support][8].

[1]: https://github.com/emqx/emqx
[2]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent
[3]: https://app.datadoghq.com/account/settings/agent/latest
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[6]: https://github.com/DataDog/integrations-extras/blob/master/emqx/metadata.csv
[7]: https://github.com/DataDog/integrations-extras/blob/master/emqx/assets/service_checks.json
[8]: https://www.emqx.com/en/support
