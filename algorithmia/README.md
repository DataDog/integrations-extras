# Algorithmia Integration

## Overview

[Algorithmia][1] is an MLOps platform that includes capabilities for data
scientists, application developers, and IT operators to deploy, manage, govern,
and secure machine learning and other probabilistic models in production.

![Algorithmia Insights in Datadog][2]

Algorithmia Insights is a feature of Algorithmia Enterprise and provides a
metrics pipeline that can be used to instrument, measure, and monitor your
machine learning models. Use cases for monitoring inference-related metrics from
machine learning models include detecting model drift, data drift, model bias,
etc.

This integration allows you to stream operational metrics as well as
user-defined, inference-related metrics from Algorithmia to Kafka to the metrics
API in Datadog.

## Setup

1. From your Algorithmia instance, configure Algorithmia Insights to connect to
   a Kafka broker (external to Algorithmia).

2. See the [Algorithmia Integrations repository][3]
   to install, configure, and start the Datadog message forwarding service used
   in this integration, which forwards metrics from a Kafka topic to the
   metrics API in Datadog.


### Validation

1. From Algorithmia, query an algorithm that has Insights enabled.
2. In the Datadog interface, navigate to the **Metrics** summary page.
3. Verify that the metrics from Insights are present in Datadog by filtering for
   `algorithmia`.
   
### Streaming metrics

This integration streams metrics from Algorithmia when a model that has Insights
enabled is queried. Each log entry includes operational metrics and
inference-related metrics.

The `duration_milliseconds` metric is one of the operational metrics that is
included in the default payload from Algorithmia. To help you get started, this
integration also includes a dashboard and monitor for this default metric.

Additional metrics can include any user-defined, inference-related metrics that
are specified in Algorithmia by the algorithm developer. User-defined metrics
depend on your specific machine learning framework and use case, but might
include values such as prediction probabilities from a regression model in
scikit-learn, confidence scores from an image classifier in TensorFlow, or input
data from incoming API requests. **Note**: The message forwarding script
provided in this integration prefixes user-defined metrics with
`algorithmia.` in Datadog.

## Data Collected

### Metrics

See [metadata.csv][4] for a list of metrics provided by this integration.

### Service Checks

The Algorithmia check does not include any service checks.

### Events

The Algorithmia check does not include any events.

## Troubleshooting

Need help? Contact [Algorithmia support][5].

[1]: https://algorithmia.com/
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/algorithmia/images/algorithmia-insights-datadog.png
[3]: https://github.com/algorithmiaio/integrations
[4]: https://github.com/DataDog/integrations-extras/blob/master/algorithmia/metadata.csv
[5]: https://algorithmia.com/contact
