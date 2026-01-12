# Stonebranch


## Overview
To learn more about this integration, visit https://docs.datadoghq.com/integrations/stonebranch/
This extension collects UAC metrics via Datadog Agent and turns them into a UC-aware view inside Datadog. It discovers Universal Controllers, OMS servers, Universal Agents, workflows, and business services from metric labels together with an example dashboards.

IT Ops, SREs, and platform teams can use this extension to:

    Track task execution and workflow outcomes.
    Monitor controller, JVM, and process health.
    Watch UAC license consumption and capacity limits.
    Receive UAC-specific alerts when OMS, agents, or licenses are in trouble.

## Use cases
- Overview of your entire UAC environment: Get an overview of one or more Universal Controllers with an all-in-one view inside of Dynatrace.
- Controller and OMS health monitoring: Detect controller node or OMS issues early using status and connection metrics.
- Automation workload visibility: Monitor execution counts, active instances, and outcome distributions across workflows and task types.
- License and capacity management: Track usage of agents, nodes, executions, and tasks against license quotas to avoid overages.
- Workflow- and agent-centric views: Use workflow and Universal Agent entity screens to understand where tasks run, how they perform, and which business services they belong to.
- Integrated troubleshooting inside Dynatrace: Use dashboards, entity screens, and alerts to quickly isolate whether a problem is in the automation logic, the controller, the agents, or the underlying infrastructure.

## Setup
1. Install and activate the extension from the Datadog Marketplace
2. Configure the metric endpoint inside of the Datadog Agent.
    - Make sure to use a valid user with the correct permissions.
3. Edit any metrics that are unwanted in the allowlist section.

## Support
TBD
