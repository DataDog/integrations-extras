# N2WS Backup & Recovery

## Overview


N2WS Backup & Recovery (CPM), known as N2WS, is an enterprise-class backup, recovery, and disaster recovery solution for Amazon Web Services (AWS) and Microsoft Azure. N2WS uses cloud native technologies (snapshots) to provide backup and restore capabilities in AWS and Azure.

Your N2WS Backup and Recovery instance supports the monitoring of backups, disaster recovery, copy to S3, alerts, 
and more by Datadog monitoring service. This integration allows users to monitor and analyze the N2WS Backup and Recovery Dashboard metrics.

## Setup

### Installation

1.	##### Install the [Python Integration][1]

2.  ##### Enable support for Datadog on your N2WS instance:
    - Connect to your N2WS Backup and Recovery instance with SSH.
    - Add the lines below to `/cpmdata/conf/cpmserver.cfg`. You might need `sudo` privileges to perform this action.
        ```
        [external_monitoring]
        enabled=True
        ```
    - Run `service apache2 restart`

3.	##### Install the Datadog Agent on your N2WS Instance.
    Login to Datadog and go to Integrations -> Agent -> Ubuntu
    Copy the agent ‘easy one-step install’ command 
    Connect to your N2WS Backup and Recovery Instance with SSH. You may require `sudo` privileges to perform this action.

4.	##### Setup Datadog Dashboard metrics
    Go to [‘Metrics-> Explorer’][2]

    **Graph**: Select your metric from the list. All N2WS metrics begin with the string ‘cpm_metric’.

    **Over**: Select data from the list. All N2WS users data begin with the string ‘cpm:user:<user-name>’.
              You can select either a specific user or the entire N2WS instance.


5.	##### Get N2WS dashboards
    In [Datadog Integrations][3] , search for 'N2WS' tile and install it. 
    You will get 5 types of dashboards to your account, 3 for N2WS Backup & Recovery v3.2.1 (only AWS supported) and 2 for for N2WS Backup & Recovery v4.0 (includes Azure):
    'N2WSBackup&Recovery-Graphicalversion', 'N2WSBackup&Recovery-Graphicalversion-areas' and 'N2WSBackup&Recovery-EntitiesSpecificDashboard' for version 3.2.1
	'N2WSBackup&Recovery-EntitiesSpecificDashboardV4.0' and 'N2WSBackup&Recovery-GraphicalVersionV4.0' for version 4.0
 
    Alternatively users can [import JSON templates from N2WS][4].

## Data Collected

Datadog collects the following data about N2WS Backup & Recovery backups:

- The number of snapshots of each type
- Successful backups (AWS only)
- Failed backups (AWS only)
- Partially successful backups (AWS only)
- Protected resources from any type
- Data about volume capacity (AWS only), alerts, etc.

### Metrics

See [metadata.csv][5] for a list of metrics provided by this check.

### Events

Datadog collects alert messages from all N2WS Backup & Recovery hosts.

### Service Checks

The N2WS Backup & Recovery integration does not include any service checks.

## Troubleshooting

- [N2WS user guide and documentation][6]
- [N2WS support][7]
- [Datadog support][8]


[1]: https://app.datadoghq.com/account/settings#integrations/python
[2]: https://app.datadoghq.com/metric/explorer
[3]: https://app.datadoghq.com/account/settings#integrations/n2ws
[4]: https://support.n2ws.com/portal/en/kb/articles/datadog-templates
[5]: https://github.com/DataDog/integrations-extras/blob/master/n2ws/metadata.csv
[6]: https://n2ws.com/support/documentation
[7]: https://n2ws.com/support 
[8]: https://docs.datadoghq.com/help/
[9]: https://app.datadoghq.com/account/settings#ubuntu
