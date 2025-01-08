# VNS3 Integration

## Overview

Get system and network state information from your Cohesive Networks VNS3 controller.

- Peering links Status Check:

  ![peering][1]

- Overlay Clients Status Check:

  ![clients][2]

- IPSec tunnels Status Check:

  ![ipsec][3]

- Overlay Link Status Check:

  ![links][4]

- Remote Support Status Check:

  ![remote_support][5]

- Interface Status Check:

  ![interface_status][6]

## Setup

### Configuration

Deploy and configure the Cohesive Networks Datadog plugin according to the [Datadog Agent Plugin Details][7] documentation.

## Data Collected

### Metrics

Listed above; see [metadata.csv][8] for a detailed list of metrics provided by this integration.

Netflow, log reporting, and SNMP polling are also supported.

### Events

The VNS3 integration does not include any events.

### Service Checks

The VNS3 integration does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog support][9] or [Cohesive Networks support][10].

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/vns3/images/peering.png
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/vns3/images/clients.png
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/vns3/images/ipsec.png
[4]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/vns3/images/links.png
[5]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/vns3/images/remotesupport.png
[6]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/vns3/images/interfaces.png
[7]: https://docs.cohesive.net/docs/network-edge-plugins/datadog/
[8]: https://github.com/DataDog/integrations-extras/blob/master/vns3/metadata.csv
[9]: https://docs.datadoghq.com/help/
[10]: https://support.cohesive.net/
