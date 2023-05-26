## Overview

ngrok delivers instant ingress to your applications in any cloud, private network, or devices with authentication, load balancing, and other critical controls via our global points of presence.

The ngrok platform includes a Datadog event destination integration.  When used in conjunction with ngrok HTTP events the visualization of valuable application insights is made possible.  Using the the Datadog HTTPS logging endpoint, the integration can quickly be setup through the [ngrok dashboard UI][2].


This integration includes:

- Dashboard - *ngrok HTTP Events*


## Setup

To forward ngrok events for consumption into Datadog there are two configurations to be made.

- ngrok Event Subscription: contains which events to be forwarded
- ngrok Event Destination: the configuration for where the events defined in the Event Subscription will be forwarded to.

Below is an example of configuring an Event Subscription with a Datadog Event Destination for HTTP request events. For step-by-step instructions, see the [ngrok Datadog Event Destination documentation page][7].

**Step 1: Create a ngrok Event Subscription**

1. In the ngrok Dashboard Console, navigate to Events page.
2. Select "New Subscription".
3. Provide a Description for Subscription and select "Add Source"
4. From the list, select "http_request_complete.v0" and select Add Event Source.



**Step 2: Configure Event Destination properties**

The steps are performed within the previously created Event Subscription configuration:

1. Navigate to the "Event Destination" tab and select "Add Destination".
2. From the dropdown choose Datadog and input the correct information:\
    a. Select the correct Datadog Site for your data - this can be found based upon the [url used to access Datadog][10].\
    b. Navigate to Datadog and [create an API key][4] within the organization settings.\
    c. Copy the API key and paste into the API Key field.\
    d. Optional:  Define a Service Name, this be added as a key to the event data as **service:value**.\
    e. Optional:  Define DD Tags, these are key:value pairs to be added as Datadog tags to the event data.\
    f. Optional:  Define a description, this is locally significant and helps identify the Datadog Event Destination.
3. Select "Send Test Event"
4. If presented with a Success message, select "Done".  If an error is presented validate the Datadog Site and API Key are correct.


**Step 3: Create Datadog Log Facets**
Once logs begin to arrive, it will be necessary to create [log facets][8] for data analysis and dashboard visualization. Log facet creation is straight forward and can be accomplished from the Datadog log side panel with guidance available [here][9]. 

Create facets for the following fields:

- event_type
- object.conn.server_name
- object.conn.client_ip
- object.conn.server_name
- object.http.response.status_code
- object.http.request.method
- object.http.request.url.path
- object.conn.server_name

## Troubleshooting

Need help? Contact [Datadog Support][1] or [ngrok Docs][6].

## Further Reading

Learn more about [ngrok][3].

[1]: http://docs.datadoghq.com/help/
[2]: https://dashboard.ngrok.com
[3]: https://ngrok.com/solutions
[4]: https://docs.datadoghq.com/account_management/api-app-keys/
[6]: https://ngrok.com/docs/integrations/datadog/event-destination/
[7]: https://ngrok.com/docs/integrations/datadog/event-destination/
[8]: https://docs.datadoghq.com/logs/explorer/facets/
[9]: https://docs.datadoghq.com/logs/explorer/facets/#create-facets
[10]: https://docs.datadoghq.com/getting_started/site/
