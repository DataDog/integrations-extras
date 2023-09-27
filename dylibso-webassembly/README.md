# Dylibso WebAssembly Observe SDK

## Overview

This integration provides function traces from WebAssembly (WASM) code running in your application. Gain insight into WebAssembly code performance as well as the following behavior:
- Function call duration
- Execution tracing
- Memory allocation

Since WebAssembly code is executed in a secure and constrained environment, traditional techniques to monitor code do not work. Our specialized observability stack allows you to continuously monitor WASM modules at the same level you expect of your other applications.

Datadog customers can use our open source SDKs and Adapters to emit full traces from your WASM programs. Please see the [`dylibso/observe-sdk`][2] repository to install the Datadog Adapter for your application.

In addition, Dylibso provides automatic instrumentation tooling which can take any existing WASM module and recompile it to include function and memory allocation tracing. For more information, contact [support@dylibso.com](mailto:support@dylibso.com) or learn more about [automatic WebAssembly instrumentation][3].


## Setup

### Installation

Depending on the programming language your application is written in, choose one of the appropriate Datadog Adapters from [`dylibso/observe-sdk`][2] on GitHub.


### Configuration

In order to connect the SDK and Adapter to your Datadog Agent, you must have the following information ready:

1. Your Datadog Agent host URL.
2. The service name of the application where the SDK and Adapter are imported.

### Validation

After you have imported and configured your Datadog Adapter from the available options within the Observe SDK:

1. Redeploy your application so the Datadog Adapter is included where you're calling WebAssembly code.
2. Ensure that a WebAssembly module (`.wasm`) has been loaded and you are calling one of its exported functions.
3. Check in your Datadog dashboard for traces sent from your service.

## Data Collected

### Events

WebAssembly Observe SDK collects traces of function execution and memory allocation events from your application.

## Troubleshooting

Need help? Contact [Dylibso support][1].

[1]: mailto:support@dylibso.com
[2]: https://github.com/dylibso/observe-sdk
[3]: https://dylibso.com/products/observe
