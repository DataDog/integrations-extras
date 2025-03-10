# Chainguard

## Overview

Chainguard allows developers to reduce engineering toil to manage CVEs, build on a secure foundation of open source software and also streamline compliance across the company against business-critical frameworks like FedRAMP, PCI-DSS, SOC2 and others. Our product, Chainguard Containers, are minimal, contain zero CVEs and come equipped with guarded protection under our remediation SLA. All 1200+ of our images are built from source, scanned and patched for CVEs regularly. 

This integration includes an out-of-the-box dashboard that displays existing containers eligible for migration to Chainguard Containers. You can quickly see long-running containers which may be end-of-life and eligible for an update to a secure container. Additionally, if you're a customer of CSM Infrastructure Vulnerabilities, you can see which containers have the most CVEs, and in turn, should be migrated to Chainguard earlier. 

## Setup

The included out-of-the-box dashboard automatically queries existing Docker container metrics collected by the Datadog Agent. No additional setup is required.

To start using a Chainguard Image, visit [Chainguard Images][1], find your desired image, and follow the instructions to pull it.

## Uninstallation

To remove the out-of-the-box dashboard, go to the Chainguard integration tile, navigate to the Configure tab, and click **Uninstall Integration**.

To uninstall a Chainguard Image, remove all references to it in your configuration and revert to the original image.

## Support

To reach our support team, please follow the instructions on our [Contact page][2].


[1]: https://images.chainguard.dev
[2]: https://www.chainguard.dev/contact