# Shoreline.io

## Overview

Shoreline incident automation enables DevOps and Site reliability engineers (SREs) to interactively **debug at scale** and quickly **build remediations** to eliminate repetitive work.

**The debug and repair feature** allows engineers to execute commands in real-time, across their server farm without having to SSH into the servers individually. You can execute anything that can be typed at the Linux command prompt, including Linux commands, shell scripts, calls to their cloud provider APIs, etc. Then, quickly turn these debug sessions into automations connected to Datadog monitors. The Shoreline app will automatically execute that automation whenever the monitor is triggered. This greatly reduces Mean Time To Repair (MTTR) and manual work.

Shoreline helps everyone on call to be as good as your best SRE.  Shoreline
arms your entire on-call team with best practice debugging tools and
approved remediation actions.  This helps the whole team find and fix
incidents more quickly with fewer escalations.  It also ensures that incidents
are fixed correctly the first time with fewer mistakes.

To get started, [visit][visit] ![link_icon] to set up a trial account.
## Setup

### Installation

Follow the steps below to configure the integration:

1. Install the Shoreline agent
2. Configure Datadog integration from Shoreline


#### Install the Shoreline agent

Shoreline Agents must be installed on every host you want Shoreline to monitor and act upon. There are a few recommended methods for installing Agents:

1. [Kubernetes][installation_kubernetis] ![link_icon]
2. [Kubernetes via Helm][installation_via_helm] ![link_icon]
3. [Virtual Machines][installation_virtual_machines] ![link_icon]

**About Shoreline Agents**\
An Agent is an efficient and non-intrusive process running in the background of all your monitored hosts. Agents constantly collect data from both the host and all connected pods and containers. This aggregated data is periodically sent to Shoreline's backend and is used to create Metrics.

Agents are also the secure link between Shoreline and your environment's Resources. Agents can execute actions on your behalf -- everything from simple Linux commands to remediation playbooks. Many Op Language statements pass an API request through Shoreline's backend and onto the relevant Agents, which then execute that command across all targeted Resources.

Since Agents receive commands from Shoreline's backend, they also take automatic remediation steps based on the Alarms, Actions, and Bots you have configured. These objects work in tandem to monitor your fleet and dispatch the appropriate response if something goes wrong.

#### Configure Datadog integration from Shoreline

Log into your Shoreline account and configure your Datadog integration. 
You will need the API and Application keys of your Datadog account.\
[Learn more][learn_more] ![link_icon]. 

![integration_example]

## Support

For support or requests, please contact Shoreline through the following channels:

Email: [support@shoreline.io][support_email]\
Documentation is available [here][docs].

[integration_example]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/shoreline/images/integrate_shoreline_and_datadog.png
[support_email]: support@shoreline.io
[visit]: https://shoreline.io/datadog?source=DatadogIntTile
[learn_more]: https://docs.shoreline.io/integrations/datadog
[installation_kubernetis]: https://docs.shoreline.io/installation/kubernetes
[installation_via_helm]: https://docs.shoreline.io/installation/kubernetes#install-with-helm
[installation_virtual_machines]: https://docs.shoreline.io/installation/virtual-machines
[link_icon]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/shoreline/images/link_icon.svg
[docs]: https://docs.shoreline.io/