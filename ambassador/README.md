## Overview

Get metrics from [Ambassador](https://www.getambassador.io) in real time to:

* Visualize the performance of your microservices

* Understand the impact of new versions of your services as you use Ambassador to do a canary rollout

![snapshot](https://raw.githubusercontent.com/DataDog/integrations-extras/dhruv/ambassador/ambassador/Images/upstream-req-time.png)

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
           value: <your_api_key>
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

See [metadata.csv](https://github.com/DataDog/integrations-extras/blob/master/ambassador/metadata.csv) for a list of metrics provided by this integration.

### Events

The DataDog integration does not include any events at this time.

### Service Checks

The DataDog integration does not include any service checks at this time.

## Troubleshooting
Need help? Contact [Datadog Support](http://docs.datadoghq.com/help/).

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog](https://www.datadoghq.com/blog/).
