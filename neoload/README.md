# NeoLoad integration

## Overview

[Tricentis NeoLoad][1] simplifies and scales performance testing for APIs and microservices, as well as end-to-end application testing through protocol and browser-based capabilities.

With the NeoLoad integration, you can track NeoLoad test performance metrics to:

- Correlate application performance with load testing metrics in NeoLoad.
- Analyze and visualize NeoLoad metrics in Datadog like throughput, errors, and performance using the out-of-the-box dashboard or [Metrics Explorer][7].

## Setup

### Configuration

For detailed instructions on NeoLoad configuration, follow the [NeoLoad documentation][2]. Since NeoLoad version 9.1, you can choose which metrics to send in the **Push Counters** configuration of the Datadog Connector in NeoLoad.

Install the NeoLoad integration in Datadog to add the default NeoLoad dashboard to your dashboard list.


## Data Collected

### Metrics

See [metadata.csv][3] for a list of metrics provided by this integration.

### Events

All NeoLoad performance tests events are sent to your [Datadog Events Explorer][4].
NeoLoad sends events to the Datadog API when a performance test starts and ends.
Set the option in the **Push Counters** configuration of the Datadog Connector in NeoLoad. Available since NeoLoad 9.1.

## Troubleshooting

Need help? Contact [Datadog support][5] or [Tricentis NeoLoad support][6].

[1]: https://www.tricentis.com/products/performance-testing-neoload
[2]: https://documentation.tricentis.com/neoload/latest/en/content/reference_guide/datadog.htm
[3]: https://github.com/DataDog/integrations-extras/blob/master/neoload/metadata.csv
[4]: https://docs.datadoghq.com/events/
[5]: https://docs.datadoghq.com/help/
[6]: https://support-hub.tricentis.com/
[7]: /metrics/explorer
