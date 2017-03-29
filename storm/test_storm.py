# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib
from nose.plugins.attrib import attr

# 3p
import responses

# project
from checks import AgentCheck
from tests.checks.common import AgentCheckTest


instance = {
    'server': 'localhost:9005',
    'environment': 'test'
}

TEST_STORM_CLUSTER_SUMMARY = {
    "executorsTotal": 33,
    "stormVersion": "1.0.3",
    "slotsTotal": 10,
    "slotsFree": 4,
    "user": None,
    "topologies": 1,
    "supervisors": 1,
    "central-log-url": None,
    "bugtracker-url": None,
    "tasksTotal": 33,
    "slotsUsed": 6
}

TEST_STORM_NIMBUSES_SUMMARY = {
    "nimbuses": [
        {
            "nimbusUptimeSeconds": "Not applicable",
            "nimbusUpTime": "Not applicable",
            "version": "Not applicable",
            "status": "Offline",
            "nimbusLogLink": "http://nimbus01.example.com:9006/daemonlog?file=nimbus.log",
            "port": "6627",
            "host": "nimbus01.example.com"
        },
        {
            "nimbusUpTimeSeconds": 25842,
            "nimbusUpTime": "7h 10m 42s",
            "version": "1.0.3",
            "status": "Leader",
            "nimbusLogLink": "http://1.2.3.4:9006/daemonlog?file=nimbus.log",
            "port": 6627,
            "host": "1.2.3.4"
        }
    ]
}

TEST_STORM_SUPERVISOR_SUMMARY = {
    "logviewerPort": 9006,
    "schedulerDisplayResource": False,
    "supervisors": [
        {
            "uptimeSeconds": 31559,
            "slotsTotal": 10,
            "version": "1.0.3",
            "slotsUsed": 6,
            "totalMem": 3072,
            "host": "1.2.3.4",
            "id": "11111111-1111-1111-1111-111111111111",
            "uptime": "8h 45m 59s",
            "totalCpu": 900,
            "usedCpu": 0,
            "logLink": "http://1.2.3.4:9006/daemonlog?file=supervisor.log",
            "usedMem": 4992
        }
    ]
}

TEST_STORM_TOPOLOGY_SUMMARY = {
    "schedulerDisplayResource": False,
    "topologies": [
        {
            "requestedTotalMem": 0,
            "assignedMemOffHeap": 0,
            "assignedCpu": 0,
            "uptimeSeconds": 1525505,
            "schedulerInfo": None,
            "uptime": "17d 15h 45m 5s",
            "id": "my_topology-1-1489183263",
            "assignedMemOnHeap": 4992,
            "encodedId": "my_topology-1-1489183263",
            "requestedMemOnHeap": 0,
            "owner": "storm",
            "assignedTotalMem": 4992,
            "name": "my_topology",
            "workersTotal": 6,
            "status": "ACTIVE",
            "requestedMemOffHeap": 0,
            "tasksTotal": 33,
            "requestedCpu": 0,
            "replicationCount": 1,
            "executorsTotal": 33
        }
    ]
}

TEST_STORM_TOPOLOGY_RESP = {
    "assignedMemOffHeap": 0,
    "topologyStats": [
        {
            "failed": None,
            "acked": 0,
            "completeLatency": "0",
            "transferred": 0,
            "emitted": 0,
            "window": "600",
            "windowPretty": "10m 0s"
        },
        {
            "failed": None,
            "acked": 104673,
            "completeLatency": "285.950",
            "transferred": 307606,
            "emitted": 307606,
            "window": "10800",
            "windowPretty": "3h 0m 0s"
        },
        {
            "failed": None,
            "acked": 104673,
            "completeLatency": "285.950",
            "transferred": 307606,
            "emitted": 307606,
            "window": "86400",
            "windowPretty": "1d 0h 0m 0s"
        },
        {
            "failed": None,
            "acked": 104673,
            "completeLatency": "285.950",
            "transferred": 307606,
            "emitted": 307606,
            "window": ":all-time",
            "windowPretty": "All time"
        }
    ],
    "assignedCpu": 0,
    "uptimeSeconds": 1525788,
    "executorsTotal": 33,
    "bolts": [
        {
            "errorWorkerLogLink": "",
            "capacity": "0.000",
            "processLatency": "201.474",
            "executors": 3,
            "boltId": "Bolt1",
            "failed": 0,
            "errorHost": "",
            "tasks": 3,
            "errorTime": None,
            "emitted": 101309,
            "executeLatency": "0.001",
            "transferred": 101309,
            "errorPort": "",
            "errorLapsedSecs": None,
            "acked": 212282,
            "encodedBoltId": "Bolt1",
            "lastError": "",
            "executed": 106311
        },
        {
            "errorWorkerLogLink": "",
            "capacity": "0.000",
            "processLatency": "0.010",
            "executors": 2,
            "boltId": "Bolt2",
            "failed": 0,
            "errorHost": "",
            "tasks": 2,
            "errorTime": None,
            "emitted": 0,
            "executeLatency": "0.015",
            "transferred": 0,
            "errorPort": "",
            "errorLapsedSecs": None,
            "acked": 3153,
            "encodedBoltId": "Bolt2",
            "lastError": "",
            "executed": 3153
        },
        {
            "errorWorkerLogLink": "",
            "capacity": "0.000",
            "processLatency": "0.003",
            "executors": 3,
            "boltId": "Bolt3",
            "failed": 0,
            "errorHost": "",
            "tasks": 3,
            "errorTime": None,
            "emitted": 0,
            "executeLatency": "0.009",
            "transferred": 0,
            "errorPort": "",
            "errorLapsedSecs": None,
            "acked": 4704,
            "encodedBoltId": "Bolt3",
            "lastError": "",
            "executed": 4704
        },
        {
            "errorWorkerLogLink": "",
            "capacity": "0.000",
            "processLatency": "291.756",
            "executors": 4,
            "boltId": "Bolt4",
            "failed": 0,
            "errorHost": "",
            "tasks": 4,
            "errorTime": None,
            "emitted": 101607,
            "executeLatency": "0.001",
            "transferred": 101607,
            "errorPort": "",
            "errorLapsedSecs": None,
            "acked": 218808,
            "encodedBoltId": "Bolt4",
            "lastError": "",
            "executed": 110946
        },
        {
            "errorWorkerLogLink": "",
            "capacity": "0.000",
            "processLatency": "1014.634",
            "executors": 2,
            "boltId": "Bolt5",
            "failed": 0,
            "errorHost": "",
            "tasks": 2,
            "errorTime": None,
            "emitted": 17,
            "executeLatency": "0.001",
            "transferred": 17,
            "errorPort": "",
            "errorLapsedSecs": None,
            "acked": 208890,
            "encodedBoltId": "Bolt5",
            "lastError": "",
            "executed": 104445
        },
        {
            "errorWorkerLogLink": "",
            "capacity": "0.000",
            "processLatency": "0.005",
            "executors": 3,
            "boltId": "Bolt6",
            "failed": 0,
            "errorHost": "",
            "tasks": 3,
            "errorTime": None,
            "emitted": 0,
            "executeLatency": "0.010",
            "transferred": 0,
            "errorPort": "",
            "errorLapsedSecs": None,
            "acked": 4705,
            "encodedBoltId": "Bolt6",
            "lastError": "",
            "executed": 4705
        }
    ],
    "schedulerDisplayResource": False,
    "replicationCount": 1,
    "requestedCpu": 0,
    "tasksTotal": 33,
    "visualizationTable": [],
    "debug": False,
    "requestedMemOffHeap": 0,
    "spouts": [
        {
            "errorWorkerLogLink": "http://1.2.3.4:9006/log?file=my_topology-1-1489183263%2F6707%2Fworker.log",
            "lastError": "com.rabbitmq.client.ShutdownSignalException: clean connection shutdown; protocol method: #method<connection.close>(reply-code=200, reply-text=OK, class-id=0, method-id=0)\n\tat com.rabbitmq.client.impl.",
            "acked": 104673,
            "errorLapsedSecs": 38737,
            "errorPort": 6707,
            "transferred": 104673,
            "encodedSpoutId": "source",
            "emitted": 104673,
            "spoutId": "source",
            "errorTime": 1490670314,
            "tasks": 8,
            "errorHost": "1.2.3.4",
            "failed": 0,
            "completeLatency": "285.950",
            "executors": 8
        }
    ],
    "status": "ACTIVE",
    "user": None,
    "msgTimeout": 300,
    "windowHint": "All time",
    "encodedId": "my_topology-1-1489183263",
    "requestedMemOnHeap": 0,
    "owner": "storm",
    "window": ":all-time",
    "assignedTotalMem": 4992,
    "samplingPct": 10,
    "assignedMemOnHeap": 4992,
    "id": "my_topology-1-1489183263",
    "configuration": {
        "drpc.request.timeout.secs": 600,
        "storm.auth.simple-acl.users.commands": [],
        "nimbus.thrift.max_buffer_size": 1048576,
        "logviewer.appender.name": "A1",
        "storm.messaging.netty.transfer.batch.size": 262144,
        "storm.exhibitor.poll.uripath": "/exhibitor/v1/cluster/list",
        "topology.name": "my_topology",
        "storm.id": "my_topology-1-1489183263",
        "topology.kryo.decorators": [],
        "ui.port": 9005,
        "java.library.path": "/usr/local/lib:/opt/local/lib:/usr/lib",
        "drpc.invocations.threads": 64,
        "storm.auth.simple-acl.users": [],
        "topology.trident.batch.emit.interval.millis": 500,
        "storm.nimbus.retry.intervalceiling.millis": 60000,
        "topology.disruptor.wait.timeout.millis": 1000,
        "topology.min.replication.count": 1,
        "ui.header.buffer.bytes": 4096,
        "ui.filter": None,
        "backpressure.disruptor.high.watermark": 0.9,
        "ui.http.x-frame-options": "DENY",
        "topology.worker.max.heap.size.mb": 1024,
        "supervisor.childopts": "-Xmx256m",
        "client.blobstore.class": "org.apache.storm.blobstore.NimbusBlobStore",
        "storm.blobstore.acl.validation.enabled": False,
        "storm.zookeeper.auth.password": None,
        "supervisor.worker.timeout.secs": 30,
        "transactional.zookeeper.servers": None,
        "ui.users": None,
        "pacemaker.childopts": "-Xmx1024m",
        "logviewer.max.sum.worker.logs.size.mb": 4096,
        "worker.heap.memory.mb": 768,
        "storm.blobstore.replication.factor": 3,
        "nimbus.cleanup.inbox.freq.secs": 600,
        "nimbus.queue.size": 100000,
        "nimbus.seeds": [
            "nimbus01.example.com"
        ],
        "nimbus.topology.validator": "org.apache.storm.nimbus.DefaultTopologyValidator",
        "worker.gc.childopts": "",
        "topology.kryo.register": None,
        "topology.kryo.factory": "org.apache.storm.serialization.DefaultKryoFactory",
        "topology.component.resources.onheap.memory.mb": 256,
        "storm.messaging.netty.authentication": False,
        "topology.disable.loadaware.messaging": False,
        "storm.messaging.transport": "org.apache.storm.messaging.netty.Context",
        "topology.error.throttle.interval.secs": 10,
        "drpc.http.port": 3774,
        "topology.component.resources.offheap.memory.mb": 0,
        "storm.messaging.netty.max_wait_ms": 1000,
        "pacemaker.port": 6699,
        "task.heartbeat.frequency.secs": 3,
        "storm.exhibitor.port": 8080,
        "topology.metrics.consumer.register": [
            {
                "parallelism.hint": 2,
                "class": "com.accelerate_experience.storm.metrics.statsd.StatsdMetricConsumer",
                "argument": {
                    "metrics.statsd.prefix": "storm.metrics.",
                    "metrics.statsd.port": 8125,
                    "metrics.statsd.host": "127.0.0.1"
                }
            }
        ],
        "task.refresh.poll.secs": 10,
        "supervisor.blobstore.download.max_retries": 3,
        "storm.workers.artifacts.dir": "workers-artifacts",
        "drpc.https.port": -1,
        "topology.tick.tuple.freq.secs": 4,
        "topology.submitter.user": "storm",
        "storm.zookeeper.root": "/storm",
        "ui.http.creds.plugin": "org.apache.storm.security.auth.DefaultHttpCredentialsPlugin",
        "storm.log4j2.conf.dir": "log4j2",
        "worker.heartbeat.frequency.secs": 1,
        "storm.cluster.state.store": "org.apache.storm.cluster_state.zookeeper_state_factory",
        "storm.messaging.netty.buffer_size": 5242880,
        "storm.local.mode.zmq": False,
        "nimbus.task.launch.secs": 120,
        "topology.users": [],
        "backpressure.disruptor.low.watermark": 0.4,
        "topology.executor.receive.buffer.size": 1024,
        "worker.profiler.childopts": "-XX:+UnlockCommercialFeatures -XX:+FlightRecorder",
        "nimbus.file.copy.expiration.secs": 600,
        "drpc.authorizer.acl.strict": False,
        "topology.worker.shared.thread.pool.size": 4,
        "storm.health.check.dir": "/var/lib/storm/healthchecks",
        "topology.transfer.buffer.size": 1024,
        "supervisor.slots.ports": [
            6700
        ],
        "topology.state.checkpoint.interval.ms": 1000,
        "topology.worker.receiver.thread.count": 1,
        "drpc.https.keystore.type": "JKS",
        "task.credentials.poll.secs": 30,
        "pacemaker.thread.timeout": 10,
        "drpc.max_buffer_size": 1048576,
        "transactional.zookeeper.port": None,
        "dev.zookeeper.path": "/tmp/dev-storm-zookeeper",
        "nimbus.inbox.jar.expiration.secs": 3600,
        "storm.nimbus.retry.interval.millis": 2000,
        "topology.submitter.principal": "",
        "ui.host": "0.0.0.0",
        "topology.spout.wait.strategy": "org.apache.storm.spout.SleepSpoutWaitStrategy",
        "topology.worker.logwriter.childopts": "-Xmx64m",
        "storm.daemon.metrics.reporter.plugins": [
            "org.apache.storm.daemon.metrics.reporters.JmxPreparableReporter"
        ],
        "pacemaker.auth.method": "NONE",
        "resource.aware.scheduler.priority.strategy": "org.apache.storm.scheduler.resource.strategies.priority.DefaultSchedulingPriorityStrategy",
        "topology.executor.send.buffer.size": 1024,
        "topology.scheduler.strategy": "org.apache.storm.scheduler.resource.strategies.scheduling.DefaultResourceAwareStrategy",
        "logviewer.port": 9006,
        "nimbus.code.sync.freq.secs": 120,
        "drpc.https.keystore.password": "",
        "topology.shellbolt.max.pending": 100,
        "storm.blobstore.inputstream.buffer.size.bytes": 65536,
        "supervisor.blobstore.class": "org.apache.storm.blobstore.NimbusBlobStore",
        "topology.backpressure.enable": False,
        "drpc.queue.size": 128,
        "task.backpressure.poll.secs": 30,
        "supervisor.blobstore.download.thread.count": 5,
        "drpc.worker.threads": 64,
        "supervisor.cpu.capacity": 300,
        "topology.enable.message.timeouts": True,
        "supervisor.heartbeat.frequency.secs": 5,
        "storm.zookeeper.port": 2181,
        "worker.log.level.reset.poll.secs": 30,
        "storm.messaging.netty.min_wait_ms": 100,
        "topology.stats.sample.rate": 1,
        "supervisor.enable": True,
        "zmq.linger.millis": 5000,
        "topology.max.replication.wait.time.sec": 60,
        "scheduler.display.resource": False,
        "topology.sleep.spout.wait.strategy.time.ms": 1,
        "logviewer.cleanup.interval.secsInterval": 86400,
        "transactional.zookeeper.root": "/transactional",
        "storm.group.mapping.service": "org.apache.storm.security.auth.ShellBasedGroupsMapping",
        "zmq.threads": 1,
        "topology.priority": 29,
        "topology.builtin.metrics.bucket.size.secs": 60,
        "nimbus.childopts": "-Xmx2048m",
        "ui.filter.params": None,
        "storm.cluster.mode": "distributed",
        "storm.messaging.netty.client_worker_threads": 1,
        "logviewer.max.per.worker.logs.size.mb": 2048,
        "supervisor.run.worker.as.user": False,
        "topology.max.task.parallelism": None,
        "drpc.invocations.port": 3773,
        "supervisor.localizer.cache.target.size.mb": 10240,
        "topology.multilang.serializer": "org.apache.storm.multilang.JsonSerializer",
        "storm.messaging.netty.server_worker_threads": 1,
        "nimbus.blobstore.class": "org.apache.storm.blobstore.LocalFsBlobStore",
        "resource.aware.scheduler.eviction.strategy": "org.apache.storm.scheduler.resource.strategies.eviction.DefaultEvictionStrategy",
        "topology.max.error.report.per.interval": 5,
        "storm.thrift.transport": "org.apache.storm.security.auth.SimpleTransportPlugin",
        "zmq.hwm": 0,
        "storm.group.mapping.service.params": None,
        "worker.profiler.enabled": False,
        "storm.principal.tolocal": "org.apache.storm.security.auth.DefaultPrincipalToLocal",
        "supervisor.worker.shutdown.sleep.secs": 1,
        "pacemaker.host": "localhost",
        "storm.zookeeper.retry.times": 5,
        "ui.actions.enabled": True,
        "topology.acker.executors": None,
        "topology.fall.back.on.java.serialization": True,
        "topology.eventlogger.executors": 0,
        "supervisor.localizer.cleanup.interval.ms": 600000,
        "storm.zookeeper.servers": [
            "zookeeper01.example.com"
        ],
        "nimbus.thrift.threads": 64,
        "logviewer.cleanup.age.mins": 10080,
        "topology.worker.childopts": None,
        "topology.classpath": None,
        "supervisor.monitor.frequency.secs": 3,
        "nimbus.credential.renewers.freq.secs": 600,
        "topology.skip.missing.kryo.registrations": False,
        "drpc.authorizer.acl.filename": "drpc-auth-acl.yaml",
        "pacemaker.kerberos.users": [],
        "storm.group.mapping.service.cache.duration.secs": 120,
        "topology.testing.always.try.serialize": False,
        "nimbus.monitor.freq.secs": 10,
        "worker.childops": "-Xmx2048m -XX:+PrintGCDetails -Xloggc:artifacts/gc.log -XX:+PrintGCDateStamps -XX:+PrintGCTimeStamps -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=10 -XX:GCLogFileSize=1M -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=artifacts/heapdump",
        "storm.health.check.timeout.ms": 10000,
        "supervisor.supervisors": [],
        "topology.tasks": None,
        "topology.bolts.outgoing.overflow.buffer.enable": False,
        "storm.messaging.netty.socket.backlog": 500,
        "topology.workers": 6,
        "pacemaker.base.threads": 10,
        "storm.local.dir": "/var/lib/storm/data",
        "worker.childopts": "-Xmx%HEAP-MEM%m -XX:+PrintGCDetails -Xloggc:artifacts/gc.log -XX:+PrintGCDateStamps -XX:+PrintGCTimeStamps -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=10 -XX:GCLogFileSize=1M -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=artifacts/heapdump",
        "storm.auth.simple-white-list.users": [],
        "topology.disruptor.batch.timeout.millis": 1,
        "topology.message.timeout.secs": 300,
        "topology.state.synchronization.timeout.secs": 60,
        "topology.tuple.serializer": "org.apache.storm.serialization.types.ListDelegateSerializer",
        "supervisor.supervisors.commands": [],
        "nimbus.blobstore.expiration.secs": 600,
        "logviewer.childopts": "-Xmx128m",
        "topology.environment": {
            "mytopology.foo": "bar"
        },
        "topology.debug": False,
        "topology.disruptor.batch.size": 100,
        "storm.messaging.netty.max_retries": 300,
        "ui.childopts": "-Xmx768m",
        "storm.network.topography.plugin": "org.apache.storm.networktopography.DefaultRackDNSToSwitchMapping",
        "storm.zookeeper.session.timeout": 20000,
        "drpc.childopts": "-Xmx768m",
        "drpc.http.creds.plugin": "org.apache.storm.security.auth.DefaultHttpCredentialsPlugin",
        "storm.zookeeper.connection.timeout": 15000,
        "storm.zookeeper.auth.user": None,
        "storm.meta.serialization.delegate": "org.apache.storm.serialization.GzipThriftSerializationDelegate",
        "topology.max.spout.pending": 500,
        "storm.codedistributor.class": "org.apache.storm.codedistributor.LocalFileSystemCodeDistributor",
        "nimbus.supervisor.timeout.secs": 60,
        "nimbus.task.timeout.secs": 30,
        "storm.zookeeper.superACL": None,
        "drpc.port": 3772,
        "pacemaker.max.threads": 50,
        "storm.zookeeper.retry.intervalceiling.millis": 30000,
        "nimbus.thrift.port": 6627,
        "storm.auth.simple-acl.admins": [],
        "topology.component.cpu.pcore.percent": 10,
        "supervisor.memory.capacity.mb": 3072,
        "storm.nimbus.retry.times": 5,
        "supervisor.worker.start.timeout.secs": 120,
        "storm.zookeeper.retry.interval": 1000,
        "logs.users": None,
        "worker.profiler.command": "flight.bash"
    },
    "uptime": "17d 15h 49m 48s",
    "schedulerInfo": None,
    "name": "my_topology",
    "workersTotal": 6
}


@attr(requires='storm')
class TestStorm(AgentCheckTest):
    """Basic Test for storm integration."""
    CHECK_NAME = 'storm'
    STORM_CHECK_CONFIG = {'instances': [{'server': 'localhost:9005', 'environment': 'test'}]}

    def assign_self_info_from_check(self):
        print self.check.service_checks
        print self.check.aggregator.metrics
        self.service_checks = self.check.service_checks
        self.metrics = self.check.aggregator.metrics
        self.events = self.check.events
        self.service_metadata = self.check.svc_metadata
        self.warnings = self.check.warnings

    def test_try_float(self):
        self.load_check(self.STORM_CHECK_CONFIG, {})
        self.assertEquals(0.1, self.check.try_float("0.1"))
        self.assertEquals(0.0, self.check.try_float("garbage"))

    def test_try_long(self):
        self.load_check(self.STORM_CHECK_CONFIG, {})
        self.assertEquals(1, self.check.try_long("1"))
        self.assertEquals(0.0, self.check.try_float("garbage"))

    @responses.activate
    def test_get_storm_cluster_summary(self):
        responses.add(
            responses.GET,
            'http://localhost:9005/api/v1/cluster/summary',
            json=TEST_STORM_CLUSTER_SUMMARY,
            status=200
        )

        self.load_check(self.STORM_CHECK_CONFIG, {})
        result = self.check.get_storm_cluster_summary()
        self.assertEquals(TEST_STORM_CLUSTER_SUMMARY, result)

    @responses.activate
    def test_get_storm_nimbus_summary(self):
        responses.add(
            responses.GET,
            'http://localhost:9005/api/v1/nimbus/summary',
            json=TEST_STORM_NIMBUSES_SUMMARY,
            status=200
        )

        self.load_check(self.STORM_CHECK_CONFIG, {})
        result = self.check.get_storm_nimbus_summary()
        self.assertEquals(TEST_STORM_NIMBUSES_SUMMARY, result)

    @responses.activate
    def test_get_storm_supervisor_summary(self):
        responses.add(
            responses.GET,
            'http://localhost:9005/api/v1/supervisor/summary',
            json=TEST_STORM_SUPERVISOR_SUMMARY,
            status=200
        )

        self.load_check(self.STORM_CHECK_CONFIG, {})
        result = self.check.get_storm_supervisor_summary()
        self.assertEquals(TEST_STORM_SUPERVISOR_SUMMARY, result)

    @responses.activate
    def test_get_storm_topology_summary(self):
        responses.add(
            responses.GET,
            'http://localhost:9005/api/v1/topology/summary',
            json=TEST_STORM_TOPOLOGY_SUMMARY,
            status=200
        )

        self.load_check(self.STORM_CHECK_CONFIG, {})
        result = self.check.get_storm_topology_summary()
        self.assertEquals(TEST_STORM_TOPOLOGY_SUMMARY, result)

    @responses.activate
    def test_get_storm_topology_info(self):
        responses.add(
            responses.GET,
            'http://localhost:9005/api/v1/topology/my_topology-1-1489183263',
            json=TEST_STORM_TOPOLOGY_RESP,
            status=200
        )

        self.load_check(self.STORM_CHECK_CONFIG, {})
        result = self.check.get_topology_info('my_topology-1-1489183263')
        self.assertEquals(TEST_STORM_TOPOLOGY_RESP, result)

    def test_process_cluster_stats(self):
        self.load_check(self.STORM_CHECK_CONFIG, {})
        results = self.check.process_cluster_stats('test', TEST_STORM_CLUSTER_SUMMARY)
        self.assertEquals(7, len(results))

        # Check Cluster Stats
        self.assertEquals(33, results['storm.cluster.executorsTotal'][0])
        self.assertEquals(10, results['storm.cluster.slotsTotal'][0])
        self.assertEquals(4, results['storm.cluster.slotsFree'][0])
        self.assertEquals(1, results['storm.cluster.topologies'][0])
        self.assertEquals(1, results['storm.cluster.supervisors'][0])
        self.assertEquals(33, results['storm.cluster.tasksTotal'][0])
        self.assertEquals(6, results['storm.cluster.slotsUsed'][0])

    def test_process_nimbus_stats(self):
        self.load_check(self.STORM_CHECK_CONFIG, {})
        results = self.check.process_nimbus_stats('test', TEST_STORM_NIMBUSES_SUMMARY)
        self.assertEquals(2, len(results))  # 1 for leader, 1 for general stats

        # Check Leader Stats
        self.assertEquals(25842, results[0]['storm.nimbus.upTimeSeconds'][0])

        # Check General Stats
        self.assertEquals(1, results[1]['storm.nimbus.numLeaders'][0])
        self.assertEquals(0, results[1]['storm.nimbus.numFollowers'][0])
        self.assertEquals(1, results[1]['storm.nimbus.numOffline'][0])
        self.assertEquals(0, results[1]['storm.nimbus.numDead'][0])

    def test_process_supervisor_stats(self):
        self.load_check(self.STORM_CHECK_CONFIG, {})
        results = self.check.process_supervisor_stats(TEST_STORM_SUPERVISOR_SUMMARY)
        self.assertEquals(1, len(results))
        self.assertEquals(7, len(results[0]))

        # Check Supervisor Stats
        self.assertEquals(31559, results[0]['storm.supervisor.uptimeSeconds'][0])
        self.assertEquals(10, results[0]['storm.supervisor.slotsTotal'][0])
        self.assertEquals(6, results[0]['storm.supervisor.slotsUsed'][0])
        self.assertEquals(3072, results[0]['storm.supervisor.totalMem'][0])
        self.assertEquals(4992, results[0]['storm.supervisor.usedMem'][0])
        self.assertEquals(900, results[0]['storm.supervisor.totalCpu'][0])
        self.assertEquals(0, results[0]['storm.supervisor.usedCpu'][0])

    def test_process_topology_stats(self):
        self.load_check(self.STORM_CHECK_CONFIG, {})
        results = self.check.process_topology_stats(TEST_STORM_TOPOLOGY_RESP)
        topology_stats = results['topologyStats']
        bolt_stats = results['bolts']
        spout_stats = results['spouts']
        self.assertEquals(1, len(spout_stats))
        self.assertEquals(6, len(bolt_stats))
        self.assertEquals(12, len(topology_stats))

        # Check Topology Stats
        self.assertEquals(307606, topology_stats['storm.topologyStats.alltime.emitted'][0])
        self.assertEquals(307606, topology_stats['storm.topologyStats.alltime.transferred'][0])
        self.assertEquals(104673, topology_stats['storm.topologyStats.alltime.acked'][0])
        self.assertEquals(0, topology_stats['storm.topologyStats.alltime.failed'][0])
        self.assertEquals(285.950, topology_stats['storm.topologyStats.alltime.completeLatency'][0])
        self.assertEquals(1525788, topology_stats['storm.topologyStats.uptimeSeconds'][0])
        self.assertEquals(33, topology_stats['storm.topologyStats.executorsTotal'][0])
        self.assertEquals(6, topology_stats['storm.topologyStats.numBolts'][0])
        self.assertEquals(1, topology_stats['storm.topologyStats.replicationCount'][0])
        self.assertEquals(33, topology_stats['storm.topologyStats.tasksTotal'][0])
        self.assertEquals(1, topology_stats['storm.topologyStats.numSpouts'][0])
        self.assertEquals(6, topology_stats['storm.topologyStats.workersTotal'][0])

        # Check Bolt Stats
        bs = bolt_stats[0]
        self.assertEquals(3, bs['storm.bolt.tasks'][0])
        self.assertTrue('#bolt:Bolt1' in bs['storm.bolt.tasks'][1])
        self.assertEquals(0.001, bs['storm.bolt.executeLatency'][0])
        self.assertEquals(201.474, bs['storm.bolt.processLatency'][0])
        self.assertEquals(0.000, bs['storm.bolt.capacity'][0])
        self.assertEquals(0, bs['storm.bolt.failed'][0])
        self.assertEquals(101309, bs['storm.bolt.emitted'][0])
        self.assertEquals(212282, bs['storm.bolt.acked'][0])
        self.assertEquals(101309, bs['storm.bolt.transferred'][0])
        self.assertEquals(106311, bs['storm.bolt.executed'][0])
        self.assertEquals(3, bs['storm.bolt.executors'][0])
        self.assertEquals(1E10, bs['storm.bolt.errorLapsedSecs'][0])

        # Check Spout Stats
        ss = spout_stats[0]
        self.assertEquals(8, ss['storm.spout.tasks'][0])
        self.assertTrue('#spout:source' in ss['storm.spout.tasks'][1])
        self.assertEquals(285.950, ss['storm.spout.completeLatency'][0])
        self.assertEquals(0, ss['storm.spout.failed'][0])
        self.assertEquals(104673, ss['storm.spout.acked'][0])
        self.assertEquals(104673, ss['storm.spout.transferred'][0])
        self.assertEquals(104673, ss['storm.spout.emitted'][0])
        self.assertEquals(8, ss['storm.spout.executors'][0])
        self.assertEquals(38737, ss['storm.spout.errorLapsedSecs'][0])

    @responses.activate
    def test_check(self):
        """
        Testing Storm check.
        """
        self.load_check(self.STORM_CHECK_CONFIG, {})

        responses.add(
            responses.GET,
            'http://localhost:9005/api/v1/cluster/summary',
            json=TEST_STORM_CLUSTER_SUMMARY,
            status=200
        )
        responses.add(
            responses.GET,
            'http://localhost:9005/api/v1/nimbus/summary',
            json=TEST_STORM_NIMBUSES_SUMMARY,
            status=200
        )
        responses.add(
            responses.GET,
            'http://localhost:9005/api/v1/supervisor/summary',
            json=TEST_STORM_SUPERVISOR_SUMMARY,
            status=200
        )
        responses.add(
            responses.GET,
            'http://localhost:9005/api/v1/topology/summary',
            json=TEST_STORM_TOPOLOGY_SUMMARY,
            status=200
        )
        responses.add(
            responses.GET,
            'http://localhost:9005/api/v1/topology/my_topology-1-1489183263',
            json=TEST_STORM_TOPOLOGY_RESP,
            status=200
        )

        # run your actual tests...
        self.run_check(self.STORM_CHECK_CONFIG['instances'][0])

        # Service Check
        self.assertServiceCheck(
            'topology-check.my_topology',
            count=1,
            status=AgentCheck.OK,
            tags=['#env:test', '#environment:test']
        )

        # Cluster Stats
        self.assertMetric(
            'storm.cluster.executorsTotal',
            count=1,
            value=33
        )
        self.assertMetric(
            'storm.cluster.slotsTotal',
            count=1,
            value=10
        )
        self.assertMetric(
            'storm.cluster.slotsFree',
            count=1,
            value=4
        )
        self.assertMetric(
            'storm.cluster.topologies',
            count=1,
            value=1
        )
        self.assertMetric(
            'storm.cluster.supervisors',
            count=1,
            value=1
        )
        self.assertMetric(
            'storm.cluster.tasksTotal',
            count=1,
            value=33
        )
        self.assertMetric(
            'storm.cluster.slotsUsed',
            count=1,
            value=6
        )

        # Nimbus Stats
        self.assertMetric(
            'storm.nimbus.upTimeSeconds',
            count=1,
            value=25842
        )
        self.assertMetric(
            'storm.nimbus.numLeaders',
            count=1,
            value=1
        )
        self.assertMetric(
            'storm.nimbus.numFollowers',
            count=1,
            value=0
        )
        self.assertMetric(
            'storm.nimbus.numOffline',
            count=1,
            value=1
        )
        self.assertMetric(
            'storm.nimbus.numDead',
            count=1,
            value=0
        )

        # Supervisor Stats
        self.assertMetric(
            'storm.supervisor.uptimeSeconds',
            count=1,
            value=31559
        )
        self.assertMetric(
            'storm.supervisor.slotsTotal',
            count=1,
            value=10
        )
        self.assertMetric(
            'storm.supervisor.slotsUsed',
            count=1,
            value=6
        )
        self.assertMetric(
            'storm.supervisor.totalMem',
            count=1,
            value=3072
        )
        self.assertMetric(
            'storm.supervisor.usedMem',
            count=1,
            value=4992
        )
        self.assertMetric(
            'storm.supervisor.totalCpu',
            count=1,
            value=900
        )
        self.assertMetric(
            'storm.supervisor.usedCpu',
            count=1,
            value=0
        )

        # Topology Stats
        self.assertMetric(
            'storm.topologyStats.alltime.emitted',
            value=307606,
            tags=['#env:test', '#environment:test', '#topology:my_topology'],
            count=1,
            metric_type='gauge'
        )
        self.assertMetric(
            'storm.topologyStats.alltime.transferred',
            value=307606,
            tags=['#env:test', '#environment:test', '#topology:my_topology'],
            count=1,
            metric_type='gauge'
        )
        self.assertMetric(
            'storm.topologyStats.alltime.acked',
            value=104673,
            tags=['#env:test', '#environment:test', '#topology:my_topology'],
            count=1,
            metric_type='gauge'
        )
        self.assertMetric(
            'storm.topologyStats.alltime.failed',
            value=0,
            tags=['#env:test', '#environment:test', '#topology:my_topology'],
            count=1,
            metric_type='gauge'
        )
        self.assertMetric(
            'storm.topologyStats.alltime.completeLatency',
            value=285.950,
            tags=['#env:test', '#environment:test', '#topology:my_topology'],
            count=1,
            metric_type='gauge'
        )
        self.assertMetric(
            'storm.topologyStats.uptimeSeconds',
            value=1525788,
            tags=['#env:test', '#environment:test', '#topology:my_topology'],
            count=1,
            metric_type='gauge'
        )
        self.assertMetric(
            'storm.topologyStats.executorsTotal',
            value=33,
            tags=['#env:test', '#environment:test', '#topology:my_topology'],
            count=1,
            metric_type='gauge'
        )
        self.assertMetric(
            'storm.topologyStats.numBolts',
            value=6,
            tags=['#env:test', '#environment:test', '#topology:my_topology'],
            count=1,
            metric_type='gauge'
        )
        self.assertMetric(
            'storm.topologyStats.replicationCount',
            value=1,
            tags=['#env:test', '#environment:test', '#topology:my_topology'],
            count=1,
            metric_type='gauge'
        )
        self.assertMetric(
            'storm.topologyStats.tasksTotal',
            value=33,
            tags=['#env:test', '#environment:test', '#topology:my_topology'],
            count=1,
            metric_type='gauge'
        )
        self.assertMetric(
            'storm.topologyStats.numSpouts',
            value=1,
            tags=['#env:test', '#environment:test', '#topology:my_topology'],
            count=1,
            metric_type='gauge'
        )
        self.assertMetric(
            'storm.topologyStats.workersTotal',
            value=6,
            tags=['#env:test', '#environment:test', '#topology:my_topology'],
            count=1,
            metric_type='gauge'
        )

        # Bolt Stats
        for name, values in [
            ('Bolt1', (3, 0.001, 201.474, 0.000, 0, 212282, 101309, 106311, 101309, 3, 1E10)),
            ('Bolt2', (2, 0.015, 0.010, 0.000, 0, 3153, 0, 3153, 0, 2, 1E10)),
            ('Bolt3', (3, 0.009, 0.003, 0.000, 0, 4704, 0, 4704, 0, 3, 1E10)),
            ('Bolt4', (4, 0.001, 291.756, 0.000, 0, 218808, 101607, 110946, 101607, 4, 1E10)),
            ('Bolt5', (2, 0.001, 1014.634, 0.000, 0, 208890, 17, 104445, 17, 2, 1E10)),
            ('Bolt6', (3, 0.010, 0.005, 0.000, 0, 4705, 0, 4705, 0, 3, 1E10))
        ]:
            self.assertMetric(
                'storm.bolt.tasks',
                value=values[0],
                tags=['#env:test', '#environment:test', '#topology:my_topology', '#bolt:' + name],
                count=1,
                metric_type='gauge'
            )
            self.assertMetric(
                'storm.bolt.executeLatency',
                value=values[1],
                tags=['#env:test', '#environment:test', '#topology:my_topology', '#bolt:' + name],
                count=1,
                metric_type='gauge'
            )
            self.assertMetric(
                'storm.bolt.processLatency',
                value=values[2],
                tags=['#env:test', '#environment:test', '#topology:my_topology', '#bolt:' + name],
                count=1,
                metric_type='gauge'
            )
            self.assertMetric(
                'storm.bolt.capacity',
                value=values[3],
                tags=['#env:test', '#environment:test', '#topology:my_topology', '#bolt:' + name],
                count=1,
                metric_type='gauge'
            )
            self.assertMetric(
                'storm.bolt.failed',
                value=values[4],
                tags=['#env:test', '#environment:test', '#topology:my_topology', '#bolt:' + name],
                count=1,
                metric_type='gauge'
            )
            self.assertMetric(
                'storm.bolt.acked',
                value=values[5],
                tags=['#env:test', '#environment:test', '#topology:my_topology', '#bolt:' + name],
                count=1,
                metric_type='gauge'
            )
            self.assertMetric(
                'storm.bolt.transferred',
                value=values[6],
                tags=['#env:test', '#environment:test', '#topology:my_topology', '#bolt:' + name],
                count=1,
                metric_type='gauge'
            )
            self.assertMetric(
                'storm.bolt.executed',
                value=values[7],
                tags=['#env:test', '#environment:test', '#topology:my_topology', '#bolt:' + name],
                count=1,
                metric_type='gauge'
            )
            self.assertMetric(
                'storm.bolt.emitted',
                value=values[8],
                tags=['#env:test', '#environment:test', '#topology:my_topology', '#bolt:' + name],
                count=1,
                metric_type='gauge'
            )
            self.assertMetric(
                'storm.bolt.executors',
                value=values[9],
                tags=['#env:test', '#environment:test', '#topology:my_topology', '#bolt:' + name],
                count=1,
                metric_type='gauge'
            )
            self.assertMetric(
                'storm.bolt.errorLapsedSecs',
                value=values[10],
                tags=['#env:test', '#environment:test', '#topology:my_topology', '#bolt:' + name],
                count=1,
                metric_type='gauge'
            )

        # Spout Stats
        for name, values in [
            ('source', (8, 285.950, 0, 104673, 104673, 104673, 8, 38737)),
        ]:
            self.assertMetric(
                'storm.spout.tasks',
                value=values[0],
                tags=['#env:test', '#environment:test', '#topology:my_topology', '#spout:' + name],
                count=1,
                metric_type='gauge'
            )
            self.assertMetric(
                'storm.spout.completeLatency',
                value=values[1],
                tags=['#env:test', '#environment:test', '#topology:my_topology', '#spout:' + name],
                count=1,
                metric_type='gauge'
            )
            self.assertMetric(
                'storm.spout.failed',
                value=values[2],
                tags=['#env:test', '#environment:test', '#topology:my_topology', '#spout:' + name],
                count=1,
                metric_type='gauge'
            )
            self.assertMetric(
                'storm.spout.acked',
                value=values[3],
                tags=['#env:test', '#environment:test', '#topology:my_topology', '#spout:' + name],
                count=1,
                metric_type='gauge'
            )
            self.assertMetric(
                'storm.spout.transferred',
                value=values[4],
                tags=['#env:test', '#environment:test', '#topology:my_topology', '#spout:' + name],
                count=1,
                metric_type='gauge'
            )
            self.assertMetric(
                'storm.spout.emitted',
                value=values[5],
                tags=['#env:test', '#environment:test', '#topology:my_topology', '#spout:' + name],
                count=1,
                metric_type='gauge'
            )
            self.assertMetric(
                'storm.spout.executors',
                value=values[6],
                tags=['#env:test', '#environment:test', '#topology:my_topology', '#spout:' + name],
                count=1,
                metric_type='gauge'
            )
            self.assertMetric(
                'storm.spout.errorLapsedSecs',
                value=values[7],
                tags=['#env:test', '#environment:test', '#topology:my_topology', '#spout:' + name],
                count=1,
                metric_type='gauge'
            )

        # Raises when COVERAGE=true and coverage < 100%
        self.coverage_report()
