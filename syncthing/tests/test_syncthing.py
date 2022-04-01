from typing import Any, Callable, Dict

from datadog_checks.base import AgentCheck
from datadog_checks.base.stubs.aggregator import AggregatorStub
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.syncthing import SyncthingCheck


def test_check(dd_run_check, aggregator, instance, requests_mock):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None

    VERSION_RESPONSE = '''
    {
      "arch": "amd64",
      "os": "linux",
      "version": "v1.17.0"
    }'''

    STATUS_RESPONSE = '''
    {
      "myID": "MY-ID"
    }'''

    CONNECTIONS_RESPONSE = '''
    {
      "connections": {
        "ID1": {
          "connected": true,
          "paused": false
        },
        "ID2": {
          "connected": false,
          "paused": false
        },
        "ID3": {
          "connected": true,
          "paused": false
        }
      }
    }'''

    FOLDERS_RESPONSE = '''
    [
      {
        "id": "folder1"
      },
      {
        "id": "folder2"
      }
    ]'''

    FOLDER1_RESPONSE = '''
    {
      "errors": 1,
      "globalBytes": 1441988667,
      "globalDeleted": 2073,
      "globalDirectories": 245,
      "globalFiles": 1618,
      "globalSymlinks": 0,
      "globalTotalItems": 3936,
      "ignorePatterns": false,
      "inSyncBytes": 1441988667,
      "inSyncFiles": 1618,
      "invalid": "",
      "localBytes": 1441988667,
      "localDeleted": 2066,
      "localDirectories": 245,
      "localFiles": 1618,
      "localSymlinks": 0,
      "localTotalItems": 3929,
      "needBytes": 0,
      "needDeletes": 0,
      "needDirectories": 0,
      "needFiles": 0,
      "needSymlinks": 0,
      "needTotalItems": 0,
      "pullErrors": 1,
      "sequence": 20782,
      "state": "idle",
      "stateChanged": "2022-03-31T21:08:25+02:00",
      "version": 20782
    }'''

    FOLDER2_RESPONSE = '''
    {
      "errors": 0,
      "globalBytes": 1441988667,
      "globalDeleted": 2073,
      "globalDirectories": 245,
      "globalFiles": 1618,
      "globalSymlinks": 0,
      "globalTotalItems": 3936,
      "ignorePatterns": false,
      "inSyncBytes": 1441988667,
      "inSyncFiles": 1618,
      "invalid": "",
      "localBytes": 1441988667,
      "localDeleted": 2066,
      "localDirectories": 245,
      "localFiles": 1618,
      "localSymlinks": 0,
      "localTotalItems": 3929,
      "needBytes": 0,
      "needDeletes": 0,
      "needDirectories": 0,
      "needFiles": 0,
      "needSymlinks": 0,
      "needTotalItems": 0,
      "pullErrors": 0,
      "sequence": 20782,
      "state": "idle",
      "stateChanged": "2022-03-31T21:08:25+02:00",
      "version": 20782
    }'''

    ERROR_RESPONSE = '''
    {
      "errors": [
        {
          "when": "2014-09-18T12:59:26.549953186+02:00",
          "message": "This is an error string"
        }
      ]
    }'''

    requests_mock.get('http://localhost/rest/system/version', text=VERSION_RESPONSE)
    requests_mock.get('http://localhost/rest/system/status', text=STATUS_RESPONSE)
    requests_mock.get('http://localhost/rest/system/connections', text=CONNECTIONS_RESPONSE)
    requests_mock.get('http://localhost/rest/config/folders', text=FOLDERS_RESPONSE)
    requests_mock.get('http://localhost/rest/db/status?folder=folder1', text=FOLDER1_RESPONSE)
    requests_mock.get('http://localhost/rest/db/status?folder=folder2', text=FOLDER2_RESPONSE)
    requests_mock.get('http://localhost/rest/system/error', text=ERROR_RESPONSE)

    check = SyncthingCheck('syncthing', {}, [instance])
    dd_run_check(check)

    gtags = ['arch:amd64', 'os:linux', 'syncthing_id:MY-ID', 'syncthing_version:v1.17.0']
    aggregator.assert_metric('syncthing.connections.connected', tags=gtags)
    aggregator.assert_metric('syncthing.connections.paused', tags=gtags)
    aggregator.assert_metric('syncthing.connections.count', tags=gtags)
    aggregator.assert_metric('syncthing.errors', tags=gtags)

    for f in ['folder1', 'folder2']:
        ftags = list(gtags)
        ftags.append('folder:' + f)
        aggregator.assert_metric('syncthing.folder.bytes', tags=ftags)
        aggregator.assert_metric('syncthing.folder.errors', tags=ftags)
        aggregator.assert_metric('syncthing.folder.files', tags=ftags)
        aggregator.assert_metric('syncthing.folder.global.bytes', tags=ftags)
        aggregator.assert_metric('syncthing.folder.global.deleted', tags=ftags)
        aggregator.assert_metric('syncthing.folder.global.directories', tags=ftags)
        aggregator.assert_metric('syncthing.folder.global.files', tags=ftags)
        aggregator.assert_metric('syncthing.folder.global.total_items', tags=ftags)
        aggregator.assert_metric('syncthing.folder.local.bytes', tags=ftags)
        aggregator.assert_metric('syncthing.folder.local.deleted', tags=ftags)
        aggregator.assert_metric('syncthing.folder.local.directories', tags=ftags)
        aggregator.assert_metric('syncthing.folder.local.files', tags=ftags)
        aggregator.assert_metric('syncthing.folder.local.total_items', tags=ftags)
        aggregator.assert_metric('syncthing.folder.need.bytes', tags=ftags)
        aggregator.assert_metric('syncthing.folder.need.deletes', tags=ftags)
        aggregator.assert_metric('syncthing.folder.need.directories', tags=ftags)
        aggregator.assert_metric('syncthing.folder.need.files', tags=ftags)
        aggregator.assert_metric('syncthing.folder.need.total_items', tags=ftags)
        aggregator.assert_metric('syncthing.folder.pull_errors', tags=ftags)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


# def test_emits_critical_service_check_when_service_is_down(dd_run_check, aggregator, instance):
#    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
#    check = SyncthingCheck('syncthing', {}, [instance])
#    dd_run_check(check)
#   # aggregator.assert_service_check('syncthing.can_connect', SyncthingCheck.CRITICAL)
