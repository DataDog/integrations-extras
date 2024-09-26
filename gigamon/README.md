# Gigamon

## Overview
[Gigamon][1]  Application Metadata Intelligence (AMI) empowers your Observability, Security Information and Event Management (SIEM), and Network Performance Monitoring tools with critical metadata attributes across thousands of business, consumer, and IT applications and services. Get deep application visibility to quickly pinpoint performance bottlenecks, quality issues, and potential network security risks. Gigamon's AMI helps you monitor and manage complex digital applications for your digital transformation initiatives. This can be achieved through the Gigamon Solution by sending the AMI metadata to Datadog. Some benefits to highlight are Rich Actionable Insights, Boost Security Posture, etc.

## Setup
Gigamon sends AMI metadata [AMX][2] to the Datadog API using HTTP `POST`. 

### Installation

GigaVUE V Series Node is a virtual machine running in the customer's infrastructure which processes and distributes network traffic. Gigamon Application Metadata Exporter (AMX) converts the output from the AMI in CEF format into JSON and sends it to Datadog. The AMX application can be deployed only on a V Series Node and can be connected to AMI running on a physical node or a virtual machine. The AMX application and the AMI are managed by GigaVUE-FM. 

1. After you install AMX in your environment, create a monitoring session in [FM][3]. 
2. Edit the exporter and provide the following required fields:
    a. Alias: Name of the exporter (String).
    b. Ingestor: Specify the Port as "514" and Type as "ami".
    c. Cloud Tool Exports: Create a new exporter tool by selecting '+' and add details as shown in the following diagram:
    ![1](https://raw.githubusercontent.com/DataDog/integrations-extras/master/gigamon/images/images/gigamon1.png)
    ![2](https://raw.githubusercontent.com/DataDog/integrations-extras/master/gigamon/images/images/gigamon2.png)
    

## Data Collected

### Metadata Attributes
Gigamon deep packet inspection extracts 7500+ application metadata attributes and forwards them to Datadog. Gigamon Application Metadata Protobook provides a complete list of supported protocols and their attributes. These protocols can also be viewed as groups by Tags, Family, and Classification method. 

Gigamon AMX converts the output from the AMI in CEF format into JSON and sends it to Datadog.

You can access the Application Metadata Protobook from the [GigaVUE FM][4].

## Troubleshooting
Need help? Contact [Gigamon Support][5].

[1]: http://gigamon.com
[2]: https://docs.gigamon.com/doclib66/Content/GV-Cloud-V-Series-Applications/AMX_intro.html
[3]: https://docs.gigamon.com/doclib66/Content/GigaVUE_Cloud_Suites.html?tocpath=GigaVUE%20Cloud%20Suite%7C_____0
[4]: https://docs.gigamon.com/doclib66/Content/GV-GigaSMART/Application%20Protocol%20Bundle.html
[5]: https://www.gigamon.com/support/support-and-services/contact-support.html

