# NS1 API endpoints that will be queried to retrieve statistics
NS1_ENDPOINTS = {
    # qps and usage stats account wide
    "qps.usage": "{apiendpoint}/v1/stats/{key}{query}",
    # qps and usage stats per zone
    "qps.usage.zone": r"{apiendpoint}/v1/stats/{key}/{domain}{query}",
    # qps and usage stats per dns record
    "qps.usage.record": r"{apiendpoint}/v1/stats/{key}/{domain}/{record}/{rectype}{query}",
    # ttl for zone
    "ttl": r"{apiendpoint}/v1/zones/{domain}",
    # account plan limits
    "billing": "{apiendpoint}/v1/account/billataglance",
    # pulsar decisions account wide
    "pulsar.decisions": "{apiendpoint}/v1/pulsar/query/decisions{query}",
    # pulsar insufficient decision data for account
    "pulsar.decisions.insufficient": "{apiendpoint}/v1/pulsar/query/decisions{query}",
    # pulsar all route map hits
    "pulsar.routemap.hit": "{apiendpoint}/v1/pulsar/query/routemap/hit/customer{query}",
    # pulsar all route map misses
    "pulsar.routemap.miss": "{apiendpoint}/v1/pulsar/query/routemap/miss/customer{query}",
    # pulsar aggregate performance data
    "pulsar.performance": "{apiendpoint}/v1/pulsar/apps/{app_id}/jobs/{job_id}/data{query}",
    # pulsar availability data
    "pulsar.availability": "{apiendpoint}/v1/pulsar/apps/{app_id}/jobs/{job_id}/availability{query}",
    # pulsar decisions for record
    "pulsar.decisions.record": "{apiendpoint}/v1/pulsar/query/decisions{query}",
    # View route map hits by record
    "pulsar.routemap.hit.record": "{apiendpoint}/v1/pulsar/query/routemap/hit/record/{rec_name}/{rec_type}{query}",
    # View route map misses by record
    "pulsar.routemap.miss.record": "{apiendpoint}/v1/pulsar/query/routemap/miss/record/{rec_name}/{rec_type}{query}",
}
