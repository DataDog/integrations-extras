## Overview

Collect custom metrics from your application with a few clicks and send it to Datadog. No need to write code, redeploy or restart your app.

* Enhance monitoring and expedite production debugging with Rookout’s on-demand data collection
* Collect custom metrics ad-hoc from Rookout without the need for new instrumentation

**Note: Since this integration enables you to collect custom metrics, there may be billing implications based on the number of custom metrics collected. More information on custom metrics can be [found here](https://docs.datadoghq.com/getting_started/custom_metrics/).**

## Setup

### Installation

Rookout sends data to Datadog via the DogStatsD service available from the Datadog Agent.

1. Install the [Datadog Agent][1] and [Rookout][2].

2. Log into [Rookout's webapp][3]

3. In the right panel (Rules) click on the menu button

    ![Rule actions menu][4]

4. Click on *Create new template* in order to edit a new rule template

    ![Create new template button][5]

5. Copy the Datadog Custom Metric rule template [available here][6] into the editor and replace the default rule template.

    ![Datadog Custom Metric rule template][7]

6. Click the save icon to save the template

    ![Click Save Icon][8]

7. Add the newly created rule to any application as you would normally

### Configuration

You can configure the rule to use specific actions, every rule should contain these attributes in the `processing.operations` object:

```
{
    "name": "dogstatsd",
    "action": "<ACTION>",
    "metric": "<METRIC_NAME>",
    "target": {
      "host": "<HOST_NAME>",
      "port": 8125
    }
}
```

Depending on the actions, it needs different additional attributes:

```
| Datadog Action |  Attributes |
|----------------|-------------|
|    increment   | value       |
|    decrement   | value       |
|      event     | title, text |
|      gauge     | value       |
|    histogram   | value       |
|     timing     | value       |
|  distribution  | value       |
```

For more information about these actions you can see [Dogstatsd documentation][9]

Any attribute must be formatted the following way to be accepted by our rule:

```
"value": {
    "name": "calc",
    "path": "123"
}
```

```
"value": {
    "name": "calc",
    "path": "\"string\""
}
```

## Data Collected
You can collect custom metrics and events by creating a Datadog output in your Rookout rule. Some commonly used patterns:

* Count the number of a times a method is invoked (increment)
* Document process started in DataDog (event)
* Record batch sizes (histogram)

## Troubleshooting

If you have any questions, contact us at support@rookout.com.

## Further Reading

Find out more at [https://docs.datadog.com/][10]

[1]: https://docs.datadoghq.com/agent
[2]: https://docs.rookout.com/docs/getting-started.html
[3]: https://app.rookout.com
[4]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/rookout/images/click_rule_action.png
[5]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/rookout/images/click_new_template.png
[6]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/rookout/rule-template.json
[7]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/rookout/images/datadog_rule_template.png
[8]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/rookout/images/click_save.png
[9]: https://docs.datadoghq.com/developers/dogstatsd/
[10]: https://docs.datadog.com/
