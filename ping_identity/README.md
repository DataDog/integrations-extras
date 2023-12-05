# Agent Check: Ping Identity

## Overview

Ping Identity delivers intelligent identity solutions for the enterprise. We enable companies to achieve Zero Trust identity-defined security and more personalized, streamlined user experiences.

Datadog integrates directly with the PingOne DaVinci platform through the Datadog API connector. The connector boasts over 350+ unique capabilites, each with a unique Datadag API endpoint to complete actions ranging from general CRUD commands to 

## Setup

### Installation

Installation with PingOne's DaVinci platform is simple and easy with Ping's drag and drop functionality on a flow canvas. Follow the below steps to configure Datadog within DaVinci:

1. On a flow, select the black "+" button in the bottom left corner of the flow canvas. 

2. Search for Datadog and select it to add it to the canvas.


### Configuration

1. Click into the connector to open the connector side panel. Select "Configure". You will need to enter the API URL, Authentication API Key and Authentication Application Key from your Datadog tenant to successfully configure the connector within your DaVinci tenant. "Apply" changes once added.

2. Scroll and select the proper capability for your use case.

3. Enter any additional information required for the connector to successfuly run. These will be capability dependent.

### Validation

You can validate that the connector is working by linking the connector to other connectors (namely the HTTP connector) to view the output of the connector in a demo flow. Utilize the "Custom HTML Message" capability from the HTTP connector and in the message field, select the "{}" to choose the output from the Datadog connector. Run the flow widget by selecting "Try Flow" in the upper right corner to execute the connector and determine if it is working as expected.

## Data Collected

### Metrics

Ping Identity does not include any metrics.

### Service Checks

Ping Identity does not include any service checks.

### Events

Ping Identity does not include any events.

## Troubleshooting

Need help? Contact tap-global@pingidentity.com.