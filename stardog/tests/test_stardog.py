import copy
import json
import threading

import requests
from six import PY3

from datadog_checks.base import ensure_bytes
from datadog_checks.stardog import StardogCheck

if PY3:
    from http.server import BaseHTTPRequestHandler, HTTPServer
else:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


HTTP = None
INSTANCE = {'username': 'admin', 'password': 'admin', 'tags': ['test1']}


def setup_module(module):
    global HTTP
    HTTP = HttpServerThread()
    HTTP.start()
    INSTANCE['stardog_url'] = 'http://localhost:{}'.format(HTTP.port)


def teardown_module(module):
    try:
        HTTP.end_http()
        HTTP.join()
    except requests.exceptions.ConnectionError:
        # The server is already down
        pass


def test_check_all_metrics(aggregator):
    """
    Testing Stardog check.
    """
    check = StardogCheck('stardog', {}, [copy.deepcopy(INSTANCE)])
    check.check({})
    tags = copy.deepcopy(INSTANCE['tags'])
    tags.append("stardog_url:http://localhost:%d" % HTTP.port)
    for metric_key in DATA:
        metric_name = "stardog.%s" % metric_key
        metric_val = DATA[metric_key]['value']
        aggregator.assert_metric(metric_name, count=1, value=metric_val, tags=tags)
    aggregator.assert_all_metrics_covered


class HttpServerThread(threading.Thread):
    def __init__(self):
        super(HttpServerThread, self).__init__()
        self.done = False
        self.hostname = 'localhost'

        class MockStardog(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path != '/admin/status':
                    self.send_response(404)
                    return
                if self.headers["Authorization"] != "Basic YWRtaW46YWRtaW4=":
                    self.send_response(401)
                    return
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                # json.dumps always outputs a str, wfile.write requires bytes
                self.wfile.write(ensure_bytes(json.dumps(DATA)))

        self.http = HTTPServer((self.hostname, 0), MockStardog)
        self.port = self.http.server_port

    def run(self):
        while not self.done:
            self.http.handle_request()

    def end_http(self):
        self.done = True
        # just a dummy get to wake it up
        requests.get("http://%s:%d" % (self.hostname, self.port))


DATA = {
    "dbms.mem.mapped.max": {"value": 120795955},
    "dbms.mem.direct.used": {"value": 11769009},
    "databases.system.planCache.size": {"value": 3},
    "system.uptime": {"value": 85571635},
    "dbms.mem.mapped.used": {"value": 8388608},
    "databases.system.planCache.ratio": {"value": 0.4},
    "dbms.mem.direct.buffer.used": {"value": 53248},
    "dbms.mem.heap.max": {"value": 2058354688},
    "dbms.mem.direct.pool.used": {"value": 0},
    "system.cpu.usage": {"value": 3.65916233046042e-4},
    "dbms.mem.heap.used": {"value": 223226480},
    "dbms.mem.direct.max": {"value": 1073741824},
    "dbms.mem.direct.buffer.max": {"value": 281857228},
    "dbms.mem.direct.pool.max": {"value": 402653184},
}
