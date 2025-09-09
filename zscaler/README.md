# Zscaler Internet Access

## Overview

[Zscaler Internet Access][1] (ZIA) is a cloud-delivered security service that provides secure and fast access to the internet and SaaS applications for users, regardless of their location or device. It acts as a secure web gateway, inspecting all internet traffic and applying security policies to protect against threats and prevent data loss.

The integration uses a webhook to ingest Web, Firewall, DNS, Tunnel, SaaS Security, SaaS Security Activity, Admin Audit, Endpoint DLP, Email DLP and Alert logs.

Visualize detailed insights into these logs with out-of-the-box dashboards. Datadog uses its built-in log pipelines to parse and enrich these logs, facilitating easy search and detailed insights. Additionally, the integration includes ready-to-use Cloud SIEM detection rules for enhanced monitoring and security.

## Requirements

A Zscaler Cloud NSS subscription is required.

## Setup

### Configure a webhook in Zscaler

### ZIA Web Logs

1. From the ZIA console, go to **Administration** > **Nanolog Streaming Service**.
2. Select the **Cloud NSS Feeds** tab. Then, click on **Add Cloud NSS Feed**.
3. In the **General** section, enter or select the following values:
   * Feed Name: `<YOUR_FEED_NAME>`
   * NSS Type: `NSS for Web`
   * Status: `Enabled`
4. In the **SIEM Connectivity** section, enter or select the following values:
   * SIEM Type: `Other`
   * API URL: The URL you copied in previous section `Retrieve the Datadog Webhook URL`
   * HTTP headers:
      * Key: `Content-Type`; Value: `application/json`
5. In the **Formatting** section, enter or select the following values:
   * Log Type: `Web log`
   * Feed Output Type: `JSON`
   * Feed Escape Character: `,\"`
   * Please use the below feed output format:
      ```
      \{"sourcetype":"zscalernss-web","event":\{"datetime":"%d{yy}-%02d{mth}-%02d{dd} %02d{hh}:%02d{mm}:%02d{ss}","reason":"%s{reason}","event_id":"%d{recordid}","protocol":"%s{proto}","action":"%s{action}","transactionsize":"%d{totalsize}","responsesize":"%d{respsize}","requestsize":"%d{reqsize}","urlcategory":"%s{urlcat}","serverip":"%s{sip}","clienttranstime":"%d{ctime}","requestmethod":"%s{reqmethod}","refererURL":"%s{referer}","useragent":"%s{ua}","product":"NSS","location":"%s{location}","ClientIP":"%s{cip}","status":"%s{respcode}","user":"%s{login}","url":"%s{url}","vendor":"Zscaler","hostname":"%s{host}","clientpublicIP":"%s{cintip}","threatcategory":"%s{malwarecat}","threatname":"%s{threatname}","filetype":"%s{filetype}","appname":"%s{appname}","pagerisk":"%d{riskscore}","department":"%s{dept}","urlsupercategory":"%s{urlsupercat}","appclass":"%s{appclass}","dlpengine":"%s{dlpeng}","urlclass":"%s{urlclass}","threatclass":"%s{malwareclass}","dlpdictionaries":"%s{dlpdict}","ft_rulename":"%s{ft_rulename}","fileclass":"%s{fileclass}","bwthrottle":"%s{bwthrottle}","servertranstime":"%d{stime}","contenttype":"%s{contenttype}","unscannabletype":"%s{unscannabletype}","deviceowner":"%s{deviceowner}","devicehostname":"%s{devicehostname}","company":"%s{company}","cloudname":"%s{cloudname}","throttlereqsize":"%d{throttlereqsize}","throttlerespsize":"%d{throttlerespsize}","bwclassname":"%s{bwclassname}","bwrulename":"%s{bwrulename}","app_risk_score":"%s{app_risk_score}","app_status":"%s{app_status}","activity":"%s{activity}","prompt_req":"%s{prompt_req}","inst_level1_type":"%s{inst_level1_type}","inst_level1_id":"%s{inst_level1_id}","inst_level1_name":"%s{inst_level1_name}","inst_level2_type":"%s{inst_level2_type}","inst_level2_id":"%s{inst_level2_id}","inst_level2_name":"%s{inst_level2_name}","inst_level3_type":"%s{inst_level3_type}","inst_level3_id":"%s{inst_level3_id}","inst_level3_name":"%s{inst_level3_name}","datacenter":"%s{datacenter}","datacentercity":"%s{datacentercity}","datacentercountry":"%s{datacentercountry}","dlpdicthitcount":"%s{dlpdicthitcount}","dlpeng":"%s{dlpeng}","dlpidentifier":"%d{dlpidentifier}","dlpmd5":"%s{dlpmd5}","dlprulename":"%s{dlprulename}","trig_dlprulename":"%s{trig_dlprulename}","other_dlprulenames":"%s{other_dlprulenames}","all_dlprulenames":"%s{all_dlprulenames}","filename":"%s{filename}","filesubtype":"%s{filesubtype}","upload_fileclass":"%s{upload_fileclass}","upload_filetype":"%s{upload_filetype}","upload_filename":"%s{upload_filename}","upload_filesubtype":"%s{upload_filesubtype}","upload_doctypename":"%s{upload_doctypename}","rdr_rulename":"%s{rdr_rulename}","fwd_type":"%s{fwd_type}","fwd_gw_name":"%s{fwd_gw_name}","fwd_gw_ip":"%s{fwd_gw_ip}","zpa_app_seg_name":"%s{zpa_app_seg_name}","reqdatasize":"%d{reqdatasize}","reqhdrsize":"%d{reqhdrsize}","respdatasize":"%d{respdatasize}","resphdrsize":"%d{resphdrsize}","reqversion":"%s{reqversion}","respversion":"%s{respversion}","refererhost":"%s{refererhost}","uaclass":"%s{uaclass}","ua_token":"%s{ua_token}","df_hostname":"%s{df_hostname}","df_hosthead":"%s{df_hosthead}","mobappname":"%s{mobappname}","mobappcat":"%s{mobappcat}","mobdevtype":"%s{mobdevtype}","cpubip":"%s{cpubip}","clt_sport":"%d{clt_sport}","srcip_country":"%s{srcip_country}","dstip_country":"%s{dstip_country}","is_src_cntry_risky":"%s{is_src_cntry_risky}","is_dst_cntry_risky":"%s{is_dst_cntry_risky}","srv_dport":"%d{srv_dport}","alpnprotocol":"%s{alpnprotocol}","trafficredirectmethod":"%s{trafficredirectmethod}","userlocationname":"%s{userlocationname}","ruletype":"%s{ruletype}","rulelabel":"%s{rulelabel}","urlfilterrulelabel":"%s{urlfilterrulelabel}","apprulelabel":"%s{apprulelabel}","bamd5":"%s{bamd5}","sha256":"%s{sha256}","ssldecrypted":"%s{ssldecrypted}","externalspr":"%s{externalspr}","keyprotectiontype":"%s{keyprotectiontype}","clientsslcipher":"%s{clientsslcipher}","clienttlsversion":"%s{clienttlsversion}","clientsslsessreuse":"%s{clientsslsessreuse}","cltsslfailreason":"%s{cltsslfailreason}","cltsslfailcount":"%d{cltsslfailcount}","srvsslcipher":"%s{srvsslcipher}","srvtlsversion":"%s{srvtlsversion}","serversslsessreuse":"%s{serversslsessreuse}","srvocspresult":"%s{srvocspresult}","srvcertchainvalpass":"%s{srvcertchainvalpass}","srvwildcardcert":"%s{srvwildcardcert}","srvcertvalidationtype":"%s{srvcertvalidationtype}","srvcertvalidityperiod":"%s{srvcertvalidityperiod}","is_ssluntrustedca":"%s{is_ssluntrustedca}","is_sslselfsigned":"%s{is_sslselfsigned}","is_sslexpiredca":"%s{is_sslexpiredca}","threatseverity":"%s{threatseverity}","urlcatmethod":"%s{urlcatmethod}","devicemodel":"%s{devicemodel}","devicename":"%s{devicename}","devicetype":"%s{devicetype}","deviceostype":"%s{deviceostype}","deviceosversion":"%s{deviceosversion}","deviceappversion":"%s{deviceappversion}","ztunnelversion":"%s{ztunnelversion}","external_devid":"%s{external_devid}","bypassed_traffic":"%d{bypassed_traffic}","bypassed_etime":"%s{bypassed_etime}","flow_type":"%s{flow_type}","pcapid":"%s{pcapid}","productversion":"%s{productversion}","nsssvcip":"%s{nsssvcip}","eedone":"%s{eedone}"\}\}
      ```
   * Time Zone: `GMT`
6. Click **Save**.
7. **Activate** your changes.

### ZIA Firewall Logs

1. From the ZIA console, go to **Administration** > **Nanolog Streaming Service**.
2. Select the **Cloud NSS Feeds** tab. Then, click on **Add Cloud NSS Feed**.
3. In the **General** section, enter or select the following values:
   * Feed Name: `<YOUR_FEED_NAME>`
   * NSS Type: `NSS for Firewall`
   * Status: `Enabled`
4. In the **SIEM Connectivity** section, enter or select the following values:
   * SIEM Type: `Other`
   * API URL: The URL you copied in previous section `Retrieve the Datadog Webhook URL`
   * HTTP headers:
      * Key: `Content-Type`; Value: `application/json`
5. In the **Formatting** section, enter or select the following values:
   * Log Type: `Firewall Logs`
   * Feed Output Type: `JSON`
   * Feed Escape Character: `,\"`
   * Please use the below feed output format:
      ```
      \{"sourcetype":"zscalernss-fw","event":\{"datetime":"%d{yy}-%02d{mth}-%02d{dd} %02d{hh}:%02d{mm}:%02d{ss}","user":"%s{login}","department":"%s{dept}","locationname":"%s{location}","cdport":"%d{cdport}","csport":"%d{csport}","sdport":"%d{sdport}","ssport":"%d{ssport}","csip":"%s{csip}","cdip":"%s{cdip}","ssip":"%s{ssip}","sdip":"%s{sdip}","tsip":"%s{tsip}","tunsport":"%d{tsport}","tuntype":"%s{ttype}","action":"%s{action}","dnat":"%s{dnat}","stateful":"%s{stateful}","aggregate":"%s{aggregate}","nwsvc":"%s{nwsvc}","nwapp":"%s{nwapp}","proto":"%s{ipproto}","ipcat":"%s{ipcat}","destcountry":"%s{destcountry}","avgduration":"%d{avgduration}","rulelabel":"%s{rulelabel}","inbytes":"%ld{inbytes}","outbytes":"%ld{outbytes}","duration":"%d{duration}","durationms":"%d{durationms}","numsessions":"%d{numsessions}","ipsrulelabel":"%s{ipsrulelabel}","threatcat":"%s{threatcat}","threatname":"%s{threatname}","deviceowner":"%s{deviceowner}","devicehostname":"%s{devicehostname}","cdfqdn":"%s{cdfqdn}","srcip_country":"%s{srcip_country}","threat_score":"%d{threat_score}","threatseverity":"%s{threat_severity}","ips_custom_signature":"%d{ips_custom_signature}","dnatrulelabel":"%s{dnatrulelabel}","recordid":"%d{recordid}","pcapid":"%s{pcapid}","eedone":"%s{eedone}","devicemodel":"%s{devicemodel}","devicename":"%s{devicename}","deviceostype":"%s{deviceostype}","deviceosversion":"%s{deviceosversion}","deviceappversion":"%s{deviceappversion}","external_deviceid":"%s{external_deviceid}","ztunnelversion":"%s{ztunnelversion}","bypassed_session":"%d{bypassed_session}","bypass_etime":"%s{bypass_etime}","flow_type":"%s{flow_type}","datacenter":"%s{datacenter}","datacentercity":"%s{datacentercity}","datacentercountry":"%s{datacentercountry}","rdr_rulename":"%s{rdr_rulename}","fwd_gw_name":"%s{fwd_gw_name}","zpa_app_seg_name":"%s{zpa_app_seg_name}"\}\}
      ```
   * Time Zone: `GMT`
6. Click **Save**.
7. **Activate** your changes.

### ZIA DNS Logs

1. From the ZIA console, go to **Administration** > **Nanolog Streaming Service**.
2. Select the **Cloud NSS Feeds** tab. Then, click on **Add Cloud NSS Feed**.
3. In the **General** section, enter or select the following values:
   * Feed Name: `<YOUR_FEED_NAME>`
   * NSS Type: `NSS for Firewall`
   * Status: `Enabled`
4. In the **SIEM Connectivity** section, enter or select the following values:
   * SIEM Type: `Other`
   * API URL: The URL you copied in previous section `Retrieve the Datadog Webhook URL`
   * HTTP headers:
      * Key: `Content-Type`; Value: `application/json`
5. In the **Formatting** section, enter or select the following values:
   * Log Type: `DNS Logs`
   * Feed Output Type: `JSON`
   * Feed Escape Character: `,\"`
   * Please use the below feed output format:
      ```
      \{"sourcetype":"zscalernss-dns","event":\{"datetime":"%d{yy}-%02d{mth}-%02d{dd} %02d{hh}:%02d{mm}:%02d{ss}","user":"%s{login}","department":"%s{dept}","location":"%s{location}","reqaction":"%s{reqaction}","resaction":"%s{resaction}","reqrulelabel":"%s{reqrulelabel}","resrulelabel":"%s{resrulelabel}","dns_reqtype":"%s{reqtype}","dns_req":"%s{req}","dns_resp":"%s{res}","srv_dport":"%d{sport}","durationms":"%d{durationms}","clt_sip":"%s{cip}","srv_dip":"%s{sip}","category":"%s{domcat}","deviceowner":"%s{deviceowner}","devicehostname":"%s{devicehostname}","ecs_slot":"%s{ecs_slot}","dnsgw_slot":"%s{dnsgw_slot}","istcp":"%d{istcp}","recordid":"%d{recordid}","pcapid":"%s{pcapid}","respipcat":"%s{respipcat}","restype":"%s{restype}","eedone":"%s{eedone}","error":"%s{error}","ecs_prefix":"%s{ecs_prefix}","dnsgw_srv_proto":"%s{dnsgw_srv_proto}","dnsgw_flags":"%s{dnsgw_flags}","http_code":"%s{http_code}","dnsappcat":"%s{dnsappcat}","dnsapp":"%s{dnsapp}","protocol":"%s{protocol}","company":"%s{company}","cloudname":"%s{cloudname}","devicename":"%s{devicename}","devicemodel":"%s{devicemodel}","deviceosversion":"%s{deviceosversion}","deviceostype":"%s{deviceostype}","deviceappversion":"%s{deviceappversion}","devicetype":"%s{devicetype}","datacenter":"%s{datacenter}","datacentercity":"%s{datacentercity}","datacentercountry":"%s{datacentercountry}"\}\}
      ```
   * Time Zone: `GMT`
6. Click **Save**.
7. **Activate** your changes.

### ZIA Tunnel Logs

1. From the ZIA console, go to **Administration** > **Nanolog Streaming Service**.
2. Select the **Cloud NSS Feeds** tab. Then, click on **Add Cloud NSS Feed**.
3. In the **General** section, enter or select the following values:
   * Feed Name: `<YOUR_FEED_NAME>`
   * NSS Type: `NSS for Web`
   * Status: `Enabled`
4. In the **SIEM Connectivity** section, enter or select the following values:
   * SIEM Type: `Other`
   * API URL: The URL you copied in previous section `Retrieve the Datadog Webhook URL`
   * HTTP headers:
      * Key: `Content-Type`; Value: `application/json`
5. In the **Formatting** section, enter or select the following values:
   * Log Type: `Tunnel`
   * Record Type: Specify the tunnel log record types. The supported record types are: IKE Phase 1, IKE Phase 2, Sample, and Tunnel Event.
   * Feed Output Type: `JSON`
   * Feed Escape Character: `,\"`
   * Time Zone: `GMT`
6. In the **FEED OUTPUT FORMAT** section, Please use the below feed output format based on each record type.
   * IKE Phase 1
      ```
      \{"sourcetype":"zscalernss-tunnel","event":\{"datetime":"%d{yy}-%02d{mth}-%02d{dd} %02d{hh}:%02d{mm}:%02d{ss}","destinationport":"%d{dstport}","tunneltype":"IPSEC IKEV %d{ikeversion}","ikeversion":"%d{ikeversion}","lifetime":"%d{lifetime}","recordid":"%d{recordid}","sourceport":"%d{srcport}","spi_in":"%lu{spi_in}","spi_out":"%lu{spi_out}","algo":"%s{algo}","authentication":"%s{authentication}","authtype":"%s{authtype}","destinationip":"%s{destvip}","location":"%s{locationname}","sourceip":"%s{sourceip}","Recordtype":"%s{tunnelactionname}","vendorname":"%s{vendorname}","user":"%s{vpncredentialname}"\}\}
      ```
   * IKE Phase 2
      ```
      \{"sourcetype":"zscalernss-tunnel","event":\{"datetime":"%d{yy}-%02d{mth}-%02d{dd} %02d{hh}:%02d{mm}:%02d{ss}","tunneltype":"IPSEC IKEV %d{ikeversion}","destportstart":"%d{destportstart}","ikeversion":"%d{ikeversion}","lifebytes":"%d{lifebytes}","lifetime":"%d{lifetime}","recordid":"%d{recordid}","spi":"%d{spi}","srcportstart":"%d{srcportstart}","algo":"%s{algo}","authentication":"%s{authentication}","authtype":"%s{authtype}","destipend":"%s{destipend}","destipstart":"%s{destipstart}","destinationip":"%s{destvip}","location":"%s{locationname}","protocol":"%s{protocol}","sourceip":"%s{sourceip}","srcipend":"%s{srcipend}","srcipstart":"%s{srcipstart}","Recordtype":"%s{tunnelactionname}","tunnelprotocol":"%s{tunnelprotocol}","user":"%s{vpncredentialname}"\}\}
      ```
   * Tunnel Event
      ```
      \{"sourcetype":"zscalernss-tunnel","event":\{"datetime":"%d{yy}-%02d{mth}-%02d{dd} %02d{hh}:%02d{mm}:%02d{ss}","recordid":"%d{recordid}","sourceport":"%d{srcport}","destinationip":"%s{destvip}","tunnelstatus":"%s{event}","tunnelstatusreason":"%s{eventreason}","location":"%s{locationname}","sourceip":"%s{sourceip}","Recordtype":"%s{tunnelactionname}","user":"%s{vpncredentialname}","tunneltype":"%s{tunneltype}"\}\}
      ```
   * Sample
      ```
      \{"sourcetype":"zscalernss-tunnel","event":\{"datetime":"%d{yy}-%02d{mth}-%02d{dd} %02d{hh}:%02d{mm}:%02d{ss}","dpdrec":"%d{dpdrec}","recordid":"%d{recordid}","rxpackets":"%d{rxpackets}","sourceport":"%d{srcport}","txpackets":"%d{txpackets}","rxbytes":"%lu{rxbytes}","txbytes":"%lu{txbytes}","destinationip":"%s{destvip}","location":"%s{locationname}","sourceip":"%s{sourceip}","Recordtype":"%s{tunnelactionname}","user":"%s{vpncredentialname}","tunneltype":"%s{tunneltype}"\}\}
      ```
7. Click **Save**.
8. **Activate** your changes.

### ZIA SaaS Security Logs

1. From the ZIA console, go to **Administration** > **Nanolog Streaming Service**.
2. Select the **Cloud NSS Feeds** tab. Then, click on **Add Cloud NSS Feed**.
3. In the **General** section, enter or select the following values:
   * Feed Name: `<YOUR_FEED_NAME>`
   * NSS Type: `NSS for Web`
   * Status: `Enabled`
4. In the **SIEM Connectivity** section, enter or select the following values:
   * SIEM Type: `Other`
   * API URL: The URL you copied in previous section `Retrieve the Datadog Webhook URL`
   * HTTP headers:
      * Key: `Content-Type`; Value: `application/json`
5. In the **Formatting** section, enter or select the following values:
   * Log Type: `SaaS Security`
      * **NOTE**: Please create a separate NSS feed for each application category. Ensure that the appropriate output format is used according to the specific application category.
   * Application Category: Choose an application category. The supported application categories are: Collaboration, CRM, Email, File, ITSM, Public Cloud Storage and Repository.
   * Feed Output Type: `JSON`
   * Feed Escape Character: `,\"`
   * Please use the below feed output format for collaboration:
      ```
      \{"sourcetype":"zscalernss-casb","event":\{"subtype":"collaboration","datetime":"%d{yy}-%02d{mth}-%02d{dd} %02d{hh}:%02d{mm}:%02d{ss}","dlpidentifier":"%d{dlpidentifier}","recordid":"%d{recordid}","any_incident":"%s{any_incident}","channel_name":"%s{channel_name}","datacenter":"%s{datacenter}","datacentercity":"%s{datacentercity}","datacentercountry":"%s{datacentercountry}","company":"%s{company}","login":"%s{owner}","tenant":"%s{tenant}","department":"%s{department}","applicationname":"%s{applicationname}","threatname":"%s{threatname}","policy":"%s{policy}","dlpdictionaries":"%s{dlpdictnames}","dlpdicthitcount":"%s{dlpdictcount}","external_recptnames":"%s{external_recptnames}","internal_recptnames":"%s{internal_recptnames}","extownername":"%s{extownername}","malware":"%s{malware}","malwareclass":"%s{malwareclass}","messageid":"%s{msgid}","rulelabel":"%s{rulelabel}","ruletype":"%s{ruletype}","sender":"%s{sender}","severity":"%s{severity}","sharedchannel_hostname":"%s{sharedchannel_hostname}","upload_doctypename":"%s{upload_doctypename}","dlpengine":"%s{dlpenginenames}"\}\}
      ```
   * Please use the below feed output format for CRM:
      ```
      \{"sourcetype":"zscalernss-casb","event":\{"subtype":"crm","datetime":"%d{yy}-%02d{mth}-%02d{dd} %02d{hh}:%02d{mm}:%02d{ss}","dlpidentifier":"%d{dlpidentifier}","filesize":"%d{filesize}","num_external_collab":"%d{num_external_collab}","num_internal_collab":"%d{num_internal_collab}","recordid":"%d{recordid}","collabscope":"%s{collabscope}","company":"%s{company}","component":"%s{component}","datacenter":"%s{datacenter}","datacentercity":"%s{datacentercity}","datacentercountry":"%s{datacentercountry}","login":"%s{owner}","tenant":"%s{tenant}","department":"%s{department}","applicationname":"%s{applicationname}","threatname":"%s{threatname}","policy":"%s{policy}","dlpdictionaries":"%s{dlpdictnames}","dlpdicthitcount":"%s{dlpdictcount}","external_collabnames":"%s{external_collabnames}","extownername":"%s{extownername}","file_msg_id":"%s{file_msg_id}","file_msg_mod_time":"%s{file_msg_mod_time}","filemd5":"%s{filemd5}","filename":"%s{filename}","filepath":"%s{filepath}","filetypecategory":"%s{filetypecategory}","fullurl":"%s{fullurl}","hostname":"%s{hostname}","internal_collabnames":"%s{internal_collabnames}","malware":"%s{malware}","malwareclass":"%s{malwareclass}","objectname":"%s{objectname}","objecttype":"%s{objecttype}","rulelabel":"%s{rulelabel}","ruletype":"%s{ruletype}","severity":"%s{severity}","sha":"%s{sha}","upload_doctypename":"%s{upload_doctypename}","dlpengine":"%s{dlpenginenames}"\}\}
      ```
   * Please use the below feed output format for email:
      ```
      \{"sourcetype":"zscalernss-casb","event":\{"subtype":"email","datetime":"%d{yy}-%02d{mth}-%02d{dd} %02d{hh}:%02d{mm}:%02d{ss}","recordid":"%d{recordid}","company":"%s{company}","tenant":"%s{tenant}","login":"%s{owner}","department":"%s{department}","applicationname":"%s{applicationname}","threatname":"%s{threatname}","policy":"%s{policy}","message":"%s{messageid}","dlpdictionaries":"%s{dlpdictnames}","dlpdicthitcount":"%s{dlpdictcount}","companyid":"%d{companyid}","dlpidentifier":"%d{dlpidentifier}","filedownloadtimems":"%d{filedownloadtimems}","filescantimems":"%d{filescantimems}","msgsize":"%d{msgsize}","num_ext_recpts":"%d{num_ext_recpts}","num_int_recpts":"%d{num_int_recpts}","repochtime":"%d{repochtime}","any_incident":"%s{any_incident}","filename":"%s{attchcomponentfilenames}","filesize":"%s{attchcomponentfilesizes}","filetype":"%s{attchcomponentfiletypes}","filemd5":"%s{attchcomponentmd5s}","datacenter":"%s{datacenter}","datacentercity":"%s{datacentercity}","datacentercountry":"%s{datacentercountry}","extownername":"%s{externalownername}","external_recptnames":"%s{extrecptnames}","internal_recptnames":"%s{intrecptnames}","is_inbound":"%s{is_inbound}","malware":"%s{malware}","malwareclass":"%s{malwareclass}","messageid":"%s{messageid}","rtime":"%s{rtime}","rulelabel":"%s{rulelabel}","ruletype":"%s{ruletype}","severity":"%s{severity}","upload_doctypename":"%s{upload_doctypename}","dlpengine":"%s{dlpenginenames}"\}\}
      ```
   * Please use the below feed output format for file:
      ```
      \{"sourcetype":"zscalernss-casb","event":\{"subtype":"file","datetime":"%d{yy}-%02d{mth}-%02d{dd} %02d{hh}:%02d{mm}:%02d{ss}","recordid":"%d{recordid}","company":"%s{company}","tenant":"%s{tenant}","login":"%s{user}","department":"%s{department}","applicationname":"%s{applicationname}","filename":"%s{filename}","filesource":"%s{filesource}","filemd5":"%s{filemd5}","threatname":"%s{threatname}","policy":"%s{policy}","dlpdictionaries":"%s{dlpdictnames}","dlpdicthitcount":"%s{dlpdictcount}","dlpengine":"%s{dlpenginenames}","fullurl":"%s{fullurl}","lastmodtime":"%s{lastmodtime}","filescantimems":"%d{filescantimems}","dlpidentifier":"%d{dlpidentifier}","epochlastmodtime":"%d{epochlastmodtime}","filesize":"%d{filesize}","collabscope":"%s{collabscope}","datacenter":"%s{datacenter}","datacentercity":"%s{datacentercity}","datacentercountry":"%s{datacentercountry}","extcollab_groups":"%s{extcollab_groups}","external_collabnames":"%s{extcollabnames}","extownername":"%s{extownername}","fileid":"%s{fileid}","filetypename":"%s{filetypename}","hostname":"%s{hostname}","intcollab_groups":"%s{intcollab_groups}","internal_collabnames":"%s{intcollabnames}","malware":"%s{malware}","malwareclass":"%s{malwareclass}","rulelabel":"%s{rulelabel}","ruletype":"%s{ruletype}","severity":"%s{severity}","suburl":"%s{suburl}","upload_doctypename":"%s{upload_doctypename}","filedownloadtimems":"%d{filedownloadtimems}"\}\}
      ```
   * Please use the below feed output format for ITSM:
      ```
      \{"sourcetype":"zscalernss-casb","event":\{"subtype":"itsm","datetime":"%d{yy}-%02d{mth}-%02d{dd} %02d{hh}:%02d{mm}:%02d{ss}","company":"%s{company}","login":"%s{owner}","tenant":"%s{tenant}","department":"%s{department}","applicationname":"%s{applicationname}","threatname":"%s{threatname}","policy":"%s{policy}","dlpdictionaries":"%s{dlpdictnames}","dlpdicthitcount":"%s{dlpdictcount}","dlpidentifier":"%d{dlpidentifier}","filesize":"%d{filesize}","num_external_collab":"%d{num_external_collab}","num_internal_collab":"%d{num_internal_collab}","recordid":"%d{recordid}","component":"%s{component}","datacenter":"%s{datacenter}","datacentercity":"%s{datacentercity}","datacentercountry":"%s{datacentercountry}","external_collabnames":"%s{external_collabnames}","extownername":"%s{extownername}","file_msg_id":"%s{file_msg_id}","file_msg_mod_time":"%s{file_msg_mod_time}","filemd5":"%s{filemd5}","filename":"%s{filename}","filepath":"%s{filepath}","filetypecategory":"%s{filetypecategory}","fullurl":"%s{fullurl}","hostname":"%s{hostname}","internal_collabnames":"%s{internal_collabnames}","malware":"%s{malware}","malwareclass":"%s{malwareclass}","objectname":"%s{objectname}","objecttype":"%s{objecttype}","rulelabel":"%s{rulelabel}","ruletype":"%s{ruletype}","severity":"%s{severity}","sha":"%s{sha}","upload_doctypename":"%s{upload_doctypename}","dlpengine":"%s{dlpenginenames}"\}\}
      ```
   * Please use the below feed output format for public cloud storage:
      ```
      \{"sourcetype":"zscalernss-casb","event":\{"subtype":"public-cloud-storage","datetime":"%d{yy}-%02d{mth}-%02d{dd} %02d{hh}:%02d{mm}:%02d{ss}","recordid":"%d{recordid}","company":"%s{company}","tenant":"%s{tenant}","owner":"%s{owner}","department":"%s{department}","applicationname":"%s{applicationname}","filename":"%s{filename}","filesource":"%s{filesource}","filemd5":"%s{filemd5}","threatname":"%s{threatname}","policy":"%s{policy}","dlpdictionaries":"%s{dlpdictnames}","dlpdicthitcount":"%s{dlpdictcount}","dlpengine":"%s{dlpenginenames}","fullurl":"%s{fullurl}","lastmodtime":"%s{lastmodtime}","bucketid":"%d{bucketid}","dlpidentifier":"%d{dlpidentifier}","numcollab":"%d{numcollab}","bucketowner":"%s{bucketowner}","collabnames":"%s{collabnames}","datacenter":"%s{datacenter}","datacentercity":"%s{datacentercity}","datacentercountry":"%s{datacentercountry}","extownername":"%s{extownername}","fileid":"%s{fileid}","hostname":"%s{hostname}","malware":"%s{malware}","malwareclass":"%s{malwareclass}","rulelabel":"%s{rulelabel}","ruletype":"%s{ruletype}","severity":"%s{severity}","upload_doctypename":"%s{upload_doctypename}","bucketname":"%s{bucketname}"\}\}
      ```
   * Please use the below feed output format for repository:
      ```
      \{"sourcetype":"zscalernss-casb","event":\{"subtype":"repository","datetime":"%d{yy}-%02d{mth}-%02d{dd} %02d{hh}:%02d{mm}:%02d{ss}","company":"%s{company}","login":"%s{owner}","tenant":"%s{tenant}","department":"%s{department}","applicationname":"%s{applicationname}","threatname":"%s{threatname}","policy":"%s{policy}","dlpdictionaries":"%s{dlpdictnames}","dlpdicthitcount":"%s{dlpdictcount}","dlpidentifier":"%d{dlpidentifier}","filesize":"%d{filesize}","num_external_collab":"%d{num_external_collab}","recordid":"%d{recordid}","datacenter":"%s{datacenter}","datacentercity":"%s{datacentercity}","datacentercountry":"%s{datacentercountry}","external_collabnames":"%s{external_collabnames}","extownername":"%s{extownername}","fileid":"%s{fileid}","filemd5":"%s{filemd5}","filename":"%s{filename}","filepath":"%s{filepath}","filetypecategory":"%s{filetypecategory}","malware":"%s{malware}","malwareclass":"%s{malwareclass}","projectname":"%s{projectname}","reponame":"%s{reponame}","rulelabel":"%s{rulelabel}","ruletype":"%s{ruletype}","severity":"%s{severity}","sha":"%s{sha}","upload_doctypename":"%s{upload_doctypename}","dlpengine":"%s{dlpenginenames}"\}\}
      ```
   * Time Zone: `GMT`
6. Click **Save**.
7. **Activate** your changes.

### ZIA SaaS Security Activity Logs

1. From the ZIA console, go to **Administration** > **Nanolog Streaming Service**.
2. Select the **Cloud NSS Feeds** tab. Then, click on **Add Cloud NSS Feed**.
3. In the **General** section, enter or select the following values:
   * Feed Name: `<YOUR_FEED_NAME>`
   * NSS Type: `NSS for Web`
   * Status: `Enabled`
4. In the **SIEM Connectivity** section, enter or select the following values:
   * SIEM Type: `Other`
   * API URL: The URL you copied in previous section `Retrieve the Datadog Webhook URL`
   * HTTP headers:
      * Key: `Content-Type`; Value: `application/json`
5. In the **Formatting** section, enter or select the following values:
   * Log Type: `SaaS Security Activity`
   * Feed Output Type: `JSON`
   * Feed Escape Character: `,\"`
   * Please use the below feed output format:
      ```
      \{"sourcetype":"zscalernss-casb","event":\{"subtype":"activity","datetime":"%d{yy}-%02d{mth}-%02d{dd} %02d{hh}:%02d{mm}:%02d{ss}","login":"%s{username}","tenant":"%s{tenant}","applicationname":"%s{appname}","object_name_1":"%s{objnames1}","object_name_2":"%s{objnames2}","is_admin_act":"%s{is_admin_act}","object_type_name_1":"%s{objtypename1}","object_type_name_2":"%s{objtypename2}","activity_count":"%d{act_cnt}","activity_type_name":"%s{act_type_name}","event_time":"%s{eventtime}","external_owner_name":"%s{extownername}","src_ip":"%s{src_ip}"\}\}
      ```
   * Time Zone: `GMT`
6. Click **Save**.
7. **Activate** your changes.

### ZIA Admin Audit Logs

1. From the ZIA console, go to **Administration** > **Nanolog Streaming Service**.
2. Select the **Cloud NSS Feeds** tab. Then, click on **Add Cloud NSS Feed**.
3. In the **General** section, enter or select the following values:
   * Feed Name: `<YOUR_FEED_NAME>`
   * NSS Type: `NSS for Web`
   * Status: `Enabled`
4. In the **SIEM Connectivity** section, enter or select the following values:
   * SIEM Type: `Other`
   * API URL: The URL you copied in previous section `Retrieve the Datadog Webhook URL`
   * HTTP headers:
      * Key: `Content-Type`; Value: `application/json`
5. In the **Formatting** section, enter or select the following values:
   * Log Type: `Admin Audit`
   * Feed Output Type: `JSON`
   * Feed Escape Character: `,\"`
   * Please use the below feed output format:
      ```
      \{ "sourcetype" : "zscalernss-audit", "event" :\{"datetime":"%d{yy}-%02d{mth}-%02d{dd} %02d{hh}:%02d{mm}:%02d{ss}","recordid":"%d{recordid}","action":"%s{action}","category":"%s{category}","subcategory":"%s{subcategory}","resource":"%s{resource}","interface":"%s{interface}","adminid":"%s{adminid}","clientip":"%s{clientip}","result":"%s{result}","errorcode":"%s{errorcode}","auditlogtype":"%s{auditlogtype}","preaction":%s{preaction},"postaction":%s{postaction}\}\}
      ```
   * Time Zone: `GMT`
6. Click **Save**.
7. **Activate** your changes.

### ZIA Endpoint DLP Logs

1. From the ZIA console, go to **Administration** > **Nanolog Streaming Service**.
2. Select the **Cloud NSS Feeds** tab. Then, click on **Add Cloud NSS Feed**.
3. In the **General** section, enter or select the following values:
   * Feed Name: `<YOUR_FEED_NAME>`
   * NSS Type: `NSS for Web`
   * Status: `Enabled`
4. In the **SIEM Connectivity** section, enter or select the following values:
   * SIEM Type: `Other`
   * API URL: The URL you copied in previous section `Retrieve the Datadog Webhook URL`
   * HTTP headers:
      * Key: `Content-Type`; Value: `application/json`
5. In the **Formatting** section, enter or select the following values:
   * Log Type: `Endpoint DLP`
   * Feed Output Type: `JSON`
   * Feed Escape Character: `,\"`
   * Please use the below feed output format:
      ```
      \{"sourcetype":"zscalernss-endpointdlp","event":\{"datetime":"%d{yy}-%02d{mth}-%02d{dd} %02d{hh}:%02d{mm}:%02d{ss}","scantime":"%llu{scantime}","numdlpengine":"%u{numdlpengids}","numdlpdict":"%u{numdlpdictids}","recordid":"%llu{recordid}","scannedbytes":"%llu{scanned_bytes}","dlpidentifier":"%llu{dlpidentifier}","user":"%s{user}","department":"%s{department}","devicename":"%s{devicename}","devicetype":"%s{devicetype}","deviceostype":"%s{deviceostype}","deviceplatform":"%s{deviceplatform}","deviceosversion":"%s{deviceosversion}","devicemodel":"%s{devicemodel}","deviceappversion":"%s{deviceappversion}","deviceowner":"%s{deviceowner}","devicehostname":"%s{devicehostname}","datacenter":"%s{datacenter}","datacentercity":"%s{datacentercity}","datacentercountry":"%s{datacentercountry}","filesrcpath":"%s{filesrcpath}","filedstpath":"%s{filedstpath}","filemd5":"%s{filemd5}","filesha":"%s{filesha}","filetypename":"%s{filetypename}","filetypecategory":"%s{filetypecategory}","filedoctype":"%s{filedoctype}","itemtype":"%s{itemtype}","srctype":"%s{srctype}","dsttype":"%s{dsttype}","itemname":"%s{itemname}","itemsrcname":"%s{itemsrcname}","itemdstname":"%s{itemdstname}","dlpengine":"%s{dlpengnames}","dlpdictionaries":"%s{dlpdictnames}","dlpdicthitcount":"%s{dlpcounts}","confirmaction":"%s{confirmaction}","actiontaken":"%s{actiontaken}","severity":"%s{severity}","triggeredrule":"%s{triggeredrulelabel}","otherrulelabels":"%s{otherrulelabels}","logtype":"%s{logtype}","channel":"%s{channel}","activitytype":"%s{activitytype}","expectedaction":"%s{expectedaction}","zdpmode":"%s{zdpmode}","additionalinfo":"%s{addinfo}","confirmjustification":"%s{confirmjust}"\}\}
      ```
   * Time Zone: `GMT`
6. Click **Save**.
7. **Activate** your changes.

### ZIA Email DLP Logs

1. From the ZIA console, go to **Administration** > **Nanolog Streaming Service**.
2. Select the **Cloud NSS Feeds** tab. Then, click on **Add Cloud NSS Feed**.
3. In the **General** section, enter or select the following values:
   * Feed Name: `<YOUR_FEED_NAME>`
   * NSS Type: `NSS for Web`
   * Status: `Enabled`
4. In the **SIEM Connectivity** section, enter or select the following values:
   * SIEM Type: `Other`
   * API URL: The URL you copied in previous section `Retrieve the Datadog Webhook URL`
   * HTTP headers:
      * Key: `Content-Type`; Value: `application/json`
5. In the **Formatting** section, enter or select the following values:
   * Log Type: `Email DLP`
   * Feed Output Type: `JSON`
   * Feed Escape Character: `,\"`
   * Please use the below feed output format:
      ```
      \{"sourcetype":"zscalernss-emaildlp","event":\{"datetime":"%d{yy}-%02d{mth}-%02d{dd} %02d{hh}:%02d{mm}:%02d{ss}","datacenter":"%s{datacenter}","datacentercity":"%s{datacentercity}","datacentercountry":"%s{datacentercountry}","company":"%s{company}","department":"%s{departmentname}","user":"%s{username}","extusername":"%s{extusername}","owner":"%s{owner}","sender":"%s{sender}","mail_sent_time":"%s{mail_sent_time}","epochmail_sent_time":"%s{epochmail_sent_time}","tenant":"%s{tenant}","appname":"%s{appname}","messageid":"%s{msgid}","subject":"%s{subject}","md5s":"%s{ac_md5s}","sizes":"%s{ac_sizes}","filetypes":"%s{ac_filetypes}","doctypes":"%s{ac_doctypes}","filenames":"%s{ac_names}","triggered_recipients":"%s{trigg_rcpts}","other_recipients":"%s{other_rcpts}","triggered_recipients_domains":"%s{trigg_rcpt_doms}","other_recipients_domains":"%s{other_rcpt_doms}","scantime":"%llu{scan_time}","dlpidentifier":"%llu{dlpidentifier}","dlpdictionaries":"%s{dlpdictnames}","dlpdicthitcount":"%s{dlpdictcnts}","dlpengine":"%s{dlpengnames}","recordid":"%llu{recordid}","logtype":"%s{logtype}","severity":"%s{severity}","action":"%s{actions}","rulelabel":"%s{rulelabels}"\}\}
      ```
   * Time Zone: `GMT`
6. Click **Save**.
7. **Activate** your changes.

### ZIA Alert Logs

1. From the ZIA console, go to **Alerts** > **Webhooks**.
2. Click **Add Webhook**.
3. In the **Add Webhook** window:
   * Name: `<YOUR_FEED_NAME>`
   * Status: `Enabled`
   * URL: The URL you copied in previous section `Retrieve the Datadog Webhook URL`
   * Authentication Type: `Token`
   * Bearer Token: `<YOUR_DATADOG_API_KEY>`
4. Click **Save**.
5. **Activate** your changes.

## Data Collected

### Logs
The Zscaler integration collects Web, Firewall, DNS, Tunnel, SaaS Security, SaaS Security Activity, Admin Audit, Endpoint DLP, Email DLP and Alert logs.

### Metrics

The Zscaler integration does not include any metrics.

### Events

The Zscaler integration does not include any events.

## Support

For further assistance, contact [Datadog support][2].

[1]: https://www.zscaler.com/products/zscaler-internet-access
[2]: https://docs.datadoghq.com/help/
