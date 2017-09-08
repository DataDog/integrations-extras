# Uptime.com

## Overview

Get events and metrics from your app in real time to

* Track and notify of any downtime or interruptions
* Visualize response time metrics from synthetic requests

![Uptime.com Graph](https://raw.githubusercontent.com/DataDog/integrations-extras/ilan/uptime/uptime/images/snapshot.png)

## Setup

### Configuration

In order to activate the integration of Datadog within your Uptime account, you will go to [Alerting>Push Notifications](https://uptime.com/push-notifications/manage/) then choose Datadog as the provider type when adding a new push notifications profile.

The following describes the fields shown when configuring Datadog within your Uptime account: 
<ul>
<li>**Name**: The reference name you desire to assign to your Datadog profile. It can assist you with organizing multiple provider profiles within your Uptime account.</li>

<li>**API key**: This will be obtained from Datadog. Please review the Obtaining Datadog API Key section below for further documentation.</li>

<li>**Application Key**: This will be obtained from Datadog. Please review the Obtaining Datadog Application Key section below for further documentation.</li>

<li>Once you've configured your Datadog profile, you will need to assign the profile to a contact group located under Alerting>Contacts. The profile is assigned at the Push Notifications field within the contact group.</li> 

</ul>
