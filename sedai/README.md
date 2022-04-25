## Overview

Sedai is an autonomous cloud platform that proactively manages production environments to prevent issues and improve availability, performance, and cloud costs. As an intelligent autopilot for SREs, Sedai independently detects, prioritizes, and analyzes monitoring data to safely and autonomously act in production without thresholds.

Enable this integration to receive notifications in Datadog about actions that Sedai autonomously executes in your production environments.

### How it Works

* **Agentless:** Seamlessly connects to your cloud accounts and automatically discovers and understands production environments.

* **Configuration-free:** Easily connects to Datadog API and other APM/Observability platforms, and intelligently identifies, prioritizes and learns metric behavior.

* **Proactive Actions:** Safely acts in production on your behalf to ensure that resources avoid availability issues and run optimally at all times.

## Setup

In Sedai:

* Navigate to Settings > Notifications > Add Integration > Datadog Icon 
![DataDog Notification Integration](https://raw.githubusercontent.com/DataDog/integrations-extras/master/sedai/images/DataDog_Notification_Integration.png)

* Enter a nickname and the API Key for your Datadog account, enable it and test the integration.
![DataDog Notification Integration](https://raw.githubusercontent.com/DataDog/integrations-extras/master/sedai/images/Add_DataDog_Channel.png)

* Once the test is verified to be working, click Save.
![Working DataDog Integration](https://raw.githubusercontent.com/DataDog/integrations-extras/master/sedai/images/Add_DataDog_Channel-Working_REC.png)

* Under Settings > Notifications, [select which notifications][2] you want to send to Datadog. 
![Enable DataDog Notifications](https://raw.githubusercontent.com/DataDog/integrations-extras/master/sedai/images/Enable_Notifications.png)

## Data Collected

This integration sends events into Datadog.

## Support

For help with this integration, please email [support@sedai.io][1].


[1]: mailto:support@sedai.io
[2]: https://sedai.gitbook.io/sedai/sedai-user-guide/controls/notifications

