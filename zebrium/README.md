# Zebrium Root Cause as a Service
 
## Overview
 
When you know there's a problem and you're not sure what caused it, [Zebrium][1] shows you the root cause directly on your Datadog dashboards. It works by using machine learning on logs, without the need for manual training or setting up any rules, and it achieves accuracy in less than 24 hours. 

Using Zebrium is simple. When troubleshooting a problem, simply add the Zebrium app to your Datadog dashboard and look at the details of the corresponding detection.

Zebrium integrates with Datadog in two ways: 1) a Datadog App with a custom dashboard widget and 2) an events and metrics integration.

### 1) Datadog App

The Zebrium app provides a pre-built, interactive dashboard widget that displays the detected problems over time, and allows you to dig into the Root Cause of these problems (as well as relevant metrics). This method provides the simplest user experience.
 
### 2) Events and metrics integration

With the integration, Zebrium detection events and metrics are sent directly into Datadog. You can visualize them any way you'd like (sample dashboard provided). This method should be used if you would like to customize how Zebrium data appears on your dashboards.

## Setup
 
### Events and metrics integration

The Zebrium events and metrics integration uses a [Datadog API key][2], which needs to be created by a Datadog admin. Once you obtain a Datadog API key, see the [Zebrium documentation for Datadog integration][3] to learn how to setup the Zebrium events and metrics integration for Datadog.

### Dashboard widget

1. Click **Install Integration** in the top right of this panel.
2. Navigate to an existing Datadog dashboard or create a new one.
3. Press the **Add Widgets** button to expose the widget drawer.
4. Search for **Zebrium** in the **Apps** section of the widget drawer.
5. Click or drag the ***Zebrium Root Cause Finder*** widget icon to add it to your Datadog dashboard.
6. Open the [Zebrium UI][5] in a new browser tab and  create an access token for your deployment. 
   - Select the hamburger menu in the upper right of the Zebrium UI and choose Access Tokens. 
   - Click the Add Access Token button, provide a name for the token, select the deployment for the token and set role to viewer. 
   - Click Add and copy the token to your clipboard. 
7. In the widget editor in the Datadog UI, enter the following information:
   - **API Endpoint**: this is the absolute URL to the root of your Zebrium instance. It is normally **https://cloud.zebrium.com**.
   - **Token**: Paste the token that you created in step 6 above.
   - **Service Group**: The name of the service group you wish to show data from. Or enter 'All' to show data from all service groups in this deployment. 
9. Optionally give the widget a title.
10. Press **Save** to finish configuring the Datadog dashboard widget.
 
## Support
 
Need help? Contact [Datadog Support][4].

## Further reading

Additional helpful documentation, links, and articles:

- [Find the root cause faster with Datadog and Zebrium][6]

[1]: https://www.zebrium.com
[2]: https://app.datadoghq.com/organization-settings/api-keys
[3]: https://docs.zebrium.com/docs/monitoring/datadog_autodetect/
[4]: http://docs.datadoghq.com/help
[5]: https://cloud.zebrium.com
[6]: https://www.datadoghq.com/blog/find-the-root-cause-faster-with-zebrium/
