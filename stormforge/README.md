# StormForge Optimize Live

## Overview

[StormForge Optimize Live][1] applies machine learning to your observability metrics to make real-time recommendations to resource requests for any deployment running in Kubernetes.

**With StormForge Optimize Live, you can:**
- Improve resource efficiency
- Leverage existing observability data
- Reduce risk of performance issues
- Achieve fast time to value
- Deploy recommendations automatically or with approval

## Setup

To set up this integration, you must have a StormForge account along with Datadog API and application keys.

### Configuration

1. Create a [Datadog API key][2].
2. Create a [Datadog application key][3].
3. Add Datadog API and application keys to the [StormForge Datadog Integration][4].
4. Deploy Optimize Live
5. Set up your Applications within [StormForge][5].

More detailed instructions can be found in the StormForge [getting started guide][6].

## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this integration.

### Events

The StormForge integration creates events for:
- Application updates
- Recommendations that have been applied

### Service Checks

The StormForge integration does not include any service checks.

## Support

For questions or other support, you can contact StormForge via [email][8].

[1]: https://www.stormforge.io/how-stormforge-optimize-live-works/
[2]: https://docs.datadoghq.com/account_management/api-app-keys/#api-keys
[3]: https://docs.datadoghq.com/account_management/api-app-keys/#application-keys
[4]: https://docs.stormforge.io/optimize-live/install/#datadog-metrics
[5]: https://app.stormforge.io
[6]: https://docs.stormforge.io/optimize-live/
[7]: https://github.com/DataDog/integrations-extras/blob/master/stormforge/metadata.csv
