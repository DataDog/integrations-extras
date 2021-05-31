# Agent Check: Zabbix

## Overview

Connect to Zabbix to:

- Monitor [Zabbix][1] through the Datadog Agent.
- Send Zabbix alerts to Datadog to see the alerts as events in your Datadog event stream.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host.

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Zabbix check on your host. See the dedicated Agent guide for [installing community integrations][3] to install checks with the [Agent prior to version 6.8][4] or the [Docker Agent][5]:

1. [Download and launch the Datadog Agent][6].
2. Run the following command to install the integrations wheel with the Agent:

   ```shell
   datadog-agent integration install -t datadog-zabbix==<INTEGRATION_VERSION>
   ```
3. Configure your integration like [any other packaged integration][6].


### Configuration

1. Edit the `zabbix.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your Zabbix performance data. See the [sample zabbix.d/conf.yaml][7] for all available configuration options.

2. [Restart the Agent][8].

#### Send Zabbix Alerts into the Event Stream

##### Create Datadog media type 

1. Navigate to *Administration > Media Types > Create Media Type*.
2. Add Datadog api_key as a parameter. And, add the following Zabbix template variables as parameters: {ALERT.MESSAGE}, {ALERT.SUBJECT}, {EVENT.DATE}, {EVENT.NAME}, {EVENT.NSEVERITY}, {EVENT.TAGSJSON}, {EVENT.TIME}, {EVENT.VALUE}, {ITEM.NAME}
3. Set **Name** to `Datadog`, **Type** to `Webhook`, and input the following code as the **Script**:
``` 
	try {
		Zabbix.Log(4, '[datadog webhook] received value=' + value);

		var params = JSON.parse(value);
	    var req = new CurlHttpRequest();
		req.AddHeader('Content-Type: application/json');
	    var webhook_url = 'https://app.datadoghq.com/intake/webhook/zabbix?api_key=' + params.api_key;
	    var webhook_data = value;
	    var resp = req.Post(webhook_url, webhook_data);
		if (req.Status() != 202) {
			throw 'Response code: '+req.Status();
		}
		Zabbix.Log(4, '[datadog webhook] received response with status code ' + req.Status() + '\n' + resp);
	} catch (error) {
		Zabbix.Log(4, '[datadog webhook] event creation failed json : ' + webhook_data)
		Zabbix.Log(4, '[datadog webhook] event creation failed : ' + error);
	}
	return JSON.stringify({});

```
4. Validate the Webhook is set up correctly by using the "Test" button.

##### Assign Webhook media to an existing user

1. After configuring the Webhook media type, navigate to *Administration > Users* and create a dedicated Zabbix user to represent the Webhook. For example, use the alias `Datadog` for the Datadog Webhook. All settings, except media, can be left at their defaults as this user does not log in to Zabbix.
2. In the user profile, go to a **Media** tab and add a Webhook with the required contact information. If the Webhook does not use a send to field, enter any combination of supported characters to bypass validation requirements.
3. Grant this user at least read permissions to all hosts for which it should send the alerts.

##### Configure an alert action for the Webhook

1. Navigate to *Configuration > Actions*.
2. From the page title dropdown, select the required action type.
3. Click on **Create Action**.
4. Name the action.
5. Choose conditions upon which operations are carried out.
6. Choose the operations to carry out.

### Validation

[Run the Agent's status subcommand][9] and look for `zabbix` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this check.

### Service Checks

`zabbix.can_connect`: Returns `CRITICAL` if the Agent can't connect to the Zabbix API, OK otherwise.

### Events

Zabbix alerts are collected as events in the Datadog event stream.

## Troubleshooting

Need help? Contact [Datadog support][11].

[1]: https://www.zabbix.com/
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/
[4]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[5]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[6]: https://docs.datadoghq.com/getting_started/integrations/
[7]: https://github.com/DataDog/integrations-extras/blob/master/zabbix/datadog_checks/zabbix/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[10]: https://github.com/DataDog/integrations-extras/blob/master/zabbix/metadata.csv
[11]: https://docs.datadoghq.com/help/
