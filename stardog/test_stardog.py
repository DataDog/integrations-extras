import BaseHTTPServer
import json
import threading

import requests
from nose.plugins.attrib import attr

from tests.checks.common import AgentCheckTest


class HttpServerThread(threading.Thread):
    def __init__(self, data):
        super(HttpServerThread, self).__init__()
        self.done = False
        self.hostname = 'localhost'

        class MockStardog(BaseHTTPServer.BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path != '/admin/status':
                    self.send_response(404)
                    return

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(data))

        self.http = BaseHTTPServer.HTTPServer((self.hostname, 0), MockStardog)
        self.port = self.http.server_port

    def run(self):
            while not self.done:
                self.http.handle_request()

    def end_http(self):
        self.done = True
        # just a dummy get to wake it up
        requests.get("http://%s:%d" % (self.hostname, self.port))


@attr(requires='stardog')
class TestStardog(AgentCheckTest):
    """Basic Test for stardog integration."""
    CHECK_NAME = 'stardog'

    data = {"dbms.mem.mapped.max": {"value": 120795955},
            "dbms.mem.direct.used": {"value": 11769009},
            "databases.system.planCache.size": {"value": 3},
            "system.uptime": {"value": 85571635},
            "dbms.mem.mapped.used": {"value": 8388608},
            "databases.system.planCache.ratio": {"value": 0.4},
            "dbms.mem.direct.buffer.used": {"value": 53248},
            "dbms.mem.heap.max": {"value": 2058354688},
            "dbms.mem.direct.pool.used": {"value": 0},
            "system.cpu.usage": {"value": 3.65916233046042E-4},
            "dbms.mem.heap.used": {"value": 223226480},
            "dbms.mem.direct.max": {"value": 1073741824},
            "dbms.mem.direct.buffer.max": {"value": 281857228},
            "dbms.mem.direct.pool.max": {"value": 402653184}
            }

    def setUp(self):
        self.http = HttpServerThread(self.data)
        self.instance = {
            'stardog_url': "http://localhost:%d" % self.http.port,
            'username': 'admin',
            'password': 'admin',
            'tags': ['test1']}
        self.check_config = {'instances': [self.instance]}
        self.http.start()

    def tearDown(self):
        self.http.end_http()
        self.http.join()

    def test_check_all_metrics(self):
        """
        Testing Stardog check.
        """
        self.load_check(self.check_config, {})
        self.run_check_twice(self.check_config)
        tags = self.instance['tags']
        tags.append("stardog_url:http://localhost:%d" % self.http.port)
        for metric_key in self.data:
            metric_name = "stardog.%s" % metric_key
            metric_val = self.data[metric_key]['value']
            self.assertMetric(metric_name, count=1, value=metric_val, tags=tags)
        self.coverage_report()
