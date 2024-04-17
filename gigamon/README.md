# Gigamon

## Overview
[Gigamon][1]  Application Metadata Intelligence empowers your Observability, Security Information and Event Management (SIEM), and Network Performance Monitoring tools with critical metadata attributes across thousands of business, consumer, and IT applications and services. Get deep application visibility to rapidly pinpoint performance bottlenecks, quality issues, and potential network security risks. Gigamon's Application Metadata Intelligence (AMI) helps you monitor and manage complex digital applications for your digital transformation initiatives. This can be achieved through the Gigamon Solution by sending the AMI metadata to DataDog. Some benefits to highlight are Rich Actionable Insights, Boost Security Posture etc.,

Deep Packet Inspection (DPI) is undeniably critical in the context of modern networking. Its capabilities, ranging from enhancing security to optimizing performance, underscore its value. For those eager to delve deeper into the nuances of DPI, Gigamon provides a rich repository of knowledge and insights.

To provide an example, Network Security: Consider prevalent threats like DDoS attacks and ransomware. DPI stands as a first line of defense, detecting and addressing such security challenges efficiently. For example, take an emerging e-commerce platform faced with a simultaneous DDoS attack and ransomware intrusion during peak hours. While a surge of malicious requests aimed to overwhelm its servers, ransomware tried sneaking in disguised as a regular file download. Thanks to the platform’s DPI solution, both threats were swiftly detected. The DPI identified the irregular traffic patterns of the DDoS attack and spotted the ransomware’s signature within data packets. Immediately, malicious DDoS packets were dropped, genuine traffic rerouted, and the ransomware-laden request blocked. The quick DPI response ensures minimal disruption, safeguarding both the platform’s reputation and its customer experience.


## Setup
Gigamon Sends AMI metadata [AMX][2] to the Datadog API using http post. 

### Installation

GigaVUE V Series Node is a virtual machine running in the customer's infrastructure which processes and distributes network traffic.  Gigamon Application Metadata Exporter (AMX) application converts the output from the Application Metadata Intelligence (AMI) in CEF format into JSON format and sends it to DataDog. The AMX application can be deployed only on a V Series Node and can be connected to Application Metadata Intelligence running on a physical node or a virtual machine. The AMX application and the AMI are managed by GigaVUE-FM. 

1. Once you have the AMX installed in your environment, Create a Monitoring Session  in [FM] [3]. 
2. Edit the exporter and provide required fields as shown below:
    a. Alias : Name of the Exporter (String )
    b. Ingestor : Provide Port as "514" and Type as "ami"
    c. Cloud Tool Exports: Create new exporter tool by selecting '+' and add details as shown in the below diagram 
    ![1](gigamon/images/gigamon1.png)
    ![2](gigamon/images/gigamon2.png)

## Data Collected
### Metadata Attributes
Gigamon Protobook provides a complete list of supported protocols and their attributes of metadata. These protocols can also be viewed as groups by Tags, Family and Classification method.

You can access the Application Protobook from the [GigaVUE‑FM][4] 

### Events
The Cribl Stream integration does not include any events.
### Service Checks
The Cribl Stream integration does not include any service checks.

## Troubleshooting
Need help? Contact [Gigamon Support][5].

[1]: http://gigamon.com
[2]: https://docs.gigamon.com/doclib61/Content/GV-Cloud-V-Series-Applications/Observability-Gareway_Application.html?tocpath=GigaVUE%20Cloud%20Suite%7CGigaVUE%20V%20Series%20Application%7CApplication%20Intelligence%7C_____4
[3]: https://docs.gigamon.com/doclib66/Content/GigaVUE_Cloud_Suites.html?tocpath=GigaVUE%20Cloud%20Suite%7C_____0
[4]: https://docs.gigamon.com/doclib66/Content/GV-GigaSMART/Application%20Protocol%20Bundle.html
[5]: https://www.gigamon.com/support/support-and-services/contact-support.html
