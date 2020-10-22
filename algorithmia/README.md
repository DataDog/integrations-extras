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
2. Install Python if it's not already present on your system.
3. Install the required Python dependencies using
   ```
   pip install -r requirements.txt
   ```
4. Define the following environment variables (required):
   ```
   export DATADOG_API_KEY=<DATADOG-API-KEY>
   export KAFKA_BROKER=1.2.3.4:9092
   export KAFKA_TOPIC=insights
   ```
   and replace the values with your Datadog API key, Kafka broker URL and port,
   and Kafka topic that you want to consume Insights from.
5. Run the Python script, which will continuously forward messages from Kafka to
   the Datadog metrics API:
   ```
   python src/kafka-datadog.py
   ```

### Validation

1. From Algorithmia, query an algorithm that has Insights enabled.
2. In the Datadog interface, navigate to the **Metrics** summary page.
3. Verify that the metrics from Insights are present in Datadog by filtering for
   `algorithmia`.

## Data Collected

### Metrics

This integration streams metrics from Algorithmia when an model that has
Insights enabled is queried. Each log entry includes operational metrics and
inference-related metrics.

See [metadata.csv][3] for a list of metrics provided by this integration.

The `duration_milliseconds` metric is one of the operational metrics that is
included in the default payload from Algorithmia. To help you get started, this
integration also includes a dashboard and monitor for this default metric.

Additional metrics can include any user-defined, inference-related metrics that
are specified in Algorithmia by the algorithm developer. User-defined metrics
will depend on your specific machine learning framework and use case, but might
include values such as prediction probabilities from a regression model in
scikit-learn, confidence scores from an image classifier in TensorFlow, or input
data from incoming API requests.

### Service Checks

The Algorithmia check does not include any service checks.

### Events

The Algorithmia check does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][4].

[1]: https://algorithmia.com/
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/algorithmia/images/algorithmia-insights-datadog.png
[3]: https://github.com/DataDog/integrations-extras/blob/master/algorithmia/metadata.csv
[4]: https://docs.datadoghq.com/help/
