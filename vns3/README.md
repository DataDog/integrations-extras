## Overview

Get state information regarding your VNS3 topology's IPSec endpoints/tunnels, VNS3 Peers, and overlay clients.

*   Peering links Status Check:

    ![peering](https://raw.githubusercontent.com/DataDog/integrations-extras/master/vns3/images/peering.png)

*   Overlay Clients Status Check:

    ![clients](https://raw.githubusercontent.com/DataDog/integrations-extras/master/vns3/images/clients.png)

*   IPSec tunnels Status Check:

    ![ipsec](https://raw.githubusercontent.com/DataDog/integrations-extras/master/vns3/images/ipsec.png)

## Setup

### Configuration

To capture metrics, you need to deploy Cohesive Networks' DataDog container, set up the VNS3 firewall, and configure the container.

Read the guide [here](https://cohesive.net/dnld/Cohesive-Networks_VNS3-DataDog-Container-Guide.pdf).

Watch the video [here](https://youtu.be/sTCgCG3m4vk).

## Data Collected
### Metrics
See [metadata.csv](https://github.com/DataDog/integrations-extras/blob/master/vns3/metadata.csv) for a list of metrics provided by this integration.

### Events
The VNS3 check does not include any events at this time.

### Service Checks
The VNS3 check does not include any service checks at this time.

## Troubleshooting
Need help? Contact [Datadog Support](http://docs.datadoghq.com/help/).

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog](https://www.datadoghq.com/blog/).

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/vns3/images/peering.png
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/vns3/images/clients.png
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/vns3/images/ipsec.png
[4]: https://cohesive.net/dnld/Cohesive-Networks_VNS3-DataDog-Container-Guide.pdf
[5]: https://youtu.be/sTCgCG3m4vk
[6]: https://github.com/DataDog/integrations-extras/blob/master/vns3/metadata.csv
[7]: http://docs.datadoghq.com/help/
[8]: https://www.datadoghq.com/blog/
