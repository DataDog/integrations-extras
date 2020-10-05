# Algorithmia Integration

## Overview

[Algorithmia][1] is an MLOps platform that includes capabilities for data
scientists, application developers, and IT operators to deploy, manage, govern,
and secure machine learning and other probabilistic models in production.

Algorithmia Insights is a feature of Algorithmia Enterprise and provides a
metrics pipeline that can be used to instrument, measure, and monitor your
machine learning models.

This integration allows you to stream operational metrics as well as
user-defined, inference-related metrics from Algorithmia to the metrics API in
Datadog.

## Setup

1. From your Algorithmia instance, configure Algorithmia Insights to connect to
   a Kafka broker.
2. Install and configure [Kafka Connect][2].
3. Install the [Datadog Kafka Connector][3].
4. Configure a Kafka Connect properties file in
   `<KAFKA-DIR>/config/connect-datadog-sink.properties` with the following
   contents:

   ```
   name=datadog-sink
   connector.class=com.datadoghq.connect.logs.DatadogLogsSinkConnector
   tasks.max=1
   key.converter=org.apache.kafka.connect.storage.StringConverter
   value.converter=org.apache.kafka.connect.json.JsonConverter
   value.converter.schemas.enable=false
   topics=insights
   datadog.api_key=<DATADOG-API-KEY>
   datadog.service=algorithmia-insights
   datadog.hostname=algorithmia-host
   datadog.tags=type:json
   ```

   and replace `<KAFKA-DIR>` with the directory where Kafka is installed and
   `<DATADOG-API-KEY>` with your Datadog API key.

5. Start the Kafka Connect service and include the properties file for the
   Datadog Kafka Connector as an argument:

   ```
   <KAFKA-DIR>/bin/connect-standalone.sh <KAFKA-DIR>/config/connect-standalone.properties <KAFKA-DIR>/config/connect-datadog-sink.properties
   ```

### Validation

1. From Algorithmia, query an algorithm that has Insights enabled.
2. In the Datadog interface, navigate to the **Logs** page.
3. Verify that the metrics are being pushed to the logs by filtering for
   `algorithmia-insights`.
4. Refer to the [Datadog documentation][4] to generate metrics from the ingested
   logs.

## Data Collected

### Metrics

This integration streams metrics from Algorithmia when an model that has
Insights enabled is queried. Each log entry includes operational metrics and
inference-related metrics.

Refer to [metadata.csv][5] for a list of operational metrics provided by this
check. Additional metrics can include any user-defined, inference-related
metrics that are specified by the algorithm developer.

### Service Checks

The Algorithmia check does not include any service checks.

### Events

The Algorithmia check does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][6].

[1]: https://algorithmia.com/
[2]: https://docs.confluent.io/current/connect/index.html
[3]: https://github.com/DataDog/datadog-kafka-connect-logs
[4]: https://docs.datadoghq.com/logs/logs_to_metrics/
[5]: https://github.com/DataDog/integrations-extras/blob/master/algorithmia/metadata.csv
[6]: https://docs.datadoghq.com/help/
