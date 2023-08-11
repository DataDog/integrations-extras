# Dylibso WebAssembly Observe SDK

## Overview

This integration provides traces, logs, and metrics from WebAssembly code running in your application.

There are open-source SDKs avaiable to integrate into your application, which emit telemtry data into your Datadog Agent.

Please see the [`dylibso/observe-sdk`](https://github.com/dylibso/observe-sdk) repository to install the Datadog Adapter for you application.

## Setup

### Installation

Depending on the programming language your application is written in, you should choose one of the appropriate Datadog Adapters from:

 [`dylibso/observe-sdk`](https://github.com/dylibso/observe-sdk) on GitHub

### Configuration

In order to connect the SDK and Adapter to your Datadog Agent, you must have the following information ready:

1. Your Datadog Agent host URL
2. The service name of the application where the SDK & Adapter are imported

### Validation

Once you have imported and configured your Datadog Adapter from the available options within the Observe SDK:

1. Redeploy your application so the Datadog Adapter is included where you're calling WebAssembly code.
2. Ensure that a WebAssembly module (.wasm) has been loaded and you are calling one of its exported functions.
3. Check in your Datadog dashboard for a trace, log, or metric sent from your service.

## Data Collected

### Metrics

WebAssembly Observe SDK can emit standard and custom metrics from your application, depending on your needs.

### Service Checks

WebAssembly Observe SDK does not include any service checks.

### Events

WebAssembly Observe SDK collects logs and traces from your application.

## Troubleshooting

Need help? Contact [Datadog support][1].

[1]: https://docs.datadoghq.com/help/

