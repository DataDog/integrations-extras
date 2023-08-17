# Dylibso WebAssembly Observe SDK

## Overview

This integration provides function traces from WebAssembly code running in your application. Gain insights into WebAssembly code performance and behavior
including function call duration, execution tracing, and memory allocation.

Since WebAssembly code is executed in a secure & constrained environment, traditional techniques to monitor code do not work. Our specialized observability stack
makes it easy to continuously monitor WASM modules at the same level you expect of your other applications.

Datadog customers can use our open source SDKs and Adapters to emit full traces from their WASM programs.

Please see the [`dylibso/observe-sdk`][2] repository to install the Datadog Adapter for you application.

In addition, Dylibso provides automatic instrumention tooling which can take any existing WASM module and losslessly recompile it to include function and memory allocation tracing. For
more information, contact [support@dylibso.com](mailto:support@dylibso.com) or learn more about [automatic WebAssembly instrumentation](https://dylibso.com/products/observe).


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
3. Check in your Datadog dashboard for traces sent from your service.

## Data Collected

### Events

WebAssembly Observe SDK collects logs and traces from your application.

## Troubleshooting

Need help? Contact [Dylibso support][1].

[1]: mailto:support@dylibso.com
[2]: https://github.com/dylibso/observe-sdk
