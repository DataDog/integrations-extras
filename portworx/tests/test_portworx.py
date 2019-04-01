import BaseHTTPServer
import threading

import requests
from nose.plugins.attrib import attr
from tests.checks.common import AgentCheckTest

class HttpServerThread(threading.Thread):
    def __init__(self, data):
        super(HttpServerThread, self).__init__()
        self.done = False
        self.hostname = 'localhost'
        self.port = 1337

        class MockPortworx(BaseHTTPServer.BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path != '/metrics':
                    self.send_response(404)
                    return

                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(data)

        self.http = BaseHTTPServer.HTTPServer((self.hostname, self.port), MockPortworx)

    def run(self):
            while not self.done:
                self.http.handle_request()

    def end_http(self):
        self.done = True
        # just a dummy get to wake it up
        requests.get("http://%s:%d" % (self.hostname, self.port))


@attr(requires='portworx')
class TestPortworx(AgentCheckTest):
    """Basic Test for portworx integration."""
    CHECK_NAME = 'portworx'


    data = ("""px_cluster_cpu_percent{cluster="clusterpaul",node="devbox",node_id="f6c68c67-7c4f-4b3b-ab50-f5a046be5c3d"} 0.76
px_cluster_disk_available_bytes{cluster="clusterpaul",node="devbox",node_id="f6c68c67-7c4f-4b3b-ab50-f5a046be5c3d"} 1.3470091182e+11
px_cluster_disk_total_bytes{cluster="clusterpaul",node="devbox",node_id="f6c68c67-7c4f-4b3b-ab50-f5a046be5c3d"} 1.37438953472e+11
px_cluster_disk_utilized_bytes{cluster="clusterpaul",node="devbox",node_id="f6c68c67-7c4f-4b3b-ab50-f5a046be5c3d"} 2.738041652e+09
px_cluster_memory_utilized_percent"{cluster="clusterpaul",node="devbox",node_id="f6c68c67-7c4f-4b3b-ab50-f5a046be5c3d"} 24
px_cluster_pendingio{cluster="clusterpaul",node="devbox",node_id="f6c68c67-7c4f-4b3b-ab50-f5a046be5c3d"} 0""")

    def setUp(self):
        self.http = HttpServerThread(self.data)
        self.instance = {'prometheus_endpoint': 'http://localhost:1337/metrics'}
        self.check_config = {'instances': [self.instance]}
        self.http.start()

    def tearDown(self):
        self.http.end_http()
        self.http.join()

    def test_check_all_metrics(self):
        """
        Testing Portworx check.
        """
        self.run_check(self.check_config)

        self.assertMetric("px.cluster_cpu_percent", count=1, value=0.76)

        self.coverage_report()