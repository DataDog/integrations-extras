N2WS Backup & Recovery (CPM), known as N2WS, is an enterprise-class backup, 
recovery and disaster recovery solution for the Amazon Web Services (AWS). 
Designed from the ground up to support AWS, N2WS uses cloud native technologies 
(e.g. EBS snapshots) to provide unmatched backup and, more importantly, restore capabilities in AWS.

N2WS Backup and Recovery Instance is now supporting the monitoring of backups, DR, copy to S3, alerts 
and more by Datadog monitoring service. 
It will allow users to monitor and analyse the N2WS Backup and Recovery Dashboard metrics.


Please perform the following steps in order to activate the service and to monitor your N2WS instance:

1.	Setup Datadog Account 
Visit Datadog to: https://www.datadoghq.com/pricing/ and setup an account that fits your scale.


2.	Install Python Integration
Login to Datadog and go to Integrations -> Integrations
Search for ‘Python’ and install it


3.	Enable Datadog support on N2WS Instance
Connect to your N2WS Backup and Recovery Instance with SSH Client, type “sudo su” and add the following lines to /cpmdata/conf/cpmserver.cfg
[external_monitoring]
enabled=True
run ‘service apache2 restart’


4.	Install Datadog Agent on N2WS Instance
Login to Datadog and go to Integrations -> Agent -> Ubuntu
Copy the agent ‘easy one-step install’ command 
Connect to your N2WS Backup and Recovery Instance with SSH Client, type “sudo su” and  run the agent Install command.


5.	Setup Datadog Dashboard metrics
Login to Datadog and go to ‘Metrics-> Explorer’

From Graph: 
Select your metric from the list (all N2WS metrics begin with the string ‘cpm_<metric-name>’)

From Over:
Select data from the list (all N2WS users data begin with the string ‘cpm:user:<user-name>’)
You can either select a specific user or the entire N2WS instance alternatively



6.	Get N2WS dashboards
In Datadog's UI, go to 'Integrations-> Integrations', search for 'N2WS' tile and install it. You will get 3 types of dashboards to your account:
'N2WSBackup&Recovery-Graphicalversion', 'N2WSBackup&Recovery-Graphicalversion-areas' and 'N2WSBackup&Recovery-Squaresdashboard'.
 
Users can alternatively import the .json templates for N2WS from here:
https://support.n2ws.com/portal/en/kb/articles/datadog-templates




