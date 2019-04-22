## Overview

Get metrics from [Ambassador][1] in real time to:

* Visualize the performance of your microservices

* Understand the impact of new versions of your services as you use Ambassador to do a canary rollout

![snapshot][2]

## Setup

By default, Ambassador installs a `statsd` sidecar on its pod. This sidecar forwards `statsd` metric to any Kubernetes service named `statsd-sink`.

1. Create a file `datadog-statsd-sink.yaml` with the following configuration, replacing the API key below with your own API key:

    ```
    ---
    apiVersion: extensions/v1beta1
    kind: Deployment
    metadata:
     name: statsd-sink
    spec:
     replicas: 1
     template:
       metadata:
         labels:
           service: statsd-sink
       spec:
         containers:
         - name: statsd-sink
           image: datadog/docker-dd-agent:latest
           ports:
             - containerPort: 8125
               name: dogstatsdport
               protocol: UDP
           env:
             - name: API_KEY
               value: "<YOUR_DATADOG_API_KEY>"
             - name: KUBERNETES
               value: "yes"
             - name: SD_BACKEND
               value: docker
         restartPolicy: Always
    status: {}
    ---
    apiVersion: v1
    kind: Service
    metadata:
     labels:
       service: statsd-sink
     name: statsd-sink
    spec:
     ports:
        - protocol: UDP
          port: 8125
          name: dogstatsdport
     selector:
       service: statsd-sink
    ```

2. Deploy the agent to Kubernetes:

    ```
    kubectl apply -f datadog-statsd-sink.yaml
    ```

3. As soon as some traffic flows through Ambassador, your metrics should appear.

## Data Collected

### Metrics

See [metadata.csv][3] for a list of metrics provided by this check.

### Events

The Ambassador check does not include any events.

### Service Checks

The Ambassador check does not include any service checks.

## Troubleshooting
Need help? Contact [Datadog support][4].

[1]: https://www.getambassador.io
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/ambassador/images/upstream-req-time.png
[3]: https://github.com/DataDog/integrations-extras/blob/master/ambassador/metadata.csv
[4]: http://docs.datadoghq.com/help/
