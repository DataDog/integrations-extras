# VNS3 Integration

## Overview

Get state information regarding your VNS3 topology's IPSec endpoints/tunnels, VNS3 Peers, and overlay clients.

- Peering links Status Check:

  ![peering][1]

- Overlay Clients Status Check:

  ![clients][2]

- IPSec tunnels Status Check:

  ![ipsec][3]

## Setup

### Configuration

To capture metrics, you need to deploy Cohesive Networks' DataDog container, set up the VNS3 firewall, and configure the container.

Read the guide [here][4].

Watch the video [here][5].

## Data Collected

### Metrics

See [metadata.csv][6] for a list of metrics provided by this integration.

### Events

The VNS3 check does not include any events.

### Service Checks

The VNS3 check does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog support][7].

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/vns3/images/peering.png
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/vns3/images/clients.png
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/vns3/images/ipsec.png
[4]: https://cohesive.net/dnld/Cohesive-Networks_VNS3-DataDog-Container-Guide.pdf
[5]: https://youtu.be/sTCgCG3m4vk
[6]: https://github.com/DataDog/integrations-extras/blob/master/vns3/metadata.csv
[7]: https://docs.datadoghq.com/help/
