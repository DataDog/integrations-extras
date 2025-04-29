# Gatling Enterprise

## Overview

Fetch your load testing metrics and build dashboards to investigate your performance issues

## Setup

In your [control-plane configuration][1], in the section `system-properties`, you have to add:

```bash
control-plane {
  locations = [
    {
      id = "prl_example"
      # ... other configuration for your location

      system-properties {
        "gatling.enterprise.dd.api.key" = "<your api key>" # fill your API key here
        "gatling.enterprise.dd.site" = "datadoghq.com"  # replace with your Datadog site
      }
    }
  ]
}
```

## Uninstallation

To remove the link between Gatling Enterprise and Datadog, remove the lines containing `gatling.enterprise.dd` in your control-plane configuration.

## Support

Access our support services through Gatling Enterprise (Help center > Support ticket) or here: https://gatlingcorp.atlassian.net/servicedesk/customer/portal/8


[1]: https://docs.gatling.io/reference/install/cloud/private-locations/introduction/