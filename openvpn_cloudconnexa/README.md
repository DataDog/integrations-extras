## Overview

This is a dashboard for log events collected from your CloudConnexa® Wide-area Private Cloud (WPC). It provides a high-level view of collected log events such as connection activity, blocked traffic, and other logs.

CloudConnexa® is a cloud-delivered service that integrates virtual networking and critical security functions to create a secure overlay network to connect your applications, private networks, workforce, and IoT devices - without complex, hard-to-scale hardware. Your dedicated secure overlay network, called Wide-area Private Cloud (WPC), enables Zero Trust access to all applications and the internet and site-to-site networking while enforcing identity-based access control, preventing malicious network activity, and providing protection by blocking malicious website access.

## Setup

The steps to set the Dashboard:

1. Setup a log stream to DataDog.
    1. Configure the AWS S3 bucket for streaming logs. See the [Tutorial: Configure AWS S3 bucket for CloudConnexa Log Streaming][1]
    2. Configure Log Streaming within CloudConnexa. See the [Tutorial: Configure DataDog for CloudConnexa Log Streaming][2]
    3. Select the categories of logs you want to have in the DataDog. We recommend enabling at least **Logins of Devices and Connectors**, **Cyber Shield Blocked Domains**, and **Cyber Shield Blocked Traffic**.
2. Install this Dashboard.
3. Customize the Dashboard according to your needs.
    1. You can access the specific event by clicking the **event on the chart** > expand **More Related Data Action** > **View Related Logs**.
    2. Customize access permissions according to the company policies.
4. Navigate to the **CloudConnexa Logs Stats** dashboards to check the events that were received.

## Data Collected

Using **CloudConnexa Log Streaming**, you can forward different sets of logs to the DataDog:
1. Logins of Devices and Connectors.
2. Cyber Shield Blocked Domains
3. Cyber Shield Blocked Traffic.
4. Traffic flows inside the private network identified by Access Visibility.

More categories are going to be added over time.

## Support

The guide on the Log Streaming details and events is here [API & Logs - Log Streaming][3].

Details on the log messages sent over Log Streaming are here [Log Event Formats][4].

The troubleshooting guide is here [Tutorial: Troubleshooting Log Streaming][5].

In case support is required, create a request at [OpenVPN Support Center][6].

 

[1]: https://openvpn.net/cloud-docs/tutorials/configuration-tutorials/log-streaming/tutorial--configure-aws-s3-bucket-for-cloudconnexa-log-streaming.html
[2]: https://openvpn.net/cloud-docs/tutorials/configuration-tutorials/log-streaming/tutorial--configure-datadog-for-cloudconnexa-log-streaming.html 
[3]: https://openvpn.net/cloud-docs/owner/api---logs/api---logs---log-streaming.html 
[4]: https://openvpn.net/cloud-docs/owner/api---logs/api---logs---log-streaming/log-event-formats.html
[5]: https://openvpn.net/cloud-docs/tutorials/configuration-tutorials/log-streaming/tutorial--troubleshoot-log-streaming.html
[6]: https://support.openvpn.com/