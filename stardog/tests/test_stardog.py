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
INSTANCE = {"username": "admin", "password": "admin", "tags": ["test1"]}


def setup_module(module):
    global HTTP
    HTTP = HttpServerThread()
    HTTP.start()
    INSTANCE["stardog_url"] = "http://localhost:{}".format(HTTP.port)


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
    check = StardogCheck("stardog", {}, [copy.deepcopy(INSTANCE)])
    check.check({})
    tags = copy.deepcopy(INSTANCE["tags"])
    tags.append("stardog_url:http://localhost:%d" % HTTP.port)
    # tags_with_db = copy.deepcopy(INSTANCE["tags"])

    for metric_key in DATA:
        metric_value = DATA[metric_key]
        if len(metric_value) > 1:
            for sub_value in metric_value:
                if sub_value in ("duration_units", "rate_units"):
                    continue
                new_key = "stardog.%s.%s" % (metric_key, sub_value)
                metric_val = float(metric_value[sub_value])
                aggregator.assert_metric(new_key, metric_type=0, count=1, value=metric_val, tags=tags)
        else:
            new_key = "stardog.%s" % metric_key
            metric_val = float(metric_value[next(iter(metric_value))])
            aggregator.assert_metric(new_key, metric_type=0, count=1, value=metric_val, tags=tags)
    aggregator.assert_all_metrics_covered


class HttpServerThread(threading.Thread):
    def __init__(self):
        super(HttpServerThread, self).__init__()
        self.done = False
        self.hostname = "localhost"

        class MockStardog(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path != "/admin/status":
                    self.send_response(404)
                    return
                if self.headers["Authorization"] != "Basic YWRtaW46YWRtaW4=":
                    self.send_response(401)
                    return
                self.send_response(200)
                self.send_header("Content-type", "application/json")
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
    "databases.foobar.equality.stalls.pendingCompaction": {"value": 0},
    "dbms.memory.blockcache.total.iteratorDeleted": {"value": 0},
    "user.threads.size": {"value": 5},
    "kga.foobar.reach.cardinality": {"value": 1},
    "databases.foobar.dictionary.value.compaction.read.throughput.bytesPerSec": {"value": 0.0},
    "databases.foobar.stats.compactions.pending": {"value": 0},
    "databases.foobar.dictionary.value.numFilesCompacting": {"value": 0},
    "dbms.memory.direct.buffer.used": {"value": 675524},
    "databases.foobar.dictionary.dict.memtable.memtableStalls": {"value": 0},
    "databases.foobar.equality.memtable.active.entries": {"value": 0},
    "dbms.memory.blockcache.data.iteratorCreated": {"value": 0},
    "databases.foobar.ternary.slowdowns.l0": {"value": 0},
    "databases.foobar.stats.stalls": {"value": 0},
    "databases.foobar.dictionary.value.memtable.immutable.entries": {"value": 0},
    "com.stardog.http.server-5820.currentRequests": {"count": 1},
    "dbms.memory.blockcache.total.filter.misses": {"value": 0},
    "databases.foobar.dictionary.value.liveDataSize": {"value": 0},
    "dbms.memory.mapped.used": {"value": 0},
    "dbms.memory.blockcache.data.hits": {"value": 0},
    "databases.foobar.equality.files.total": {"value": 0},
    "databases.system.numKeys": {"value": 0},
    "dbms.memory.blockcache.dictionary.hits": {"value": 0},
    "dbms.memory.system.virtual": {"value": 427180916736},
    "databases.foobar.stats.memtable.total.size.bytes": {"value": 6144},
    "databases.foobar.equality.compactions.written.bytes": {"value": 0},
    "admin.threads.queued": {"value": 0},
    "dbms.credentials.cache.size": {"value": 1},
    "databases.foobar.dictionary.dict.compaction.write.throughput.bytesPerSec": {"value": 0.0},
    "databases.foobar.dictionary.dict.memory.total": {"value": 2048},
    "dbms.memory.config.starrocks_size": {"value": 5712306504},
    "dbms.memory.blockcache.dictionary.iteratorDeleted": {"value": 0},
    "databases.foobar.stats.memtable.immutable.count": {"value": 0},
    "databases.foobar.dictionary.dict.compaction.read.throughput.bytesPerSec": {"value": 0.0},
    "databases.foobar.equality.liveDataSize": {"value": 0},
    "dbms.license.expiration": {"value": 3480},
    "databases.foobar.dictionary.value.flushes.running": {"value": 0},
    "databases.foobar.dictionary.value.slowdowns.l0": {"value": 0},
    "databases.foobar.dictionary.value.memtable.unpinned.size.bytes": {"value": 2048},
    "databases.foobar.backgroundErrors": {"value": 0},
    "databases.foobar.dictionary.value.memtable.memtableStalls": {"value": 0},
    "databases.foobar.dictionary.value.slowdowns": {"value": 0},
    "databases.foobar.ternary.compaction.time.sec": {"value": 0.0},
    "databases.foobar.equality.backgroundErrors": {"value": 0},
    "databases.foobar.dictionary.dict.slowdowns.l0.withCompaction": {"value": 0},
    "databases.foobar.ternary.memtable.immutable.entries": {"value": 0},
    "databases.foobar.equality.compaction.keysDropped": {"value": 0.0},
    "dbms.memory.system.rss.peak": {"value": 753139712},
    "databases.foobar.ternary.memtable.memtableSlowdowns": {"value": 0},
    "databases.foobar.dictionary.dict.memtable.active.entries": {"value": 10},
    "dbms.memory.config.dict_index_cache": {"value": 823237018},
    "databases.foobar.equality.memtable.total.size.bytes": {"value": 4096},
    "databases.foobar.stats.memtable.active.size.bytes": {"value": 6144},
    "databases.foobar.ternary.numLevels": {"value": 5},
    "databases.foobar.stats.files.total": {"value": 0},
    "databases.foobar.ternary.stalls.l0.withCompaction": {"value": 0},
    "databases.foobar.dictionary.value.stalls.l0.withCompaction": {"value": 0},
    "databases.foobar.dictionary.dict.flushes.pending": {"value": 0},
    "databases.foobar.dictionary.dict.writeAmplification": {"value": 0.0},
    "dbms.memory.blockcache.total.capacity": {"value": 1999307072},
    "databases.foobar.ternary.compaction.read.throughput.bytesPerSec": {"value": 0},
    "databases.foobar.dictionary.value.backgroundErrors": {"value": 0},
    "databases.foobar.deleted": {"count": 0},
    "databases.foobar.dictionary.value.stalls.pendingCompaction": {"value": 0},
    "databases.foobar.ternary.tableReaderMemory.bytes": {"value": 0},
    "databases.foobar.dictionary.value.numKeys": {"value": 10},
    "databases.foobar.equality.compaction.keysProcessed": {"value": 0.0},
    "databases.foobar.stats.stalls.l0": {"value": 0},
    "dbms.memory.blockcache.dictionary.written": {"value": 0},
    "databases.foobar.ternary.compaction.time.avg.sec": {"value": 0.0},
    "dbms.memory.blockcache.txn.ratio": {"value": 0.0},
    "dbms.memory.blockcache.txn.add.count": {"value": 0},
    "dbms.memory.blockcache.total.usage": {"value": 0},
    "dbms.memory.system.usageRatio": {"value": 0.5974303588531371},
    "dbms.memory.heap.query.blocks.max": {"value": 2448131358},
    "dbms.memory.blockcache.data.ratio": {"value": 0.0},
    "databases.foobar.dictionary.dict.memtable.immutable.entries": {"value": 0},
    "dbms.memory.native.max": {"value": 8589934592},
    "databases.foobar.equality.compactions.completed": {"value": 0},
    "databases.foobar.equality.writeAmplification": {"value": 0.0},
    "databases.foobar.dictionary.value.tableReaderMemory.bytes": {"value": 0},
    "dbms.memory.blockcache.txn.read": {"value": 0},
    "databases.system.backgroundErrors": {"value": 0},
    "databases.foobar.dictionary.dict.liveDataSize": {"value": 0},
    "databases.foobar.stats.slowdowns": {"value": 0},
    "databases.foobar.stats.compactions.written.bytes": {"value": 0},
    "databases.foobar.size": {"value": 6},
    "databases.foobar.stats.memtable.active.entries": {"value": 3},
    "databases.foobar.dictionary.dict.compaction.time.avg.sec": {"value": 0.0},
    "databases.foobar.dictionary.dict.numKeys": {"value": 10},
    "databases.foobar.stats.compaction.time.sec": {"value": 0.0},
    "databases.foobar.ternary.stalls.pendingCompaction": {"value": 0},
    "dbms.memory.blockcache.total.data.misses": {"value": 0},
    "databases.foobar.stats.memory.total": {"value": 6144},
    "databases.foobar.dictionary.value.stalls.l0": {"value": 0},
    "databases.foobar.dictionary.dict.flushes.running": {"value": 0},
    "dbms.memory.blockcache.total.data.hits": {"value": 0},
    "databases.foobar.queries.memory.acquired": {"count": 0},
    "databases.foobar.added": {"count": 6},
    "dbms.memory.system.regionCount": {"value": 1689},
    "databases.foobar.stats.compactions.running": {"value": 0},
    "databases.foobar.dictionary.value.memtable.memtableSlowdowns": {"value": 0},
    "databases.foobar.equality.flushes.running": {"value": 0},
    "dbms.memory.blockcache.data.misses": {"value": 0},
    "databases.foobar.dictionary.dict.compactions.running": {"value": 0},
    "databases.foobar.planCache.size": {"value": 1},
    "databases.foobar.equality.stalls.l0": {"value": 0},
    "databases.foobar.equality.memtable.immutable.size.bytes": {"value": 0},
    "dbms.credentials.cache.evictions": {"value": 0},
    "databases.foobar.equality.compaction.time.sec": {"value": 0.0},
    "databases.foobar.files.total": {"value": 1},
    "admin.threads.size": {"value": 8},
    "dbms.memory.blockcache.dictionary.usage": {"value": 0},
    "databases.foobar.stats.memtable.pinned.size.bytes": {"value": 0},
    "databases.foobar.dictionary.value.memtable.active.size.bytes": {"value": 2048},
    "databases.foobar.stats.compactions.read.bytes": {"value": 0},
    "databases.foobar.stats.memtable.unpinned.size.bytes": {"value": 6144},
    "system.uptime": {"value": 196226},
    "databases.foobar.stats.memtable.memtableSlowdowns": {"value": 0},
    "databases.foobar.dictionary.value.compaction.keysProcessed": {"value": 0.0},
    "databases.foobar.dictionary.value.compactions.running": {"value": 0},
    "databases.foobar.stats.memtable.immutable.size.bytes": {"value": 0},
    "databases.foobar.ternary.liveDataSize": {"value": 0},
    "databases.foobar.equality.memtable.immutable.entries": {"value": 0},
    "databases.foobar.ternary.compactions.completed": {"value": 0},
    "databases.foobar.dictionary.dict.slowdowns": {"value": 0},
    "dbms.memory.blockcache.txn.written": {"value": 0},
    "databases.foobar.numKeys": {"value": 0},
    "databases.foobar.ternary.flushes.pending": {"value": 0},
    "user.threads.queued": {"value": 0},
    "dbms.credentials.cache.loadSuccesses": {"value": 1},
    "dbms.memory.system.rss": {"value": 472694784},
    "databases.foobar.dictionary.dict.numLevels": {"value": 5},
    "dbms.memory.blockcache.txn.iteratorDeleted": {"value": 0},
    "dbms.credentials.cache.hits": {"value": 16},
    "databases.foobar.dictionary.value.flushes.pending": {"value": 0},
    "databases.foobar.stats.compaction.time.avg.sec": {"value": 0.0},
    "databases.foobar.equality.compactions.read.bytes": {"value": 0},
    "dbms.memory.blockcache.txn.iteratorCreated": {"value": 0},
    "databases.foobar.stats.backgroundErrors": {"value": 0},
    "databases.foobar.ternary.slowdowns.l0.withCompaction": {"value": 0},
    "databases.foobar.ternary.compactions.running": {"value": 0},
    "databases.foobar.ternary.memtable.active.size.bytes": {"value": 8091648},
    "databases.foobar.dictionary.dict.slowdowns.l0": {"value": 0},
    "databases.foobar.ternary.slowdowns.pendingCompaction": {"value": 0},
    "dbms.memory.blockcache.data.read": {"value": 0},
    "dbms.memory.system.pageSize": {"value": 16384},
    "databases.foobar.dictionary.value.memtable.immutable.count": {"value": 0},
    "databases.foobar.planCache.ratio": {"value": 0.0},
    "databases.foobar.txns.size": {
        "count": 1,
        "max": 6,
        "mean": 6.0,
        "min": 6,
        "p50": 6.0,
        "p75": 6.0,
        "p95": 6.0,
        "p98": 6.0,
        "p99": 6.0,
        "p999": 6.0,
        "stddev": 0.0,
    },
    "databases.foobar.equality.compactions.pending": {"value": 0},
    "databases.foobar.dictionary.value.compactions.read.bytes": {"value": 0},
    "databases.foobar.stats.tableReaderMemory.bytes": {"value": 0},
    "databases.foobar.dictionary.dict.compactions.read.bytes": {"value": 0},
    "databases.foobar.ternary.compaction.keysDropped": {"value": 0.0},
    "databases.foobar.equality.flushes.pending": {"value": 0},
    "databases.foobar.stats.flushes.running": {"value": 0},
    "dbms.memory.blockcache.total.iteratorCreated": {"value": 0},
    "dbms.memory.blockcache.dictionary.read": {"value": 0},
    "databases.foobar.equality.numKeys": {"value": 0},
    "dbms.memory.blockcache.dictionary.misses": {"value": 0},
    "databases.foobar.dictionary.dict.stalls.l0.withCompaction": {"value": 0},
    "dbms.memory.blockcache.txn.capacity": {"value": 285615296},
    "dbms.memory.blockcache.data.iteratorDeleted": {"value": 0},
    "databases.foobar.ternary.backgroundErrors": {"value": 0},
    "databases.foobar.ternary.numKeys": {"value": 48},
    "databases.foobar.equality.compaction.read.throughput.bytesPerSec": {"value": 0.0},
    "databases.foobar.stats.numLevels": {"value": 5},
    "databases.foobar.stats.compactions.completed": {"value": 0},
    "databases.foobar.dictionary.value.writeAmplification": {"value": 0.0},
    "dbms.memory.blockcache.total.data.ratio": {"value": 0.0},
    "databases.foobar.dictionary.dict.memtable.memtableSlowdowns": {"value": 0},
    "databases.foobar.dictionary.dict.compaction.keysProcessed": {"value": 0.0},
    "databases.foobar.dictionary.dict.backgroundErrors": {"value": 0},
    "admin.threads.active": {"value": 1},
    "databases.foobar.equality.slowdowns.pendingCompaction": {"value": 0},
    "dbms.memory.blockcache.total.index.misses": {"value": 0},
    "databases.foobar.equality.compaction.time.avg.sec": {"value": 0.0},
    "databases.foobar.ternary.numFilesCompacting": {"value": 0},
    "databases.foobar.dictionary.value.memtable.pinned.size.bytes": {"value": 0},
    "databases.foobar.openConnections": {"count": 0},
    "dbms.memory.heap.used": {"value": 267032216},
    "databases.foobar.ternary.compaction.write.throughput.bytesPerSec": {"value": 0},
    "databases.foobar.dictionary.value.compaction.time.avg.sec": {"value": 0.0},
    "databases.foobar.equality.compaction.write.throughput.bytesPerSec": {"value": 0.0},
    "databases.foobar.ternary.memtable.unpinned.size.bytes": {"value": 8091648},
    "databases.foobar.dictionary.dict.memtable.unpinned.size.bytes": {"value": 2048},
    "databases.foobar.dictionary.value.compaction.time.sec": {"value": 0.0},
    "databases.foobar.queries.latency": {
        "count": 2,
        "max": 0.025134959000000002,
        "mean": 0.02089200203963135,
        "min": 0.01740075,
        "p50": 0.01740075,
        "p75": 0.025134959000000002,
        "p95": 0.025134959000000002,
        "p98": 0.025134959000000002,
        "p99": 0.025134959000000002,
        "p999": 0.025134959000000002,
        "stddev": 0.003848796193870894,
        "m15_rate": 0.001912753264906753,
        "m1_rate": 0.003541815581316047,
        "m5_rate": 0.004252232020565875,
        "mean_rate": 0.011661396085341221,
        "duration_units": "seconds",
        "rate_units": "calls/second",
    },
    "databases.foobar.ternary.compactions.pending": {"value": 0},
    "databases.foobar.dictionary.dict.memtable.immutable.size.bytes": {"value": 0},
    "databases.foobar.equality.stalls": {"value": 0},
    "databases.foobar.stats.numKeys": {"value": 3},
    "dbms.memory.blockcache.data.pinnedUsage": {"value": 0},
    "dbms.memory.config.dict_value_cache": {"value": 823237018},
    "databases.foobar.txns.latency": {
        "count": 1,
        "max": 0.043208916,
        "mean": 0.043208916,
        "min": 0.043208916,
        "p50": 0.043208916,
        "p75": 0.043208916,
        "p95": 0.043208916,
        "p98": 0.043208916,
        "p99": 0.043208916,
        "p999": 0.043208916,
        "stddev": 0.0,
        "m15_rate": 9.484070116640398e-4,
        "m1_rate": 0.0015506900910289933,
        "m5_rate": 0.0020729741807790705,
        "mean_rate": 0.005830692934585878,
        "duration_units": "seconds",
        "rate_units": "calls/second",
    },
    "databases.foobar.dictionary.value.stalls": {"value": 0},
    "system.db.count": {"value": 1},
    "databases.foobar.stats.compaction.keysProcessed": {"value": 0.0},
    "dbms.memory.blockcache.txn.usage": {"value": 0},
    "databases.foobar.ternary.flushes.running": {"value": 0},
    "databases.foobar.equality.memtable.unpinned.size.bytes": {"value": 4096},
    "databases.foobar.dictionary.dict.files.total": {"value": 0},
    "databases.foobar.stats.compaction.read.throughput.bytesPerSec": {"value": 0.0},
    "databases.foobar.dictionary.dict.stalls.pendingCompaction": {"value": 0},
    "databases.foobar.equality.memory.total": {"value": 4096},
    "databases.foobar.dictionary.value.numLevels": {"value": 5},
    "databases.foobar.dictionary.dict.compaction.time.sec": {"value": 0.0},
    "databases.foobar.ternary.slowdowns": {"value": 0},
    "databases.foobar.equality.numFilesCompacting": {"value": 0},
    "dbms.memory.blockcache.dictionary.iteratorCreated": {"value": 0},
    "databases.foobar.dictionary.dict.stalls": {"value": 0},
    "databases.foobar.dictionary.value.memtable.immutable.size.bytes": {"value": 0},
    "system.cpu.usage": {"value": 0.001337039184532932},
    "databases.foobar.ternary.compactions.written.bytes": {"value": 0},
    "databases.foobar.dictionary.value.compactions.written.bytes": {"value": 0},
    "databases.foobar.stats.writeAmplification": {"value": 0.0},
    "databases.foobar.ternary.memtable.immutable.size.bytes": {"value": 0},
    "databases.foobar.ternary.memtable.pinned.size.bytes": {"value": 0},
    "dbms.memory.blockcache.data.usage": {"value": 0},
    "databases.foobar.ternary.memtable.memtableStalls": {"value": 0},
    "databases.foobar.stats.compaction.keysDropped": {"value": 0.0},
    "databases.foobar.equality.memtable.active.size.bytes": {"value": 4096},
    "databases.foobar.queries.running": {"count": 0},
    "databases.foobar.dictionary.dict.memtable.total.size.bytes": {"value": 2048},
    "dbms.memory.blockcache.data.add.count": {"value": 0},
    "databases.foobar.equality.numLevels": {"value": 5},
    "databases.foobar.dictionary.dict.slowdowns.pendingCompaction": {"value": 0},
    "databases.foobar.equality.slowdowns.l0.withCompaction": {"value": 0},
    "databases.foobar.equality.compactions.running": {"value": 0},
    "databases.foobar.dictionary.value.slowdowns.l0.withCompaction": {"value": 0},
    "databases.foobar.stats.stalls.pendingCompaction": {"value": 0},
    "dbms.memory.blockcache.total.pinnedUsage": {"value": 0},
    "databases.foobar.dictionary.dict.compaction.keysDropped": {"value": 0.0},
    "dbms.memory.blockcache.txn.add.failure.count": {"value": 0},
    "dbms.credentials.cache.loadFailures": {"value": 0},
    "databases.foobar.ternary.stalls.l0": {"value": 0},
    "databases.foobar.dictionary.dict.stalls.l0": {"value": 0},
    "user.threads.active": {"value": 0},
    "dbms.memory.blockcache.total.filter.ratio": {"value": 0.0},
    "dbms.memory.blockcache.dictionary.pinnedUsage": {"value": 0},
    "databases.foobar.ternary.compactions.read.bytes": {"value": 0},
    "databases.foobar.stats.compaction.write.throughput.bytesPerSec": {"value": 0.0},
    "databases.foobar.ternary.memtable.total.size.bytes": {"value": 8091648},
    "databases.foobar.equality.memtable.immutable.count": {"value": 0},
    "dbms.memory.blockcache.data.capacity": {"value": 1142461184},
    "dbms.memory.blockcache.txn.pinnedUsage": {"value": 0},
    "databases.foobar.stats.liveDataSize": {"value": 0},
    "databases.foobar.ternary.stalls": {"value": 0},
    "databases.foobar.stats.flushes.pending": {"value": 0},
    "databases.foobar.dictionary.dict.memtable.pinned.size.bytes": {"value": 0},
    "databases.foobar.ternary.files.total": {"value": 0},
    "databases.foobar.dictionary.value.memtable.total.size.bytes": {"value": 2048},
    "databases.foobar.dictionary.value.slowdowns.pendingCompaction": {"value": 0},
    "databases.foobar.txns.openTransactions": {"count": 0},
    "databases.foobar.dictionary.value.compaction.keysDropped": {"value": 0.0},
    "dbms.memory.blockcache.txn.hits": {"value": 0},
    "dbms.memory.blockcache.total.index.hits": {"value": 0},
    "databases.foobar.equality.tableReaderMemory.bytes": {"value": 0},
    "databases.foobar.dictionary.value.memory.total": {"value": 2048},
    "databases.foobar.dictionary.value.compactions.pending": {"value": 0},
    "databases.foobar.dictionary.dict.compactions.completed": {"value": 0},
    "dbms.memory.blockcache.total.filter.hits": {"value": 0},
    "databases.foobar.ternary.writeAmplification": {"value": 0.0},
    "databases.foobar.dictionary.value.compactions.completed": {"value": 0},
    "databases.foobar.equality.memtable.memtableStalls": {"value": 0},
    "databases.foobar.equality.slowdowns": {"value": 0},
    "dbms.credentials.cache.misses": {"value": 1},
    "databases.foobar.stats.memtable.memtableStalls": {"value": 0},
    "dbms.memory.blockcache.dictionary.add.failure.count": {"value": 0},
    "databases.foobar.dictionary.dict.tableReaderMemory.bytes": {"value": 0},
    "databases.foobar.dictionary.dict.memtable.immutable.count": {"value": 0},
    "databases.system.files.total": {"value": 1},
    "databases.system.planCache.size": {"value": 4},
    "databases.foobar.stats.memtable.immutable.entries": {"value": 0},
    "dbms.memory.blockcache.dictionary.add.count": {"value": 0},
    "databases.foobar.ternary.memtable.active.entries": {"value": 48},
    "databases.foobar.dictionary.dict.memtable.active.size.bytes": {"value": 2048},
    "dbms.memory.heap.max": {"value": 4116185088},
    "databases.system.planCache.ratio": {"value": 0.6},
    "dbms.memory.blockcache.data.add.failure.count": {"value": 0},
    "databases.foobar.dictionary.dict.compactions.pending": {"value": 0},
    "dbms.license.quantity": {"value": 3},
    "databases.foobar.ternary.compaction.keysProcessed": {"value": 0.0},
    "databases.foobar.queries.memory.spilled": {"count": 0},
    "databases.foobar.ternary.memtable.immutable.count": {"value": 0},
    "kga.foobar.reach.rate": {"value": 2.777777777777778e-4},
    "kga.foobar.reach.histogram": {
        "count": 1,
        "max": 1,
        "mean": 1.0,
        "min": 1,
        "p50": 1.0,
        "p75": 1.0,
        "p95": 1.0,
        "p98": 1.0,
        "p99": 1.0,
        "p999": 1.0,
        "stddev": 0.0,
    },
    "databases.foobar.equality.stalls.l0.withCompaction": {"value": 0},
    "dbms.memory.native.query.blocks.used": {"value": 0},
    "dbms.memory.blockcache.txn.misses": {"value": 0},
    "dbms.memory.native.query.blocks.max": {"value": 2448131358},
    "databases.foobar.dictionary.dict.compactions.written.bytes": {"value": 0},
    "com.stardog.http.server-5820.avgRequestTime": {
        "count": 16,
        "max": 272,
        "mean": 41.99301006953569,
        "min": 0,
        "p50": 36.0,
        "p75": 37.0,
        "p95": 157.0,
        "p98": 272.0,
        "p99": 272.0,
        "p999": 272.0,
        "stddev": 48.5538395950457,
    },
    "dbms.memory.blockcache.data.written": {"value": 0},
    "databases.foobar.stats.numFilesCompacting": {"value": 0},
    "databases.foobar.equality.memtable.pinned.size.bytes": {"value": 0},
    "databases.foobar.dictionary.value.memtable.active.entries": {"value": 10},
    "databases.foobar.dictionary.dict.numFilesCompacting": {"value": 0},
    "databases.foobar.stats.stalls.l0.withCompaction": {"value": 0},
    "databases.foobar.equality.memtable.memtableSlowdowns": {"value": 0},
    "databases.foobar.dictionary.value.files.total": {"value": 0},
    "dbms.memory.blockcache.dictionary.ratio": {"value": 0.0},
    "databases.foobar.stats.slowdowns.l0": {"value": 0},
    "dbms.memory.heap.query.blocks.used": {"value": 0},
    "dbms.memory.config.query_mem_blocks": {"value": 2448131358},
    "databases.foobar.dictionary.value.compaction.write.throughput.bytesPerSec": {"value": 0.0},
    "dbms.memory.blockcache.dictionary.capacity": {"value": 571230592},
    "databases.foobar.stats.slowdowns.l0.withCompaction": {"value": 0},
    "databases.foobar.stats.slowdowns.pendingCompaction": {"value": 0},
    "databases.foobar.ternary.memory.total": {"value": 8091648},
    "databases.foobar.equality.slowdowns.l0": {"value": 0},
    "dbms.backup.keep.last.number.backups": {"value": "4"},
    "dbms.memory.blockcache.total.index.ratio": {"value": 0.0},
}
