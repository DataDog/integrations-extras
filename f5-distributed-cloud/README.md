## Overview

F5 Distributed Cloud (XC) Services provides customers with a global cloud native platform that can deploy, manage, and secure their applications in hybrid environments (public cloud, private data centers, or colocations). ADN and CDN services are also available. 

The F5 XC platform includes the Global Log Receiver. F5 XC global log receiver can be configured to securely send logs to a Datadog HTTPS logging endpoint. Configuration can be done via the [F5 XC Console UI][6].


The F5 Distributed Cloud Services integration includes:

- Dashboard - *Access Log Overview*
- Saved View - *Including facets for commonly queried fields*

## Setup

You can configure global log streaming in either system namespace or in shared namespace. In case of configuring in shared namespace, you can configure to stream from either shared namespace or all namespaces or specific list of namespaces. If you are configuring in system namespace, you can only stream logs from system namespace.

The example shown in this guide creates a global log receiver object in the Console in system namespace for streaming the logs to the external log collection system.

Perform the following in the F5® Distributed Cloud Console:

**Step 1: Start creating a global log receiver**

- In the Console home page, select Shared Configuration service.
- Select Manage > Global Log Receiver.
- Select Global Log Receiver in case of Cloud and Edge Sites service.

![snapshot][3]

- Select Add Global Log Receiver button.

**Step 2: Configure global log receiver properties**
Do the following in the Global Log Receiver section:

- Enter a name in the metadata section. Optionally, set labels and add a description.
- Select Request Logs or Security Events for the Log Type field. The request logs are set by default.
- Select events to be streamed based on namespace from the following options:
    - Select logs from current namespace - streams logs from the shared namespace.
    - Select logs from all namespaces - streams logs from all namespaces.
    - Select logs in specific namespaces - streams logs from specified namespaces. Enter the namespace name in the displayed namespaces list. Use Add item button to add more than one namespace.  Namespaces provide logical grouping and isolation of objects within a distributed cloud tenant.
- Select Datadog for the Receiver Configuration box. Configure following for the Datadog receiver:
    - Provide the appropriate data Doc site name, (datadoghq.com) in this case.   
    - Provide a Datadog API key.

![snapshot][4]

**Step 3: Optionally, configure advanced settings**
Advanced settings include configuring batch options and TLS. Using batch options, you can apply limits such as maximum number of messages bytes or timeout for a batch of logs to be sent to the receiver.

- Select Show Advanced Fields toggle and do the following in the Batch Options section:
    - Select Timeout Seconds for the Batch Timeout Options and enter a timeout value in the Timeout Seconds box.
    - Select Max Events for the Batch Max Events and enter a value between 32 and 2000 in the Max Events box.
    - Select Max Bytes for the Batch Bytes and enter a value between 4096 and 1048576 in the Batch Bytes box. Logs will be sent after the batch is size is equal to or more than the specified byte size.

Do the following for TLS section:

- Select Use TLS for the TLS field.
- Select Server CA Certificates for the Trusted CA field. Enter the certificates in PEM or Base64 format in the Server CA Certificates box.
- Select Enable mTLS for mTLS config and enter client certificate in PEM or Base64 format in the Client Certificate box.
    - Select Configure in the Client Private Key field, enter the secret in the box with type selected as Text.
    - Select Blindfold, wait for the operation to complete, and click Apply.

**Step 4: Complete log receiver creation**

- Select Save & Exit to complete creating the global log receiver. Verify that logs are received into your Datadog account.

## Data Collected

### Metrics

The F5 Distributed Cloud Services integration does not include any metrics at this time.

### Events

The F5 Distributed Cloud Services integration does not include any events at this time.

### Service Checks

The F5 Distributed Cloud Services integration does not include any service checks at this time.

## Troubleshooting

Need help? Contact [Datadog Support][5].

## Further Reading

Learn more about [F5 Distributed Cloud Services][7].

[3]: images/image-0.png
[4]: images/logreceiver-config.png
[5]: http://docs.datadoghq.com/help/
[6]: https://www.f5.com/cloud/products/distributed-cloud-console
[7]: https://www.f5.com/cloud
