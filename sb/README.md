# Stonebranch

## Overview

**Stonebranch Simplifies IT Automation and Orchestration across complex and diverse IT environments.**

The Stonebranch Universal Automation Center (UAC) platform helps organizations automate, manage, and orchestrate IT tasks and processes across multiple platforms and business applications in real-time. With UAC, you can break down automation silos by enabling centralized control and visibility across your entire hybrid IT environment, including on-premises, cloud, and containerized microservices.

**Six Pillars of Automation and Orchestration with Stonebranch UAC:**

**Event-Driven Automation:** Stonebranch UAC's event-based approach launches tasks, jobs, and workflows based on system triggers that can happen anytime. With our platform, you can automate IT processes in real time versus legacy batch and time-based job scheduling software approaches, which the UAC also supports. 

**Workflow Automation and Orchestration:** The UAC platform allows enterprises to visually design workflows across any environment. With low-or no-code drag-and-drop capabilities, enterprises can easily connect the dots between applications or platforms. 

**Self-Service Automation:** Our platform uses access controls via member groups to customize the experience for DevOps, Data Analysts, and any business user group, like finance or HR.  

**Infrastructure and Service Automation:** With Stonebranch UAC, you can create, start, stop, terminate, monitor, and alter both on-prem and cloud infrastructures. Our platform's ability to empower end-users, like DevOps, with self-service provisioning via infrastructure-as-code capabilities. 

**Manage Data Pipelines:** Automate data flow between disparate applications and platforms via native managed file transfer capabilities. Data movement is highly secure, and the platform is designed to transfer data within your internal environment or externally with 3rd party partners and vendors. 

**Analytics and Visibility:** Stonebranch UAC offers a command-center style set of views that provide alerts, dashboards, SLA monitoring, and more. This also includes customizing views by individual end-users and member groups. 

With the Stonebranch Universal Automation Center, you can integrate with any platform or application – from cloud to on-premises, and containerized microservices. 

For more information, please visit www.stonebranch.com


## Setup

1.  **Enable the Stonebranch integration** in your Datadog Agent.

2.  **Create an "observability" user** in Universal Controller with the `ops.admin` role. This account will authenticate to the metrics endpoint:\
    `https://universal-controller/uc/resources/metrics`

3.  **Edit the integration's config** (`datadog.d/stonebranch/conf.yaml`) and specify:

    ```yaml
    instances:
      - url: "https://universal-controller/uc/resources/metrics"
        username: "<OBSERVABILITY_USER>"
        password: "<OBSERVABILITY_PASSWORD>"
    ```


## Uninstallation

1.  **Revoke access** by removing the observability user from its User Groups in the Universal Controller-this stops all metric queries.

2.  **Uninstall the integration** from your Datadog Agent by following the standard removal steps:

    -   Stop the Agent (`sudo systemctl stop datadog-agent`)
    -   Delete the Stonebranch config file (`sudo rm /etc/datadog-agent/conf.d/stonebranch/conf.yaml`)
    -   Restart the Agent (`sudo systemctl start datadog-agent`)

## Support

For any Universal Controller–related questions, reach out to the Stonebranch main support team.


