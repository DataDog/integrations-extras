import ast
import json

from flask import Flask, Response

app = Flask(__name__)


# V5 Test Routes
@app.route("/pass/admin/api.php")
def passResponse():
    dict = (
        '{"domains_being_blocked":125230,"dns_queries_today":13322,"ads_blocked_today":5490,'
        '"ads_percentage_today":41.21003,"unique_domains":928,"queries_forwarded":6702,'
        '"queries_cached":1130,"clients_ever_seen":4,"unique_clients":4,"dns_queries_all_types":13322,'
        '"reply_NODATA":12,"reply_NXDOMAIN":15,"reply_CNAME":173,"reply_IP":317,"privacy_level":0,"status":"enabled"}'
    )
    return Response(dict, status=200)


@app.route("/no_status/admin/api.php")
def no_status():
    dict = (
        '{"domains_being_blocked":125230,"dns_queries_today":13322,"ads_blocked_today":5490,'
        '"ads_percentage_today":41.21003,"unique_domains":928,"queries_forwarded":6702,"queries_cached":1130,'
        '"clients_ever_seen":4,"unique_clients":4,"dns_queries_all_types":13322,"reply_NODATA":12,'
        '"reply_NXDOMAIN":15,"reply_CNAME":173,"reply_IP":317,"privacy_level":0}'
    )
    return Response(dict, status=200)


@app.route("/bad_status/admin/api.php")
def bad_status():
    dict = (
        '{"domains_being_blocked":125230,"dns_queries_today":13322,"ads_blocked_today":5490,'
        '"ads_percentage_today":41.21003,"unique_domains":928,"queries_forwarded":6702,'
        '"queries_cached":1130,"clients_ever_seen":4,"unique_clients":4,"dns_queries_all_types":13322,'
        '"reply_NODATA":12,"reply_NXDOMAIN":15,"reply_CNAME":173,"reply_IP":317,"privacy_level":0,'
        '"status":"running"}'
    )
    return Response(dict, status=200)


@app.route("/fail/admin/api.php")
def FailResponse():
    dict = (
        '{"domains_being_blocked":125230,"dns_queries_today":13322,"ads_blocked_today":5490,'
        '"ads_percentage_today":41.21003,"unique_domains":928,"queries_forwarded":6702,"queries_cached":1130,'
        '"clients_ever_seen":4,"unique_clients":4,"dns_queries_all_types":13322,"reply_NODATA":12,'
        '"reply_NXDOMAIN":15,"reply_CNAME":173,"reply_IP":317,"privacy_level":0,"status":"enabled"}'
    )
    return Response(dict, status=404)


# v6 Test Routes
@app.route("/v6/bad_auth")
def no_auth_response():
    dict = '{"error":{"key":"not_found","message":"Not found","hint":"/api"},"took":6.0796737670898438e-05}'
    return Response(dict, status=401)


@app.route("/api/auth", methods=['GET', 'POST'])
def auth():
    data = (
        "{'session': {'valid': True, 'totp': False, 'sid': 'p6ldWvLNFpJCx2ZUwXVQsw=', "
        "'csrf': 'Jm4BPShHjQGPCkzVw6VZ4w=', 'validity': 1800, "
        "'message': 'password correct'}, 'took': 0.13656830787658691}"
    )
    data_dict = ast.literal_eval(data)
    json_string = json.dumps(data_dict)
    return Response(json_string, status=200)


@app.route("/api/stats/summary")
def metrics():
    dict = (
        '{"queries":{"total":0,"blocked":0,"percent_blocked":0,"unique_domains":0,'
        '"forwarded":0,"cached":0,"frequency":0,"types":{"A":0,"AAAA":0,"ANY":0,'
        '"SRV":0,"SOA":0,"PTR":0,"TXT":0,"NAPTR":0,"MX":0,"DS":0,"RRSIG":0,'
        '"DNSKEY":0,"NS":0,"SVCB":0,"HTTPS":0,"OTHER":0},"status":{"UNKNOWN":0,'
        '"GRAVITY":0,"FORWARDED":0,"CACHE":0,"REGEX":0,"DENYLIST":0,'
        '"EXTERNAL_BLOCKED_IP":0,"EXTERNAL_BLOCKED_NULL":0,'
        '"EXTERNAL_BLOCKED_NXRA":0,"GRAVITY_CNAME":0,"REGEX_CNAME":0,'
        '"DENYLIST_CNAME":0,"RETRIED":0,"RETRIED_DNSSEC":0,"IN_PROGRESS":0,'
        '"DBBUSY":0,"SPECIAL_DOMAIN":0,"CACHE_STALE":0,'
        '"EXTERNAL_BLOCKED_EDE15":0},"replies":{"UNKNOWN":0,"NODATA":0,'
        '"NXDOMAIN":0,"CNAME":0,"IP":0,"DOMAIN":0,"RRNAME":0,"SERVFAIL":0,'
        '"REFUSED":0,"NOTIMP":0,"OTHER":0,"DNSSEC":0,"NONE":0,"BLOB":0}},'
        '"clients":{"active":0,"total":0},"gravity":{"domains_being_blocked":79984,'
        '"last_update":1759837296},"took":4.076957702636719e-05}'
    )

    return Response(dict, status=200)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888)
