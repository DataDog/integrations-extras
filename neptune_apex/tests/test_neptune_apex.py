from typing import Any, Callable, Dict

import pytest
import responses

from datadog_checks.base import AgentCheck, ConfigurationError
from datadog_checks.base.stubs.aggregator import AggregatorStub
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.neptune_apex import NeptuneApexCheck


@pytest.mark.unit
def test_config():
    instance = {}
    with pytest.raises(ConfigurationError):
        NeptuneApexCheck("neptune_apex", {}, [instance])

    instance = {"address": "http://127.0.0.1"}
    # this should not fail
    NeptuneApexCheck("neptune_apex", {}, [instance])


MOCK_STATUS_RESPONSE = """<?xml version="1.0"?>
<status software="5.10_8F22" hardware="1.0">
<hostname>MyReef</hostname>
<serial>ABC:12345</serial>
<timezone>-6.00</timezone>
<date>01/25/2023 18:12:42</date>
<power><failed>01/23/2023 20:38:08</failed>
<restored>01/23/2023 20:38:44</restored></power>
<probes>
<probe>
 <name>Tmp</name> <value>80.8 </value>
 <type>Temp</type></probe><probe>
 <name>pH</name> <value>8.04 </value>
 <type>pH</type></probe><probe>
 <name>ORP</name> <value>182  </value>
 <type>ORP</type></probe><probe>
 <name>LLS</name> <value>14.7 </value>
</probe><probe>
 <name>Light1_2_1A</name> <value>0.0  </value>
</probe><probe>
 <name>Light2_2_2A</name> <value>0.2  </value>
</probe><probe>
 <name>RetPump_2_3A</name> <value>0.0  </value>
</probe><probe>
 <name>Heater_2_4A</name> <value>0.0  </value>
</probe><probe>
 <name>HeaterL-2-1A</name> <value>0.0  </value>
</probe><probe>
 <name>Skimmer-2-2A</name> <value>0.0  </value>
</probe><probe>
 <name>RefLght_2_7A</name> <value>0.0  </value>
</probe><probe>
 <name>Fan_2_8A</name> <value>0.0  </value>
</probe><probe>
 <name>Light1_2_1W</name> <value>   0 </value>
</probe><probe>
 <name>Light2_2_2W</name> <value>  16 </value>
</probe><probe>
 <name>RetPump_2_3W</name> <value>   1 </value>
</probe><probe>
 <name>Heater_2_4W</name> <value>   1 </value>
</probe><probe>
 <name>HeaterL-2-1W</name> <value>   0 </value>
</probe><probe>
 <name>Skimmer-2-2W</name> <value>   0 </value>
</probe><probe>
 <name>RefLght_2_7W</name> <value>   1 </value>
</probe><probe>
 <name>Fan_2_8W</name> <value>   0 </value>
</probe><probe>
 <name>Volt_2</name> <value>117  </value>
</probe></probes>
<outlets>
<outlet>
 <name>VarSpd1_I1</name>
 <outputID>0</outputID>
 <state>PF1</state>
 <deviceID>base_Var1</deviceID>
</outlet>
<outlet>
 <name>VarSpd2_I2</name>
 <outputID>1</outputID>
 <state>PF2</state>
 <deviceID>base_Var2</deviceID>
</outlet>
<outlet>
 <name>VarSpd3_I3</name>
 <outputID>2</outputID>
 <state>PF3</state>
 <deviceID>base_Var3</deviceID>
</outlet>
<outlet>
 <name>VarSpd4_I4</name>
 <outputID>3</outputID>
 <state>PF4</state>
 <deviceID>base_Var4</deviceID>
</outlet>
<outlet>
 <name>SndAlm_I6</name>
 <outputID>4</outputID>
 <state>AOF</state>
 <deviceID>base_Alarm</deviceID>
</outlet>
<outlet>
 <name>SndWrn_I7</name>
 <outputID>5</outputID>
 <state>AOF</state>
 <deviceID>base_Warn</deviceID>
</outlet>
<outlet>
 <name>EmailAlm_I5</name>
 <outputID>6</outputID>
 <state>AOF</state>
 <deviceID>base_email</deviceID>
</outlet>
<outlet>
 <name>Email2Alm_I9</name>
 <outputID>7</outputID>
 <state>AOF</state>
 <deviceID>base_email2</deviceID>
</outlet>
<outlet>
 <name>Alarm_1_2</name>
 <outputID>8</outputID>
 <state>AOF</state>
 <deviceID>1_2</deviceID>
</outlet>
<outlet>
 <name>Light1_2_1</name>
 <outputID>9</outputID>
 <state>AON</state>
 <deviceID>2_1</deviceID>
</outlet>
<outlet>
 <name>Light2_2_2</name>
 <outputID>10</outputID>
 <state>AON</state>
 <deviceID>2_2</deviceID>
</outlet>
<outlet>
 <name>RetPump_2_3</name>
 <outputID>11</outputID>
 <state>AON</state>
 <deviceID>2_3</deviceID>
</outlet>
<outlet>
 <name>Heater_2_4</name>
 <outputID>12</outputID>
 <state>AON</state>
 <deviceID>2_4</deviceID>
</outlet>
<outlet>
 <name>HeaterL-2-1</name>
 <outputID>13</outputID>
 <state>AON</state>
 <deviceID>2_5</deviceID>
</outlet>
<outlet>
 <name>Skimmer-2-2</name>
 <outputID>14</outputID>
 <state>AON</state>
 <deviceID>2_6</deviceID>
</outlet>
<outlet>
 <name>RefLght_2_7</name>
 <outputID>15</outputID>
 <state>AON</state>
 <deviceID>2_7</deviceID>
</outlet>
<outlet>
 <name>Fan_2_8</name>
 <outputID>16</outputID>
 <state>AON</state>
 <deviceID>2_8</deviceID>
</outlet>
<outlet>
 <name>LinkA_2_9</name>
 <outputID>17</outputID>
 <state>AOF</state>
 <deviceID>2_9</deviceID>
</outlet>
<outlet>
 <name>LinkB_2_10</name>
 <outputID>18</outputID>
 <state>AOF</state>
 <deviceID>2_10</deviceID>
</outlet>
</outlets></status>
"""

MOCK_OUTLOG_RESPONSE = """<?xml version="1.0"?>
<outlog software="5.10_8F22" hardware="1.0">
<hostname>MyReef</hostname>
<serial>ABC:12345</serial>
<timezone>-6.00</timezone>
<record><date>01/28/2023 09:00:17</date>
<name>Skimmer</name>
<value>OFF</value></record>
<record><date>01/28/2023 09:31:36</date>
<name>ATO</name>
<value>OFF</value></record>
<record><date>01/28/2023 10:00:40</date>
<name>Heater-Right</name>
<value>OFF</value></record>
<record><date>01/28/2023 10:00:42</date>
<name>Heater-Left</name>
<value>OFF</value></record>
<record><date>01/28/2023 10:09:18</date>
<name>CanFilter</name>
<value>OFF</value></record>
<record><date>01/28/2023 10:41:02</date>
<name>CanFilter</name>
<value>ON</value></record>
<record><date>01/28/2023 10:41:32</date>
<name>CanFilter</name>
<value>OFF</value></record>
<record><date>01/28/2023 11:01:40</date>
<name>Heater-Left</name>
<value>ON</value></record>
<record><date>01/28/2023 11:01:41</date>
<name>Heater-Right</name>
<value>ON</value></record>
<record><date>01/28/2023 11:01:47</date>
<name>CanFilter</name>
<value>ON</value></record>
<record><date>01/28/2023 11:04:36</date>
<name>Skimmer</name>
<value>ON</value></record>
<record><date>01/28/2023 11:07:24</date>
<name>ATO</name>
<value>ON</value></record>
</outlog>
"""


@pytest.mark.integration
@pytest.mark.usefixtures("dd_environment")
@responses.activate
def test_check(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = NeptuneApexCheck("neptune_apex", {}, [instance])

    responses.add(
        responses.GET,
        "http://127.0.0.1/cgi-bin/status.xml",
        body=MOCK_STATUS_RESPONSE,
        status=200,
    )
    responses.add(
        responses.GET,
        "http://127.0.0.1/cgi-bin/outlog.xml",
        body=MOCK_OUTLOG_RESPONSE,
        status=200,
    )

    dd_run_check(check)

    # assert probes
    aggregator.assert_metric("neptune_apex.outlet.state", at_least=1)
    for m in ["lls", "unknown", "volt", "ph", "orp"]:
        aggregator.assert_metric("neptune_apex.probe.{}".format(m), at_least=1)
    # assert outlets
    tags = tags = [
        "controller_hardware:1.0",
        "controller_name:MyReef",
        "controller_serial:ABC:12345",
        "controller_software:5.10_8F22",
    ]
    checked_outlet_tags = (
        ["device_id:2_8", "id:16", "name:Fan_2_8", "outlet_type:outlet", "state:AON"],
        [
            "device_id:2_4",
            "id:12",
            "name:Heater_2_4",
            "outlet_type:outlet",
            "state:AON",
        ],
        [
            "device_id:2_2",
            "id:10",
            "name:Light2_2_2",
            "outlet_type:outlet",
            "state:AON",
        ],
        [
            "device_id:2_3",
            "id:11",
            "name:RetPump_2_3",
            "outlet_type:outlet",
            "state:AON",
        ],
        [
            "device_id:2_7",
            "id:15",
            "name:RefLght_2_7",
            "outlet_type:outlet",
            "state:AON",
        ],
        ["device_id:2_1", "id:9", "name:Light1_2_1", "outlet_type:outlet", "state:AON"],
        [
            "device_id:2_5",
            "id:13",
            "name:HeaterL-2-1",
            "outlet_type:outlet",
            "state:AON",
        ],
        [
            "device_id:2_6",
            "id:14",
            "name:Skimmer-2-2",
            "outlet_type:outlet",
            "state:AON",
        ],
    )
    for t in checked_outlet_tags:
        aggregator.assert_metric("neptune_apex.outlet.usage.watts", at_least=1, tags=tags + t)
        aggregator.assert_metric("neptune_apex.outlet.usage.amps", at_least=1, tags=tags + t)
    aggregator.assert_metric("neptune_apex.can_connect", at_least=1)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())

    # check for outlog
    event_tests = (
        ("Skimmer", "OFF"),
        ("ATO", "OFF"),
        ("Heater-Right", "OFF"),
        ("Heater-Left", "OFF"),
        ("CanFilter", "OFF"),
        ("Skimmer", "ON"),
        ("ATO", "ON"),
        ("Heater-Right", "ON"),
        ("Heater-Left", "ON"),
        ("CanFilter", "ON"),
    )
    for t in event_tests:
        aggregator.assert_event(
            "Outlet state was toggled for {} on {} ({}). Turned to {}.".format(t[0], "MyReef", "ABC:12345", t[1]),
            at_least=1,
        )


@pytest.mark.integration
@pytest.mark.usefixtures("dd_environment")
@responses.activate
def test_emits_critical_service_check_when_service_is_down(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = NeptuneApexCheck("neptune_apex", {}, [instance])

    responses.add(responses.GET, "http://127.0.0.1/cgi-bin/status.xml", body="oops", status=500)
    responses.add(responses.GET, "http://127.0.0.1/cgi-bin/outlog.xml", body="oops", status=500)

    with pytest.raises(Exception):
        dd_run_check(check)
    aggregator.assert_service_check("neptune_apex.can_connect", NeptuneApexCheck.CRITICAL)
