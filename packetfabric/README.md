# PacketFabric

## Overview

[PacketFabric][1] is a global Network as a Service (NaaS) provider that offers secure, private, and on-demand connectivity services. 

You can use PacketFabric to quickly and easily build a robust network between cloud platforms, SaaS providers, and hundreds of colocation centers around the [world][2].

With this integration, you can leverage Datadog to monitor your PacketFabric network traffic data, for example
- Traffic rate metrics for physical interfaces
- Traffic rate metrics for logical interfaces

![metrics dashboard][3]

## Setup

### Installation

1. Go to the PacketFabric integration in Datadog. 
2. Click **Install**. 
3. You are redirected to the PacketFabric login page. Enter your credentials to log in. 
4. You are shown a page requesting Datadog permissions. Click **Authorize**. 

Once authorized, the metrics will be sent from PacketFabric to Datadog every 15 minutes as part of a scheduled task. 


## Uninstallation

Once this integration has been uninstalled, any previous authorizations are revoked. 

Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the API Keys page.  


## Data Collected

### Metrics
See [metadata.csv][4] for a list of metrics provided by this integration.


## Support

Need help? Contact [PacketFabric Support](mailto:support@packetfabric.com).

[1]: https://packetfabric.com
[2]: https://packetfabric.com/locations
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/packetfabric/images/metrics_dashboard.png
[4]: https://github.com/DataDog/integrations-extras/blob/master/packetfabric/metadata.csv
