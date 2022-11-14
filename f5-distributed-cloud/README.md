## Overview

F5 Distributed Cloud (XC) Services provides customers with a global cloud native platform that can deploy, manage, and secure their applications in hybrid environments (public cloud, private data centers, or colocations). ADN and CDN services are also available. 

The F5 XC platform includes the Global Log Receiver, which can be configured to securely send logs to a Datadog HTTPS logging endpoint. Configuration can be done via the [F5 XC Console UI][2].


This integration includes:

- Dashboard - *Access Log Overview*
- Saved View - *Including facets for commonly queried fields*

## Setup

Global log streaming is available for either system namespace or in shared namespace:
- Shared Namespaces support streaming logs from all shared namespaces in your account, or a specific list of shared namespaces that you can specify.
- System Namespaces only support streaming logs from system namespaces.

Below is an example of configuring a global log receiver in a system namespace. For a step-by-step video, see the [Configuring Remote Logging to Datadog official Datadog Youtube instructions][7].

**Step 1: To create a global log receiver**

1. In the F5® Distributed Cloud Console, navigate to the Shared Configuration service.
2. Select Manage > Global Log Receiver.
3. Select Global Log Receiver in case of Cloud and Edge Sites service.
4. Click add Global Log Receiver button



**Step 2: Configure global log receiver properties**
Do the following in the Global Log Receiver section:

1. Within the Global Log Receiver section, enter a name in the metadata section. Optional: set labels and add a description.
2. Select Request Logs or Security Events for the Log Type field. Note: Request logs are set by default.
3. Select events to be streamed based on namespace from the following options:
	a. Select logs from the current namespace - streams logs from the shared namespace.
	3.b Select logs from all namespaces - streams logs from all namespaces.
	3.c Select logs in specific namespaces - streams logs from specified namespaces. Enter the namespace name in the displayed namespaces list. To add more than one namespace, select Add item. Note: Namespaces provide logical grouping and isolation of objects within a distributed cloud tenant.
4. Select Datadog for the Receiver Configuration box. Configure the following for the Datadog receiver:
 	4.a Set the site name to datadoghq.com.
	4.b Navigate to Datadog and [create an API key][4] within the organization settings. 
	4.c Copy the API key
	4.d Navigate back to F5 and paste in the Datadog API key in the Datadog receiver fields.

**Optional Step 3: Configure advanced settings**
Advanced settings include configuring batch options and TLS. You can apply limits such as maximum number of messages bytes or timeout for a batch of logs to be sent to the receiver.

1. Select the Show Advanced Fields toggle
2. Within the Batch Options section:
	 2.a Select Timeout Seconds for the Batch Timeout Options and enter a timeout value in the Timeout Seconds box.
	 2.b Select Max Events for the Batch Max Events and enter a value between 32 and 2000 in the Max Events box.
	 2.c Select Max Bytes for the Batch Bytes and enter a value between 4096 and 1048576 in the Batch Bytes box. Logs will be sent after the batch is size is equal to or more than the specified byte size.
3. Within the TLS section:
	 3.a Select Use TLS for the TLS field.
	 3.b Select Server CA Certificates for the Trusted CA field. Enter the certificates in PEM or Base64 format in the Server CA Certificates box.
	 3.c Select Enable mTLS for mTLS config and enter client certificate in PEM or Base64 format in the Client Certificate box.
	 3.d Select Configure in the Client Private Key field, enter the secret in the box with type selected as Text.
	 3.e Select Blindfold, wait for the operation to complete, and click Apply.

**Step 4: Finish set up**

- Select Save & Exit to complete creating the global log receiver. Verify that [logs][5] are received into your Datadog account.


## Troubleshooting

Need help? Contact [Datadog Support][1] or [F5 Support][6].

## Further Reading

Learn more about [F5 Distributed Cloud Services][3].

[1]: http://docs.datadoghq.com/help/
[2]: https://www.f5.com/cloud/products/distributed-cloud-console
[3]: https://www.f5.com/cloud
[4]: https://docs.datadoghq.com/account_management/api-app-keys/
[5]: https://app.datadoghq.com/logs
[6]: https://docs.cloud.f5.com/docs/support/support
[7]: https://youtu.be/VUtXCUngiw8
