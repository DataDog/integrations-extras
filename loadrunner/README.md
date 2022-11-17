# LoadRunner Professional

## Overview

[LoadRunner Professional][7] provides a load testing solution that enables you to test the performance of diverse application types, and to identify and resolve issues before applications go live.


The LoadRunner Professional integration with Datadog enables you to view Datadog metrics in LoadRunner Controller and Analysis graphs.


## Setup

Set up the LoadRunner Professional Datadog monitor to view data from Datadog. For each Datadog host, you define the metrics for which you want to view data.


You can also create a **host group** and define metrics for the group, as well as the aggregation function to use. Datadog applies the function to the results from the relevant hosts, and returns the response for each metric.


### LoadRunner Professional Datadog monitor


1. In the LoadRunner Controller, on the **Run** tab, select **Graphs > Datadog Graphs > Datadog**.


The **Datadog graph** display box opens in the display area.

2. In the graph display box, click **Add measurements**.

3. In the **Datadog dialog box > Monitored Server Machines** pane, click **Add**. The **Connect to Datadog** dialog box opens.

4. Define the following to set up the connection to Datadog:


   ![snapshot][2]

   -  **Site**. Select the Datadog site where you have your user account.

   -  **API key and application key**. These are generated in Datadog for your user account.

   Click **Connect**.


5. The **Select host** dialog box opens, listing the available hosts for the account.

   Select the host or hosts from which you want to pull metrics, and click **OK**.

   ![snapshot][3]

   **Note:** If you select more than one host, this creates a host group for the metrics.


6. The selected host or host group is added to the **Monitored Server Machines** pane in the Datadog dialog box. Select an entry in the pane.

7. To define metrics for the selected host or host group, click **Add** in the **Resource Measurements** area.

8. The **Select metrics for host** or **Select metrics for host group** dialog box opens. It lists the available metrics for the host, or for all hosts in the host group.

   ![snapshot][4]

   - Select the relevant metrics and add them to the **Selected metrics** list.

   - If you are defining metrics for a host group, define the aggregation method. Datadog applies the selected method to the metrics from all hosts.

   Click **OK**.

   The measurements are displayed in the **Resource Measurements** pane of the Datadog dialog box.


9. When done, click **OK** in the Datadog dialog box.

10. After some brief processing, the Controller displays metrics in the Datadog graph.


For metrics that are collected from multiple hosts (as indicated in the **Machine** column), each data point in the graph gives the aggregated value for all hosts. The aggregation method is indicated in the metric name, for example, `avg:metric1`.


## Analysis Datadog graph


The Analysis Datadog graph displays metrics fetched by the Datadog monitor. For details, see [Datadog monitor][5].

When a metric is showing aggregated results from more than one host, the names of all hosts are included in the **Measurement** column in the legend. The aggregation method is indicated in the metric name, for example, `avg:metric1`.


![snapshot][6]
![snapshot][8]

## Support

Need help? Go to the [LoadRunner Professional Help Page][1].


  
[1]: https://admhelp.microfocus.com/lr/en/2022-2022-r2/help/WebHelp/Content/WelcomeContent/c_Welcome.htm?tocpath=Get%20Started%7C_____1
[2]: https://github.com/DataDog/integrations-extras/blob/master/loadrunner/images/datadog-connect.png
[3]: https://github.com/DataDog/integrations-extras/blob/master/loadrunner/images/datadog-host.png
[4]: https://github.com/DataDog/integrations-extras/blob/master/loadrunner/images/datadog-metrics.png
[5]: https://admhelp.microfocus.com/lr/en/2022-2022-r2/help/WebHelp/Content/Controller/Datadog-monitor.htm
[6]: https://github.com/DataDog/integrations-extras/blob/master/loadrunner/images/datadog-graph.png
[7]: https://www.microfocus.com/products/loadrunner-professional/overview
[8]: https://github.com/DataDog/integrations-extras/blob/master/loadrunner/images/datadog-graph-legend.png
