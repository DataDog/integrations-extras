## Overview

ngrok delivers instant ingress to your applications in any cloud, private network, or devices with authentication, load balancing, and other critical controls using our global points of presence.

The ngrok platform includes a Datadog event destination integration. With ngrok HTTP events, you can visualize valuable application insights using Datadog Log Management including HTTP status code breakdown, top client IPs and most requested resources. You can use the Datadog HTTPS logging endpoint to set up the integration on the [ngrok dashboard UI][2].



## Setup

To forward ngrok events for consumption into Datadog, you need to make two configurations.

- ngrok Event Subscription: Contains which events to be forwarded
- ngrok Event Destination: The configuration for where the events defined in the Event Subscription are forwarded to.

The following example demonstrates how to configure an Event Subscription with a Datadog Event Destination for HTTP request events. For step-by-step instructions, see the [ngrok Datadog Event Destination documentation][7].

**Step 1: Create a ngrok Event Subscription**

1. In the ngrok Dashboard Console, navigate to Events page.
2. Select "New Subscription".
3. Provide a Description for Subscription and select "Add Source".
4. From the list, select "http_request_complete.v0" and select Add Event Source.



**Step 2: Configure Event Destination properties**

The steps are performed within the previously created Event Subscription configuration:

1. Navigate to the "Event Destination" tab and select "Add Destination".
2. From the dropdown menu, select Datadog and input the correct information:
    a. Select the correct [Datadog site][10] for your data.\
    b. Navigate to Datadog and [create an API key][4] within the organization settings.\
    c. Copy the API key and paste into the API Key field.\
    d. Optionally, define a Service Name, this be added as a key to the event data as **service:value**.\
    e. Optionally, define DD Tags, these are `key:value` pairs to be added as Datadog tags to the event data.\
    f. Optional, define a description, this is locally significant and helps identify the Datadog Event Destination.
3. Select "Send Test Event".
4. If presented with a Success message, select "Done".  If an error is presented, validate that the Datadog site and API key are correct.


**Step 3: Create Datadog Log Facets**
Once logs begin to arrive, create [log facets][8] for data analysis and dashboard visualization. For more information about creating log facets, see the [Log Facets documentation][9]. 

Create facets for the following fields:

- event_type
- object.conn.server_name
- object.conn.client_ip
- object.http.response.status_code
- object.http.request.method
- object.http.request.url.path

## Troubleshooting

Need help? Contact [ngrok Support][1] or reference the [ngrok documentation][6].

## Further Reading

Learn more about [ngrok][3].

[1]: mailto:support@ngrok.com
[2]: https://dashboard.ngrok.com
[3]: https://ngrok.com/solutions
[4]: https://docs.datadoghq.com/account_management/api-app-keys/
[6]: https://ngrok.com/docs/integrations/datadog/
[7]: https://ngrok.com/docs/integrations/datadog/event-destination/
[8]: https://docs.datadoghq.com/logs/explorer/facets/
[9]: https://docs.datadoghq.com/logs/explorer/facets/#create-facets
[10]: https://docs.datadoghq.com/getting_started/site/
