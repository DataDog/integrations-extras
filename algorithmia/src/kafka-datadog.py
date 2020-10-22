import os
import json
import sys
from datadog import initialize, api
from kafka import KafkaConsumer

try:
    DATADOG_API_KEY = os.environ["DATADOG_API_KEY"]
except KeyError:
    sys.exit("Please define the DATADOG_API_KEY environment variable")

try:
    KAFKA_BROKER = os.environ["KAFKA_BROKER"]
except KeyError:
    sys.exit("Please define the KAFKA_BROKER environment variable")

try:
    KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]
except KeyError:
    sys.exit("Please define the KAFKA_TOPIC environment variable")

OPERATIONAL_METRICS = {"algorithm_version", "request_id", "time", "algorithm_name", "session_id", "algorithm_owner"}

options = {"api_key": DATADOG_API_KEY}
initialize(**options)

# Set up Kafka consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    value_deserializer=lambda m: json.loads(m.decode("ascii")),
)

# Consume data from Kafka topic
for msg in consumer:
    # Get JSON data from Algorithmia Insights
    insight = msg.value

    # Filter for inference metrics by removing known operational metrics
    inference_metrics = {key: insight[key] for key in insight.keys() ^ OPERATIONAL_METRICS}

    # Construct metrics payload
    metrics_payload = []
    for key, value in inference_metrics.items():
        metrics_payload.append(
            {
                "metric": "algorithmia." + key,
                "points": [insight["time"], value],
                "type": "gauge",
                "tags": [
                    "algorithm_name:" + insight["algorithm_name"],
                    "algorithm_version:" + insight["algorithm_version"],
                    "algorithm_owner:" + insight["algorithm_owner"],
                    "request_id:" + insight["request_id"],
                    "session_id:" + insight["session_id"],
                ],
            }
        )

    # Send metrics to Datadog
    api.Metric.send(metrics_payload)
