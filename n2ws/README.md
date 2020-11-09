# N2WS Backup & Recovery

## Overview

N2WS Backup & Recovery (CPM), known as N2WS, is an enterprise-class backup, recovery, and disaster recovery (DR) solution for Amazon Web Services (AWS). 
N2WS uses cloud native technologies (e.g. EBS snapshots) to provide backup and restore capabilities in AWS.

Your N2WS Backup and Recovery instance supports the monitoring of backups, disaster recovery (DR), copy to S3, alerts 
and more by Datadog monitoring service. 
This integration allows users to monitor and analyze the N2WS Backup and Recovery Dashboard metrics.

## Setup

### Installation

1.	Install the [Python Integration][1]


2.	Enable Datadog support on your N2WS instance
Connect to your N2WS Backup and Recovery instance with SSH. Add the following lines to `/cpmdata/conf/cpmserver.cfg`. You may require `sudo` privileges to perform this action.
`[external_monitoring]
enabled=True`

Run `service apache2 restart`


3.	Install the Datadog Agent on your N2WS Instance
Login to Datadog and go to Integrations -> Agent -> Ubuntu
Copy the agent ‘easy one-step install’ command 
Connect to your N2WS Backup and Recovery Instance with SSH. You may require `sudo` privileges to perform this action.


4.	Setup Datadog Dashboard metrics
Go to [‘Metrics-> Explorer’][2]

**Graph**: Select your metric from the list. All N2WS metrics begin with the string ‘cpm_metric’.

**Over**: Select data from the list. All N2WS users data begin with the string ‘cpm:user:<user-name>’.
You can select either a specific user or the entire N2WS instance.


5.	Get N2WS dashboards
In [Datadog Integrations][3] , search for 'N2WS' tile and install it. 
    You will get 3 types of dashboards to your account:
    'N2WSBackup&Recovery-Graphicalversion', 'N2WSBackup&Recovery-Graphicalversion-areas' and 'N2WSBackup&Recovery-Squaresdashboard'.
 
Alternatively users can [import JSON templates from N2WS][4].


## Data Collected

Datadog collects data about N2WS Backup & Recovery backups: number of snapshots of each type, successfull backups, failed backups, partially successful backups, 
protected resources from any type, data about volume capacity, alerts, etc.


### Metrics

See [metadata.csv][5] for a list of metrics provided by this check.


### Events

Datadog collects alert messages from all the N2WS Backup & Recovery hosts.


### Service Checks

N2WS Backup & Recovery doesn't have service checks.


## Troubleshooting

[N2WS User Guide and documentation][6]
[N2WS Support][7] 



[1]: https://app.datadoghq.com/account/settings#integrations/python
[2]: https://app.datadoghq.com/metric/explorer
[3]: https://app.datadoghq.com/account/settings#integrations
[4]: https://support.n2ws.com/portal/en/kb/articles/datadog-templates
[5]: https://github.com/DataDog/integrations-extras/blob/master/n2ws/metadata.csv
[6]: https://n2ws.com/support/documentation
[7]: https://n2ws.com/support 
