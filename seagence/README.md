# Seagence for Datadog

## Overview

[Seagence][1] is a defect monitoring platform for Java applications that detects defects including root cause in real-time.

### Description

Tired of debugging unknown defects impacting your customer experience? Using revolutionary ExecutionPath technology, discover how Seagence detects unknown defects caused by various issues like swallowed exceptions, multithreading issues, and others including defects that disguise in a 200 HTTP response code in your production Java applications. Seagence is the only solution that can detect unknown defects as they manifest. You fix your code without debugging.

### Usage

Seagence integrates with Datadog using API based integration. Seagence's java agent is attached to your production application which will post collected data (ExecutionPaths and contextual information) to Seagence backend. When Seagence backend detects a defect, it posts the defect and it's root cause as a Datadog event to Datadog backend using Rest API. Upon defect event posted, a Datadog monitor (which is automatically setup) will raise alert.

## Setup

For Installation, Setup and Configuration instructions, please visit [getting started][3] on [Seagence website][1]

## Data Collected

### Metrics

Seagence does not include any metrics.

### Service Checks

Seagence does not include any service checks.

### Events

Seagence posts an event to datadog upon detecting a defect.

## Support

Need help? Contact [Seagence support][2].


[1]: https://www.seagence.com
[2]: mailto:info@seagence.com
[3]: https://seagence.com/product/getting-started/
