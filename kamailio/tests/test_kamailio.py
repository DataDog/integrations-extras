# import re
# from os import path
import collections
import datetime
import multiprocessing
import subprocess  # noqa: F401
import time
from os import getppid
from unittest import mock

import docker
import psutil
import pytest
import requests

from datadog_checks.base import ConfigurationError
from datadog_checks.dev.http import MockResponse
from datadog_checks.kamailio import KamailioCheck
from datadog_checks.kamailio.common import KAMAGENT_RUN_SCRIPT, NAMESPACE, TRACKED_METRICS

from .common import (
    MOCK_JSONRPC_RESPONSE_CORE_MODULES,
    MOCK_JSONRPC_RESPONSE_CORE_VERSION,
    MOCK_JSONRPC_RESPONSE_DISPATCHER_LIST,
    MOCK_JSONRPC_RESPONSE_STATS_ALL,
    MOCK_JSONRPC_RESPONSE_TM_STATS,
    MOCK_KAMCMD_RESPONSE_CORE_MODULES,
    MOCK_KAMCMD_RESPONSE_CORE_VERSION,
    MOCK_KAMCMD_RESPONSE_DISPATCHER_LIST,
    MOCK_KAMCMD_RESPONSE_STATS_ALL,
    MOCK_KAMCMD_RESPONSE_TM_STATS,
)

# our test container uses the tmx module stats, not the tm stats
DOCKER_TRACKED_METRICS = {k: v for k, v in TRACKED_METRICS.items() if k[0:3] != 'tm.'}

# scripts on the container are not located in site-packages as would be when installing the wheel
DOCKER_KAMAGENT_RUN_SCRIPT = '/opt/datadog-agent/scripts/run.sh'


class MockProcess(object):
    def __init__(self, pid=None, name=None, create_time=None, ppid=None, cmdline=None, status="sleeping"):
        # if pid is not specified find an open one that won't be used by another proc
        if pid is None:
            p = multiprocessing.Process(target=lambda: time.sleep(0.001))
            p.start()
            self._pid = p.pid
            p.terminate()
        else:
            self._pid = pid
        self._name = name
        self._create_time = create_time if create_time is not None else datetime.datetime.now().timestamp()
        self._ppid = ppid if ppid is not None else getppid()
        self._cmdline = cmdline if cmdline is not None else [name]
        self._status = status

        self._gone = False
        self._pid_reused = False
        self._hash = None
        self.info = None

        self._exitcode = object()
        self._ident = (self.pid, self._create_time)

    def __str__(self):
        info = collections.OrderedDict()
        info["pid"] = self.pid
        if self._name:
            info["name"] = self._name
        with self.oneshot():
            try:
                info["name"] = self.name()
                info["status"] = self.status()
            except psutil.ZombieProcess:
                info["status"] = "zombie"
            except psutil.NoSuchProcess:
                info["status"] = "terminated"
            except psutil.AccessDenied:
                pass
            if self._exitcode not in (object, None):
                info["exitcode"] = self._exitcode
            if self._create_time:
                info["started"] = datetime.datetime.fromtimestamp(self._create_time).strftime("%Y-%m-%d %H:%M:%S")
            return "%s.%s(%s)" % (
                self.__class__.__module__,
                self.__class__.__name__,
                ", ".join(["%s=%r" % (k, v) for k, v in info.items()]),
            )

    __repr__ = __str__

    def __eq__(self, other):
        if not isinstance(other, (MockProcess, psutil.Process)):
            return NotImplemented
        return self._ident == other._ident

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(self._ident)
        return self._hash

    @property
    def pid(self):
        return self._pid

    def oneshot(self):
        raise NotImplementedError()

    def as_dict(self, attrs=None, ad_value=None):
        valid_names = {"pid", "cmdline", "create_time", "name", "status", "ppid"}
        if attrs is not None:
            if not isinstance(attrs, (list, tuple, set, frozenset)):
                raise TypeError("invalid attrs type %s" % type(attrs))
            attrs = set(attrs)
            invalid_names = attrs - valid_names
            if invalid_names:
                raise ValueError(
                    "invalid attr name%s %s"
                    % ("s" if len(invalid_names) > 1 else "", ", ".join(map(repr, invalid_names)))
                )

        retdict = dict()
        ls = attrs or valid_names
        for name in ls:
            try:
                if name == "pid":
                    ret = self.pid
                else:
                    meth = getattr(self, name)
                    ret = meth()
            except (psutil.AccessDenied, psutil.ZombieProcess):
                ret = ad_value
            except NotImplementedError:
                if attrs:
                    raise
                continue
            retdict[name] = ret
        return retdict

    def parent(self):
        return psutil.Process(self.ppid())

    def parents(self):
        raise NotImplementedError()

    def is_running(self):
        if self._gone or self._pid_reused:
            return False
        try:
            return not (self != psutil.Process(self.pid))
        except psutil.ZombieProcess:
            # We should never get here as it's already handled in
            # Process.__init__; here just for extra safety.
            return True
        except psutil.NoSuchProcess:
            self._gone = True
            return False

    def cmdline(self):
        return self._cmdline

    def status(self):
        return self._status

    def ppid(self):
        return self._ppid

    def name(self):
        return self._name

    def cwd(self):
        raise NotImplementedError()

    def username(self):
        raise NotImplementedError()

    def exe(self):
        raise NotImplementedError()

    def create_time(self):
        return self._create_time

    def nice(self, value=None):
        raise NotImplementedError()

    def uids(self):
        raise NotImplementedError()

    def gids(self):
        raise NotImplementedError()

    def terminal(self):
        raise NotImplementedError()

    def num_fds(self):
        raise NotImplementedError()

    def io_counters(self):
        raise NotImplementedError()

    def ionice(self, ioclass=None, value=None):
        raise NotImplementedError()

    def rlimit(self, resource, limits=None):
        raise NotImplementedError()

    def cpu_affinity(self, cpus=None):
        raise NotImplementedError()

    def cpu_num(self):
        raise NotImplementedError()

    def environ(self):
        raise NotImplementedError()

    def num_handles(self):
        raise NotImplementedError()

    def num_ctx_switches(self):
        raise NotImplementedError()

    def num_threads(self):
        raise NotImplementedError()

    def threads(self):
        raise NotImplementedError()

    def children(self, recursive=False):
        raise NotImplementedError()

    def cpu_percent(self, interval=None):
        raise NotImplementedError()

    def cpu_times(self):
        raise NotImplementedError()

    def memory_info(self):
        raise NotImplementedError()

    def memory_full_info(self):
        raise NotImplementedError()

    def memory_percent(self, memtype="rss"):
        raise NotImplementedError()

    def memory_maps(self, grouped=True):
        raise NotImplementedError()

    def open_files(self):
        raise NotImplementedError()

    def connections(self, kind="inet"):
        raise NotImplementedError()

    def send_signal(self, sig):
        raise NotImplementedError()

    def suspend(self):
        raise NotImplementedError()

    def resume(self):
        raise NotImplementedError()

    def terminate(self):
        raise NotImplementedError()

    def kill(self):
        raise NotImplementedError()

    def wait(self, timeout=None):
        raise NotImplementedError()


class MockPopen(object):
    def __init__(self, args, *_args, **kwargs):
        self.args = args

        # the mocked outputs
        try:
            self._stdout = kwargs["mock_stdout"]
        except KeyError:
            self._stdout = None
        try:
            self._stderr = kwargs["mock_stderr"]
        except KeyError:
            self._stderr = None

        # always success
        self.returncode = 0

    def __enter__(self):
        return self

    def communicate(self, input=None, timeout=None):
        return (self._stdout, self._stderr)

    def poll(self):
        raise NotImplementedError()

    def wait(self, timeout=None):
        raise NotImplementedError()

    def send_signal(self, sig):
        raise NotImplementedError()

    def terminate(self):
        raise NotImplementedError()

    def kill(self):
        raise NotImplementedError()


def mockProcessIterFormat(proc, attrs, ad_value):
    proc.info = proc.as_dict(attrs=attrs, ad_value=ad_value)
    return proc


def mockPsutilIterServicesDown(attrs=None, ad_value=None):
    yield mockProcessIterFormat(MockProcess(name="systemd", cmdline=["/sbin/init"]), attrs, ad_value)


def mockPsutilIterServicesUp(attrs=None, ad_value=None):
    yield mockProcessIterFormat(MockProcess(name="systemd", cmdline=["/sbin/init"]), attrs, ad_value)
    yield mockProcessIterFormat(
        MockProcess(
            name="kamailio",
            cmdline=[
                "/usr/sbin/kamailio",
                "-f",
                "/etc/kamailio/kamailio.cfg",
            ],
        ),
        attrs,
        ad_value,
    )


def mockPsutilIterServicesUpWithMpath(attrs=None, ad_value=None):
    yield mockProcessIterFormat(MockProcess(name="systemd", cmdline=["/sbin/init"]), attrs, ad_value)
    yield mockProcessIterFormat(
        MockProcess(
            name="kamailio",
            cmdline=[
                "/usr/sbin/kamailio",
                "-f",
                "/etc/kamailio/kamailio.cfg",
                "-L",
                "/usr/lib/x86_64-linux-gnu/kamailio/modules/",
            ],
        ),
        attrs,
        ad_value,
    )


def mockSubprocessPopenKamcmdResponseOk(*args, **kwargs):
    if args[0][0] == KAMAGENT_RUN_SCRIPT:
        cmd = args[0][1]
    else:
        cmd = args[0][0]

    if cmd != 'kamcmd':
        raise NotImplementedError()

    method = args[0][args[0].index(cmd) + 1]
    if method == "core.version":
        return MockPopen(args[0], mock_stdout=MOCK_KAMCMD_RESPONSE_CORE_VERSION, mock_stderr=b"")
    elif method == "core.modules":
        return MockPopen(args[0], mock_stdout=MOCK_KAMCMD_RESPONSE_CORE_MODULES, mock_stderr=b"")
    elif method == "stats.get_statistics":
        if kwargs["json"]["params"][0] == "all":
            return MockPopen(args[0], mock_stdout=MOCK_KAMCMD_RESPONSE_STATS_ALL, mock_stderr=b"")
        else:
            raise NotImplementedError()
    elif method == "dispatcher.list":
        return MockPopen(args[0], mock_stdout=MOCK_KAMCMD_RESPONSE_DISPATCHER_LIST, mock_stderr=b"")
    elif method == "tm.stats":
        return MockPopen(args[0], mock_stdout=MOCK_KAMCMD_RESPONSE_TM_STATS, mock_stderr=b"")
    else:
        raise NotImplementedError()


def mockSubprocessPopenKamcmdResponsePermissionDenied(*args, **kwargs):
    if args[0][0] == KAMAGENT_RUN_SCRIPT:
        cmd = args[0][1]
    else:
        cmd = args[0][0]

    if cmd != 'kamcmd':
        raise NotImplementedError()

    return MockPopen(
        args[0],
        mock_stdout=b"",
        mock_stderr=b"ERROR: connect_unix_sock: connect(/var/run/kamailio//kamailio_ctl): Permission denied [13]\n",
    )


def mockSubprocessPopenKamcmdAndKamgetmodulesResponseOk(*args, **kwargs):
    if args[0][0] == KAMAGENT_RUN_SCRIPT:
        cmd = args[0][1]
    else:
        cmd = args[0][0]

    if cmd == 'kamcmd':
        method = args[0][args[0].index(cmd) + 1]
        if method == "core.version":
            return MockPopen(args[0], mock_stdout=MOCK_KAMCMD_RESPONSE_CORE_VERSION, mock_stderr=b"")
        elif method == "core.modules":
            return MockPopen(args[0], mock_stdout=MOCK_KAMCMD_RESPONSE_CORE_MODULES, mock_stderr=b"")
        elif method == "stats.get_statistics":
            if kwargs["json"]["params"][0] == "all":
                return MockPopen(args[0], mock_stdout=MOCK_KAMCMD_RESPONSE_STATS_ALL, mock_stderr=b"")
            else:
                raise NotImplementedError()
        elif method == "dispatcher.list":
            return MockPopen(args[0], mock_stdout=MOCK_KAMCMD_RESPONSE_DISPATCHER_LIST, mock_stderr=b"")
        elif method == "tm.stats":
            return MockPopen(args[0], mock_stdout=MOCK_KAMCMD_RESPONSE_TM_STATS, mock_stderr=b"")
        else:
            raise NotImplementedError()
    elif cmd == 'getmodules':
        return MockPopen(args[0], mock_stdout=MOCK_KAMCMD_RESPONSE_CORE_MODULES, mock_stderr=b"")
    else:
        raise NotImplementedError()


def mockSubprocessPopenKamcmdAndKamgetmodulesPermissionDenied(*args, **kwargs):
    if args[0][0] == KAMAGENT_RUN_SCRIPT:
        cmd = args[0][1]
    else:
        cmd = args[0][0]

    if cmd == 'kamcmd':
        method = args[0][args[0].index(cmd) + 1]
        if method == "core.version":
            return MockPopen(args[0], mock_stdout=MOCK_KAMCMD_RESPONSE_CORE_VERSION, mock_stderr=b"")
        elif method == "core.modules":
            return MockPopen(args[0], mock_stdout=MOCK_KAMCMD_RESPONSE_CORE_MODULES, mock_stderr=b"")
        elif method == "stats.get_statistics":
            if kwargs["json"]["params"][0] == "all":
                return MockPopen(args[0], mock_stdout=MOCK_KAMCMD_RESPONSE_STATS_ALL, mock_stderr=b"")
            else:
                raise NotImplementedError()
        elif method == "dispatcher.list":
            return MockPopen(args[0], mock_stdout=MOCK_KAMCMD_RESPONSE_DISPATCHER_LIST, mock_stderr=b"")
        elif method == "tm.stats":
            return MockPopen(args[0], mock_stdout=MOCK_KAMCMD_RESPONSE_TM_STATS, mock_stderr=b"")
        else:
            raise NotImplementedError()
    elif cmd == 'getmodules':
        return MockPopen(
            args[0],
            mock_stdout=b"",
            mock_stderr=(
                b'Traceback (most recent call last):\n'
                b'  File "/usr/local/lib/python3.7/dist-packages/psutil/_common.py", line 443, '
                b'in wrapper\n'
                b'    ret = self._cache[fun]\n'
                b'AttributeError: _cache\n\n'
                b'During handling of the above exception, '
                b'another exception occurred:\n\n'
                b'Traceback (most recent call last):\n  File '
                b'"/usr/local/lib/python3.7/dist-packages/psutil/_pslinux.py", line 1645, in wrapper\n'
                b'    return fun(self, *args, '
                b'**kwargs)\n'
                b'  File "/usr/local/lib/python3.7/dist-packages/psutil/_common.py", line 446, in wrapper\n'
                b'    return fun('
                b'self)\n'
                b'  File "/usr/local/lib/python3.7/dist-packages/psutil/_pslinux.py", line 1723, in _read_smaps_file\n'
                b'    with '
                b'open_binary("%s/%s/smaps" % (self._procfs_path, self.pid)) as f:\n'
                b'  File '
                b'"/usr/local/lib/python3.7/dist-packages/psutil/_common.py", line 728, in open_binary\n'
                b'    return open(fname, "rb", '
                b'buffering=FILE_READ_BUFFER_SIZE)\n'
                b'PermissionError: [Errno 13] Permission denied: \'/proc/17348/smaps\'\n\n'
                b'During handling '
                b'of the above exception, another exception occurred:\n\n'
                b'Traceback (most recent call last):\n'
                b'  File "/tmp/kamgetmodules", '
                b'line 14, in <module>\n'
                b'    for mmap in proc.memory_maps():\n'
                b'  File '
                b'"/usr/local/lib/python3.7/dist-packages/psutil/__init__.py", line 1121, in memory_maps\n'
                b'    it = self._proc.memory_maps('
                b')\n'
                b'  File "/usr/local/lib/python3.7/dist-packages/psutil/_pslinux.py", line 1645, in wrapper\n'
                b'    return fun(self, *args, '
                b'**kwargs)\n'
                b'  File "/usr/local/lib/python3.7/dist-packages/psutil/_pslinux.py", line 1980, in memory_maps\n'
                b'    data = '
                b'self._read_smaps_file()\n'
                b'  File "/usr/local/lib/python3.7/dist-packages/psutil/_pslinux.py", line 1647, in wrapper\n    '
                b'raise AccessDenied(self.pid, self._name)\n'
                b'psutil.AccessDenied: (pid=17348, name=\'kamailio\')\n'
            ),
        )
    else:
        raise NotImplementedError()


def mockRequestsPostJsonrpcHttpError(*args, **kwargs):
    raise requests.exceptions.HTTPError()


def mockRequestsPostJsonrpcResponse200(*args, **kwargs):
    method = kwargs["json"]["method"]
    if method == "core.version":
        return MockResponse(
            json_data=MOCK_JSONRPC_RESPONSE_CORE_VERSION,
            status_code=200,
        )
    elif method == "core.modules":
        return MockResponse(
            json_data=MOCK_JSONRPC_RESPONSE_CORE_MODULES,
            status_code=200,
        )
    elif method == "stats.get_statistics":
        if kwargs["json"]["params"][0] == "all":
            return MockResponse(
                json_data=MOCK_JSONRPC_RESPONSE_STATS_ALL,
                status_code=200,
            )
        else:
            raise NotImplementedError()
    elif method == "dispatcher.list":
        return MockResponse(
            json_data=MOCK_JSONRPC_RESPONSE_DISPATCHER_LIST,
            status_code=200,
        )
    elif method == "tm.stats":
        return MockResponse(
            json_data=MOCK_JSONRPC_RESPONSE_TM_STATS,
            status_code=200,
        )
    else:
        raise NotImplementedError()


def mockRequestsPostJsonrpcResponse301(*args, **kwargs):
    return MockResponse(status_code=301)


def mockRequestsPostJsonrpcResponse302(*args, **kwargs):
    return MockResponse(status_code=302)


def mockRequestsPostJsonrpcResponse307(*args, **kwargs):
    return MockResponse(status_code=307)


def mockRequestsPostJsonrpcResponse400(*args, **kwargs):
    return MockResponse(status_code=400)


def mockRequestsPostJsonrpcResponse401(*args, **kwargs):
    return MockResponse(status_code=401)


def mockRequestsPostJsonrpcResponse403(*args, **kwargs):
    return MockResponse(status_code=403)


def mockRequestsPostJsonrpcResponse404(*args, **kwargs):
    return MockResponse(status_code=404)


def mockRequestsPostJsonrpcResponse408(*args, **kwargs):
    return MockResponse(status_code=408)


def mockRequestsPostJsonrpcResponse500(*args, **kwargs):
    return MockResponse(status_code=500)


def dockerMockSubprocessPopen(*args, **kwargs):
    cmd = args[0]
    # commandline args as string
    if isinstance(cmd, str):
        cmd = cmd.replace(KAMAGENT_RUN_SCRIPT, DOCKER_KAMAGENT_RUN_SCRIPT)
    # otherwise must be an iterable
    elif cmd[0] == KAMAGENT_RUN_SCRIPT:
        cmd[0] = DOCKER_KAMAGENT_RUN_SCRIPT

    client = docker.from_env()
    container = client.containers.get('ddev-kamailio')

    res = container.exec_run(cmd, stdout=True, stderr=True, user='dd-agent', demux=True)[1]
    stdout = res[0] if res[0] is not None else b''
    stderr = res[1] if res[1] is not None else b''
    return MockPopen(args[0], mock_stdout=stdout, mock_stderr=stderr)


def dockerMockKamailiocheckIsprocalive(name):
    client = docker.from_env()
    container = client.containers.get('ddev-kamailio')

    res = container.exec_run(f'pidof {name}', stdout=False, stderr=False, user='dd-agent')[0]
    return res == 0


@pytest.mark.unit
def testBadInstanceConfig(dd_run_check, aggregator, instance_missing_configs):
    with pytest.raises(ConfigurationError):
        KamailioCheck("kamailio", {}, [instance_missing_configs])


@pytest.mark.unit
@mock.patch("tests.test_kamailio.subprocess.Popen", mockSubprocessPopenKamcmdResponsePermissionDenied)
@mock.patch("tests.test_kamailio.requests.post", mockRequestsPostJsonrpcResponse500)
def testFailureConfiguringKamcmd(dd_run_check, aggregator, instance_kamcmd):
    with pytest.raises(ConfigurationError):
        KamailioCheck("kamailio", {}, [instance_kamcmd])


@pytest.mark.unit
@mock.patch("tests.test_kamailio.requests.post", mockRequestsPostJsonrpcResponse200)
def testSuccessConfiguringKamcmdAsJsonrpcNoauth(dd_run_check, aggregator, instance_jsonrpc_noauth):
    KamailioCheck("kamailio", {}, [instance_jsonrpc_noauth])


@pytest.mark.unit
@mock.patch("tests.test_kamailio.requests.post", mockRequestsPostJsonrpcResponse200)
def testSuccessConfiguringKamcmdAsJsonrpcAuth(dd_run_check, aggregator, instance_jsonrpc_auth):
    KamailioCheck("kamailio", {}, [instance_jsonrpc_auth])


@pytest.mark.unit
@mock.patch("tests.test_kamailio.requests.post", mockRequestsPostJsonrpcResponse200)
def testSuccessConfiguringKamcmdAsJsonrpcRedirect(dd_run_check, aggregator, instance_jsonrpc_redirect):
    KamailioCheck("kamailio", {}, [instance_jsonrpc_redirect])


@pytest.mark.unit
@mock.patch("tests.test_kamailio.subprocess.Popen", mockSubprocessPopenKamcmdResponseOk)
@mock.patch("tests.test_kamailio.requests.post", mockRequestsPostJsonrpcResponse500)
def testSuccessConfiguringKamcmdAsKamcmd(dd_run_check, aggregator, instance_kamcmd):
    KamailioCheck("kamailio", {}, [instance_kamcmd])


@pytest.mark.unit
@mock.patch("tests.test_kamailio.subprocess.Popen", mockSubprocessPopenKamcmdAndKamgetmodulesPermissionDenied)
@mock.patch("tests.test_kamailio.requests.post", mockRequestsPostJsonrpcResponse500)
def testFailureConfiguringModulesFromMmaps(dd_run_check, aggregator, instance_using_mmaps):
    with pytest.raises(ConfigurationError):
        KamailioCheck("kamailio", {}, [instance_using_mmaps])


@pytest.mark.unit
@mock.patch("tests.test_kamailio.subprocess.Popen", mockSubprocessPopenKamcmdAndKamgetmodulesResponseOk)
@mock.patch("tests.test_kamailio.requests.post", mockRequestsPostJsonrpcResponse500)
def testSuccessConfiguringModulesFromMmaps(dd_run_check, aggregator, instance_using_mmaps):
    KamailioCheck("kamailio", {}, [instance_using_mmaps])


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
@mock.patch('datadog_checks.kamailio.check.subprocess.Popen', dockerMockSubprocessPopen)
@mock.patch('datadog_checks.kamailio.check.KamailioCheck.isProcAlive', dockerMockKamailiocheckIsprocalive)
def testIntegrationsViaDocker(dd_run_check, aggregator, dd_environment):
    for instance in dd_environment:
        c = KamailioCheck("kamailio", {}, [instance])
        dd_run_check(c)

        aggregator.assert_service_check("kamailio.services_up")
        aggregator.assert_no_duplicate_service_checks()

        for k, v in DOCKER_TRACKED_METRICS.items():
            aggregator.assert_metric(f"{NAMESPACE}.{k}", metric_type=aggregator.METRIC_ENUM_MAP[v["type"]])
        aggregator.assert_all_metrics_covered()

        aggregator.reset()
