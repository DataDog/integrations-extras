# RBLTracker

## Overview

Connect your RBLTracker account to Datadog to track listing and de-listing events from RBLTracker on your Datadog dashboards and event tream..

## Setup

### Configuration

Setting up RBLTracker using webhooks:

* Create an API Key in Datadog. <span class="hidden-api-key">${api_key}</span>
* In [RBLTracker](https://rbltracker.com/), create a new Datadog contact type from the **Manage -> Contacts** section of the RBLTracker portal.
* Paste the Datadog **API Key**.
* (optional) adjust the contact schedule for this new contact.

RBLTracker will now send listing and delisting alerts to your Datadog as events. 
