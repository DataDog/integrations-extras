# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import pytest
from mock import MagicMock
from datadog_checks.bind9_check import bind9_check
import os
import urllib2
import xml.etree.ElementTree as ET
from datadog_checks.errors import CheckException

HERE = os.path.dirname(os.path.abspath(__file__))
URL = 'http://10.10.1.101:8080'

@pytest.fixture()
def aggregator():
    from datadog_checks.stubs import aggregator
    aggregator.reset()
    return aggregator

@pytest.fixture
def instance():
    data = {'url': URL}
    return data
EXPECTED_VALUES = (
    ('opcode_QUERY', 0),
    ('opcode_IQUERY', 0),
    ('opcode_STATUS', 0),
    ('opcode_RESERVED3', 0),
    ('opcode_NOTIFY', 0),
    ('opcode_UPDATE', 0),
    ('opcode_RESERVED6', 0),
    ('opcode_RESERVED7', 0),
    ('opcode_RESERVED8', 0),
    ('opcode_RESERVED9', 0),
    ('opcode_RESERVED10', 0),
    ('opcode_RESERVED11', 0),
    ('opcode_RESERVED12', 0),
    ('opcode_RESERVED13', 0),
    ('opcode_RESERVED14', 0),
    ('opcode_RESERVED15', 0),
    ('nsstat_Requestv4', 0),
    ('nsstat_Requestv6', 0),
    ('nsstat_ReqEdns0', 0),
    ('nsstat_ReqBadEDNSVer', 0),
    ('nsstat_ReqTSIG', 0),
    ('nsstat_ReqSIG0', 0),
    ('nsstat_ReqBadSIG', 0),
    ('nsstat_ReqTCP', 0),
    ('nsstat_AuthQryRej', 0),
    ('nsstat_RecQryRej', 0),
    ('nsstat_XfrRej', 0),
    ('nsstat_UpdateRej', 0),
    ('nsstat_Response', 0),
    ('nsstat_TruncatedResp', 0),
    ('nsstat_RespEDNS0', 0),
    ('nsstat_RespTSIG', 0),
    ('nsstat_RespSIG0', 0),
    ('nsstat_QrySuccess', 0),
    ('nsstat_QryAuthAns', 0),
    ('nsstat_QryNoauthAns', 0),
    ('nsstat_QryReferral', 0),
    ('nsstat_QryNxrrset', 0),
    ('nsstat_QrySERVFAIL', 0),
    ('nsstat_QryFORMERR', 0),
    ('nsstat_QryNXDOMAIN', 0),
    ('nsstat_QryRecursion', 0),
    ('nsstat_QryDuplicate', 0),
    ('nsstat_QryDropped', 0),
    ('nsstat_QryFailure', 0),
    ('nsstat_XfrReqDone', 0),
    ('nsstat_UpdateReqFwd', 0),
    ('nsstat_UpdateRespFwd', 0),
    ('nsstat_UpdateFwdFail', 0),
    ('nsstat_UpdateDone', 0),
    ('nsstat_UpdateFail', 0),
    ('nsstat_UpdateBadPrereq', 0),
    ('nsstat_RecursClients', 0),
    ('nsstat_DNS64', 0),
    ('nsstat_RateDropped', 0),
    ('nsstat_RateSlipped', 0),
    ('nsstat_RPZRewrites', 0),
    ('nsstat_QryUDP', 0),
    ('nsstat_QryTCP', 0),
    ('nsstat_NSIDOpt', 0),
    ('nsstat_ExpireOpt', 0),
    ('nsstat_OtherOpt', 0),
    ('nsstat_SitOpt', 0),
    ('nsstat_SitNew', 0),
    ('nsstat_SitBadSize', 0),
    ('nsstat_SitBadTime', 0),
    ('nsstat_SitNoMatch', 0),
    ('nsstat_SitMatch', 0),
    ('zonestat_NotifyOutv4', 0),
    ('zonestat_NotifyOutv6', 0),
    ('zonestat_NotifyInv4', 0),
    ('zonestat_NotifyInv6', 0),
    ('zonestat_NotifyRej', 0),
    ('zonestat_SOAOutv4', 0),
    ('zonestat_SOAOutv6', 0),
    ('zonestat_AXFRReqv4', 0),
    ('zonestat_AXFRReqv6', 0),
    ('zonestat_IXFRReqv4', 0),
    ('zonestat_IXFRReqv6', 0),
    ('zonestat_XfrSuccess', 0),
    ('zonestat_XfrFail', 0),
    ('sockstat_UDP4Open', 11),
    ('sockstat_UDP6Open', 5),
    ('sockstat_TCP4Open', 8),
    ('sockstat_TCP6Open', 2),
    ('sockstat_UnixOpen', 0),
    ('sockstat_RawOpen', 1),
    ('sockstat_UDP4OpenFail', 0),
    ('sockstat_UDP6OpenFail', 0),
    ('sockstat_TCP4OpenFail', 0),
    ('sockstat_TCP6OpenFail', 0),
    ('sockstat_UnixOpenFail', 0),
    ('sockstat_RawOpenFail', 0),
    ('sockstat_UDP4Close', 5),
    ('sockstat_UDP6Close', 3),
    ('sockstat_TCP4Close', 93),
    ('sockstat_TCP6Close', 0),
    ('sockstat_UnixClose', 0),
    ('sockstat_FDWatchClose', 0),
    ('sockstat_RawClose', 0),
    ('sockstat_UDP4BindFail', 0),
    ('sockstat_UDP6BindFail', 0),
    ('sockstat_TCP4BindFail', 0),
    ('sockstat_TCP6BindFail', 0),
    ('sockstat_UnixBindFail', 0),
    ('sockstat_FdwatchBindFail', 0),
    ('sockstat_UDP4ConnFail', 0),
    ('sockstat_UDP6ConnFail', 3),
    ('sockstat_TCP4ConnFail', 0),
    ('sockstat_TCP6ConnFail', 0),
    ('sockstat_UnixConnFail', 0),
    ('sockstat_FDwatchConnFail', 0),
    ('sockstat_UDP4Conn', 5),
    ('sockstat_UDP6Conn', 0),
    ('sockstat_TCP4Conn', 3),
    ('sockstat_TCP6Conn', 0),
    ('sockstat_UnixConn', 0),
    ('sockstat_FDwatchConn', 0),
    ('sockstat_TCP4AcceptFail', 0),
    ('sockstat_TCP6AcceptFail', 0),
    ('sockstat_UnixAcceptFail', 0),
    ('sockstat_TCP4Accept', 64),
    ('sockstat_TCP6Accept', 0),
    ('sockstat_UnixAccept', 0),
    ('sockstat_UDP4SendErr', 0),
    ('sockstat_UDP6SendErr', 3),
    ('sockstat_TCP4SendErr', 0),
    ('sockstat_TCP6SendErr', 0),
    ('sockstat_UnixSendErr', 0),
    ('sockstat_FDwatchSendErr', 0),
    ('sockstat_UDP4RecvErr', 0),
    ('sockstat_UDP6RecvErr', 0),
    ('sockstat_TCP4RecvErr', 0),
    ('sockstat_TCP6RecvErr', 0),
    ('sockstat_UnixRecvErr', 0),
    ('sockstat_FDwatchRecvErr', 0),
    ('sockstat_RawRecvErr', 0),
    ('sockstat_UDP4Active', 6),
    ('sockstat_UDP6Active', 2),
    ('sockstat_TCP4Active', 69),
    ('sockstat_TCP6Active', 2),
    ('sockstat_UnixActive', 0),
    ('sockstat_RawActive', 1)
)

Date = ["2018-08-08T01-15-46Z","2010-08-08T01-15-46Z"]
Epoch = ["1533671146","1281210346"]

def test_getStatsFromUrl() :
    c = bind9_check('bind9_check', {}, {}, None)
    with open(os.path.join(HERE,'sample_stats.xml'), 'r') as file :
        tree=ET.parse(file)
        root = tree.getroot()
        assert c.getStatsFromUrl(URL).attrib == root.attrib

def test_check(aggregator, instance) :
    c = bind9_check('bind9_check', {}, {}, None)
    with open(os.path.join(HERE,'sample_stats.xml'), 'r') as file :
        tree=ET.parse(file)
        root = tree.getroot()
        c.getStatsFromUrl = MagicMock(return_value=root)
    with pytest.raises(CheckException) :
        c.check({})
    c.check(instance)
    
    for metric, value in EXPECTED_VALUES:
        aggregator.assert_metric(metric, value=value)
    aggregator.assert_service_check(c.BIND_SERVICE_CHECK)
    aggregator.assert_all_metrics_covered()

def test_DateTimeToEpoch() :
    c = bind9_check('bind9_check', {}, {}, None)
    assert c.DateTimeToEpoch(Date[0]) == Epoch[0]
    assert c.DateTimeToEpoch(Date[1]) == Epoch[1]
