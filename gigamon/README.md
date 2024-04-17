# Gigamon

## Overview
[Gigamon][1]  Application Metadata Intelligence empowers your Observability, Security Information and Event Management (SIEM), and Network Performance Monitoring tools with critical metadata attributes across thousands of business, consumer, and IT applications and services. Get deep application visibility to rapidly pinpoint performance bottlenecks, quality issues, and potential network security risks. Gigamon's Application Metadata Intelligence (AMI) helps you monitor and manage complex digital applications for your digital transformation initiatives. This can be achieved through the Gigamon Solution by sending the AMI metadata to Datadog. Some benefits to highlight are Rich Actionable Insights, Boost Security Posture etc.

For more information, [contact][6] 

## Setup
Gigamon Sends AMI metadata [AMX][2] to the Datadog API using http post. 

### Installation

GigaVUE V Series Node is a virtual machine running in the customer's infrastructure which processes and distributes network traffic.  Gigamon Application Metadata Exporter (AMX) application converts the output from the Application Metadata Intelligence (AMI) in CEF format into JSON format and sends it to Datadog. The AMX application can be deployed only on a V Series Node and can be connected to Application Metadata Intelligence running on a physical node or a virtual machine. The AMX application and the AMI are managed by GigaVUE-FM. 

1. Once you have the AMX installed in your environment, Create a Monitoring Session  in [FM] [3]. 
2. Edit the exporter and provide required fields as shown below:
    a. Alias : Name of the Exporter (String )
    b. Ingestor : Provide Port as "514" and Type as "ami"
    c. Cloud Tool Exports: Create new exporter tool by selecting '+' and add details as shown in the below diagram 
    ![1](https://raw.githubusercontent.com/DataDog/integrations-extras/master/gigamon/images/images/gigamon1.png)
    ![2](https://raw.githubusercontent.com/DataDog/integrations-extras/master/gigamon/images/images/gigamon2.png)
    

## Data Collected

### Metadata Attributes
Gigamon deep packet inspection extracts 7500+ application metadata attributes & forwards to Datadog. Gigamon Application Metadata Protobook provides a complete list of supported protocols and their attributes. These protocols can also be viewed as groups by Tags, Family and Classification method.

You can access the Application Metadata Protobook from the [GigaVUE FM][4].

## Troubleshooting
Need help? Contact [Gigamon Support][5].

[1]: http://gigamon.com
[2]: https://docs.gigamon.com/doclib66/Content/GV-Cloud-V-Series-Applications/AMX_intro.html
[3]: https://docs.gigamon.com/doclib66/Content/GigaVUE_Cloud_Suites.html?tocpath=GigaVUE%20Cloud%20Suite%7C_____0
[4]: https://docs.gigamon.com/doclib66/Content/GV-GigaSMART/Application%20Protocol%20Bundle.html
[5]: https://www.gigamon.com/support/support-and-services/contact-support.html
[6]: alliances@gigamon.com 
