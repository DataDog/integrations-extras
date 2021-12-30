# Superwise Integration

## Overview
[Superwise][1]  is about solving model observability for high-scale ML operations.
Superwise model observability gives you visibility and context into your models' behaviors, so you can easily express and monitor model risks as they relate to your business. With Superwise, data scientists, ML engineers, and business ops get intuitive model observability without the alert fatigue so you can be confident about your model management and focus on the fun things in life like building newer, better models.  
    

![Superwise Dashboard]( https://raw.githubusercontent.com/DataDog/integrations-extras/master/superwise/images/5.png)  

Superwise’s model metrics and incidents integration streamline results of our out-of-the-box model metrics, including drift, activity, incidents, and any custom metrics you configure, directly into Datadog app. You’ll get an immediate overview of which models are misbehaving that can be tailored to any use case, logic, segmentation, threshold, and sensitivity.


## Setup

Once a user configures the Datadog integration in Superwise, standard model metrics are sent to Datadog and users get model observability dashboards within Datadog. Users can also configure any specific model metric and incident policy and send them to Datadog for model observability tailored to their business context.

1. Go to [Superwise portal][2] and Select the integration tab.
![Superwise Integration]( https://raw.githubusercontent.com/DataDog/integrations-extras/master/superwise/images/1.png)

2. Click on Create a new channel and select Datadog Integration.
![Superwise Integration]( https://raw.githubusercontent.com/DataDog/integrations-extras/master/superwise/images/2.png)

3. Input your Datadog API Key and Application key and click on the Test button. The Test button will send a dummy request to your Datadog account to validate the integration. You should get a success message in Superwise . To finish the setup click “Create channel”.

![Superwise Integration]( https://raw.githubusercontent.com/DataDog/integrations-extras/master/superwise/images/6.png)

3. That's it, Now you can see a widget of new integration with Datdog and that it (:
![Superwise Integration]( https://raw.githubusercontent.com/DataDog/integrations-extras/master/superwise/images/3.png)

 ### Validation
Go to the metric explorer section of the Datadog app to verify the integration between Superwise and Datadog,
Superwise sent the superwise.integration.test metric to Datadog to validate the integration.  
![Superwise Integration]( https://raw.githubusercontent.com/DataDog/integrations-extras/master/superwise/images/4.png)   

## Data Collected

### Metrics

See [metadata.csv][3] for a list of metrics provided by this check.

### Events

The Superwise integration does not include any events.

### Service Checks

The Superwise integration does not include any service checks.

## Troubleshooting

Need help? Contact [Superwise support][4].


[1]: https://www.superwise.ai/
[2]: https://portal.superwise.ai/
[3]: https://github.com/DataDog/integrations-core/blob/master/check/metadata.csv
[4]: https://docs.superwise.ai
