## Overview

Rigor provides synthetic monitoring and optimization insights throughout your development lifecycle.

![timeboard][1]

With Rigor, you can collect synthetic, front-end performance metrics and push those metrics into Datadog. You can also push alerts into Datadog as events.

## Setup

Rigor has two different integrations with Datadog, a metrics integration and an events integration.

### Configuration
#### Metrics collection

As an administrator, click the "Admin Tools" menu in the upper right hand of your screen and select "Integrations".

![admin-menu][2]

Add a new integration, by clicking the "New" button. You will now be able to configure the integration.

![push-configuration][3]

Add a unique name for this integration and your API key from Datadog. Then choose which tags and metrics you want to send. Some things to remember:

- We include a normalized version of the check name as a default tag
- For multi-step checks (Real Browser and API Checks), we include the position of the
  request that the metrics came from
- Uptime checks include HTTP, Port, and API checks
- Port checks only report the "Response Time" metric
- Not all browsers support all metrics

If you would like Real Browser Checks to report timings from the [User Timings API][4], make sure "Send All User Timings?" is selected. Any marks are reported under the `rigor.real_browser.marks` namespace and measures are reported under the `rigor.real_browser.measures` namespace. Be aware that selecting this option could send a lot of new series into Datadog, especially if the marks and measures on the site you are testing are dynamically generated.

Once you have configured the integration. You can add to any Real Browser, HTTP, Port, or API check. Just edit the check and go to the "Notifications" tab. Here you can add the integration that you just created.

![add-integration-to-check][5]

#### Events collection

As an administrator, click the "Admin Tools" menu in the upper right hand of your screen and select "Alert Webhooks".

![webhook-menu][6]

Add a new integration, by clicking the "New" button and clicking the Datadog tile.

![webhooks-chooser][7]

Add a unique name for this webhook and make sure to update the triggers with your Datadog API key.

![webhooks-configuration][8]

Once you have configured the integration. You can add to any Real Browser, HTTP, Port, or API check. Just edit the check and go to the "Notifications" tab. Here you can add the webhook that you just created.

![add-webhookto-check][9]

## Data Collected

### Metrics

Any of Rigor's metrics can be sent to Datadog. The metrics that are actually sent depend on how the integration was configured. The possible metrics are:

#### HTTP checks

- `rigor.http.dns_time`
- `rigor.http.first_byte_time`
- `rigor.http.response_time`

#### Port checks

- `rigor.port.response_time`

#### API checks

- `rigor.api.dns_time`
- `rigor.api.first_byte_time`
- `rigor.api.response_time`

#### Real browser checks

- `rigor.real_browser.first_byte_time_ms`
- `rigor.real_browser.dom_interactive_time_ms`
- `rigor.real_browser.first_paint_time_ms`
- `rigor.real_browser.start_render_ms`
- `rigor.real_browser.first_contentful_paint_time_ms`
- `rigor.real_browser.first_meaningful_paint_time_ms`
- `rigor.real_browser.dom_load_time_ms`
- `rigor.real_browser.dom_complete_time_ms`
- `rigor.real_browser.onload_time_ms`
- `rigor.real_browser.visually_complete_ms`
- `rigor.real_browser.speed_index`
- `rigor.real_browser.fully_loaded_time_ms`
- `rigor.real_browser.requests`
- `rigor.real_browser.content_bytes`
- `rigor.real_browser.html_files`
- `rigor.real_browser.html_bytes`
- `rigor.real_browser.image_files`
- `rigor.real_browser.image_bytes`
- `rigor.real_browser.javascript_files`
- `rigor.real_browser.javascript_bytes`
- `rigor.real_browser.css_files`
- `rigor.real_browser.css_bytes`
- `rigor.real_browser.video_files`
- `rigor.real_browser.video_bytes`
- `rigor.real_browser.font_files`
- `rigor.real_browser.font_bytes`
- `rigor.real_browser.other_files`
- `rigor.real_browser.other_bytes`
- `rigor.real_browser.client_errors`
- `rigor.real_browser.connection_errors`
- `rigor.real_browser.server_errors`
- `rigor.real_browser.errors`

Additionally, if the integration is configured, browser User Timings will be sent under the `rigor.real_browser.marks` and `rigor.real_browser.measures` namespaces.

See [metadata.csv][13] for a list of metrics provided by this integration.

### Events

When a check is configured to alert via a Datadog event, 2 events types will be pushed into Datadog:

- **Failed** - whenever the check fails enough to pass the threshold so that it sends an alert
- **Back online** - whenever the check successfully runs while in an alerting state

![events-example][10]

### Service Checks

This integration does not include any service checks.

### Troubleshooting

Need help? Contact [Rigor Support][11].

### Further Reading

Learn more about Rigor and how we can help make your website faster, visit [rigor][12].

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/rigor/images/rigor_timeboard_with_metrics.png
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/rigor/images/rigor_admin_menu.png
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/rigor/images/rigor_integration_configuration.png
[4]: https://developer.mozilla.org/en-US/docs/Web/API/User_Timing_API
[5]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/rigor/images/rigor_add_integration_to_check.png
[6]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/rigor/images/rigor_webhooks_menu.png
[7]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/rigor/images/rigor_webhooks_chooser.png
[8]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/rigor/images/rigor_webhooks_configuration.png
[9]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/rigor/images/rigor_add_webhook_to_check.png
[10]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/rigor/images/rigor_events_example.png
[11]: mailto:support@rigor.com
[12]: https://rigor.com
[13]: https://github.com/DataDog/integrations-core/blob/master/rigor/metadata.csv
