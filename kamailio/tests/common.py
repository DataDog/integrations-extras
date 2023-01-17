from os import path

HERE = path.dirname(path.abspath(__file__))

MOCK_INSTANCE_MISSING_CONFIGS = {}

MOCK_INSTANCE_USING_MMAPS = {
    "service_checks": ["kamailio"],
    "get_modules_from_mmaps": True,
    "min_collection_interval": 15,
}

MOCK_INSTANCE_JSONRPC_NOAUTH = {
    "service_checks": ["kamailio"],
    "jsonrpc_config": {
        "url": "http://localhost/rpc/noauth",
        "version": "2.0",
        "id": 1,
        "verify_ssl": False,
        "allow_redirects": False,
        "token": "",
    },
    "min_collection_interval": 15,
}

MOCK_INSTANCE_JSONRPC_AUTH = {
    "service_checks": ["kamailio"],
    "jsonrpc_config": {
        "url": "https://localhost/rpc/auth",
        "version": "2.0",
        "id": 1,
        "verify_ssl": False,
        "allow_redirects": False,
        "token": "ANerqjNJ6cwCibGQDxtCfGlgHM2qfzzj",
    },
    "min_collection_interval": 15,
}

MOCK_INSTANCE_JSONRPC_REDIRECT = {
    "service_checks": ["kamailio"],
    "jsonrpc_config": {
        "url": "http://localhost/redirect",
        "version": "2.0",
        "id": 1,
        "verify_ssl": False,
        "allow_redirects": True,
        "token": "",
    },
    "min_collection_interval": 15,
}

MOCK_INSTANCE_KAMCMD = {
    "service_checks": ["kamailio"],
    "min_collection_interval": 15,
}

MOCK_JSONRPC_RESPONSE_CORE_VERSION = {'jsonrpc': '2.0', 'result': 'kamailio 5.5.5 (x86_64/linux) ', 'id': 1}

MOCK_JSONRPC_RESPONSE_CORE_MODULES = {
    'jsonrpc': '2.0',
    'result': [
        'ndb_redis',
        'siptrace',
        'websocket',
        'dispatcher',
        'keepalive',
        'drouting',
        'pike',
        'rtpengine',
        'nathelper',
        'domain',
        'uac_redirect',
        'uac',
        'permissions',
        'auth_db',
        'auth',
        'sqlops',
        'rtimer',
        'dialog',
        'htable',
        'avpops',
        'cfgutils',
        'xmlops',
        'http_async_client',
        'jsonrpcs',
        'jansson',
        'json',
        'xhttp',
        'acc',
        'cfg_rpc',
        'ctl',
        'sanity',
        'xlog',
        'siputils',
        'textopsx',
        'textops',
        'dsiprouter',
        'registrar',
        'usrloc',
        'maxfwd',
        'pv',
        'path',
        'rr',
        'sl',
        'tmx',
        'tm',
        'corex',
        'kex',
        'db_mysql',
        'tls',
    ],
    'id': 1,
}

MOCK_JSONRPC_RESPONSE_STATS_ALL = {
    'jsonrpc': '2.0',
    'result': [
        'core:bad_URIs_rcvd = 0',
        'core:bad_msg_hdr = 0',
        'core:drop_replies = 0',
        'core:drop_requests = 0',
        'core:err_replies = 0',
        'core:err_requests = 0',
        'core:fwd_replies = 0',
        'core:fwd_requests = 0',
        'core:rcv_replies = 0',
        'core:rcv_replies_18x = 0',
        'core:rcv_replies_1xx = 0',
        'core:rcv_replies_1xx_bye = 0',
        'core:rcv_replies_1xx_cancel = 0',
        'core:rcv_replies_1xx_invite = 0',
        'core:rcv_replies_1xx_message = 0',
        'core:rcv_replies_1xx_prack = 0',
        'core:rcv_replies_1xx_refer = 0',
        'core:rcv_replies_1xx_reg = 0',
        'core:rcv_replies_1xx_update = 0',
        'core:rcv_replies_2xx = 0',
        'core:rcv_replies_2xx_bye = 0',
        'core:rcv_replies_2xx_cancel = 0',
        'core:rcv_replies_2xx_invite = 0',
        'core:rcv_replies_2xx_message = 0',
        'core:rcv_replies_2xx_prack = 0',
        'core:rcv_replies_2xx_refer = 0',
        'core:rcv_replies_2xx_reg = 0',
        'core:rcv_replies_2xx_update = 0',
        'core:rcv_replies_3xx = 0',
        'core:rcv_replies_3xx_bye = 0',
        'core:rcv_replies_3xx_cancel = 0',
        'core:rcv_replies_3xx_invite = 0',
        'core:rcv_replies_3xx_message = 0',
        'core:rcv_replies_3xx_prack = 0',
        'core:rcv_replies_3xx_refer = 0',
        'core:rcv_replies_3xx_reg = 0',
        'core:rcv_replies_3xx_update = 0',
        'core:rcv_replies_401 = 0',
        'core:rcv_replies_404 = 0',
        'core:rcv_replies_407 = 0',
        'core:rcv_replies_480 = 0',
        'core:rcv_replies_486 = 0',
        'core:rcv_replies_4xx = 0',
        'core:rcv_replies_4xx_bye = 0',
        'core:rcv_replies_4xx_cancel = 0',
        'core:rcv_replies_4xx_invite = 0',
        'core:rcv_replies_4xx_message = 0',
        'core:rcv_replies_4xx_prack = 0',
        'core:rcv_replies_4xx_refer = 0',
        'core:rcv_replies_4xx_reg = 0',
        'core:rcv_replies_4xx_update = 0',
        'core:rcv_replies_5xx = 0',
        'core:rcv_replies_5xx_bye = 0',
        'core:rcv_replies_5xx_cancel = 0',
        'core:rcv_replies_5xx_invite = 0',
        'core:rcv_replies_5xx_message = 0',
        'core:rcv_replies_5xx_prack = 0',
        'core:rcv_replies_5xx_refer = 0',
        'core:rcv_replies_5xx_reg = 0',
        'core:rcv_replies_5xx_update = 0',
        'core:rcv_replies_6xx = 0',
        'core:rcv_replies_6xx_bye = 0',
        'core:rcv_replies_6xx_cancel = 0',
        'core:rcv_replies_6xx_invite = 0',
        'core:rcv_replies_6xx_message = 0',
        'core:rcv_replies_6xx_prack = 0',
        'core:rcv_replies_6xx_refer = 0',
        'core:rcv_replies_6xx_reg = 0',
        'core:rcv_replies_6xx_update = 0',
        'core:rcv_requests = 11',
        'core:rcv_requests_ack = 0',
        'core:rcv_requests_bye = 0',
        'core:rcv_requests_cancel = 0',
        'core:rcv_requests_info = 0',
        'core:rcv_requests_invite = 1',
        'core:rcv_requests_message = 0',
        'core:rcv_requests_notify = 0',
        'core:rcv_requests_options = 6',
        'core:rcv_requests_prack = 0',
        'core:rcv_requests_publish = 0',
        'core:rcv_requests_refer = 0',
        'core:rcv_requests_register = 0',
        'core:rcv_requests_subscribe = 0',
        'core:rcv_requests_update = 0',
        'core:unsupported_methods = 0',
        'dialog:active_dialogs = 0',
        'dialog:early_dialogs = 0',
        'dialog:expired_dialogs = 0',
        'dialog:failed_dialogs = 0',
        'dialog:processed_dialogs = 0',
        'dns:failed_dns_request = 1',
        'dns:slow_dns_request = 0',
        'http_async_client:errors = 0',
        'http_async_client:replies = 0',
        'http_async_client:requests = 0',
        'http_async_client:timeouts = 0',
        'mysql:driver_errors = 0',
        'pike:blocked_ips = 0',
        'registrar:accepted_regs = 0',
        'registrar:default_expire = 3600',
        'registrar:default_expires_range = 0',
        'registrar:expires_range = 0',
        'registrar:max_contacts = 0',
        'registrar:max_expires = 0',
        'registrar:rejected_regs = 0',
        'shmem:fragments = 11',
        'shmem:free_size = 57165928',
        'shmem:max_used_size = 77147336',
        'shmem:real_used_size = 77051800',
        'shmem:total_size = 134217728',
        'shmem:used_size = 33343712',
        'sl:1xx_replies = 0',
        'sl:200_replies = 4',
        'sl:202_replies = 0',
        'sl:2xx_replies = 0',
        'sl:300_replies = 0',
        'sl:301_replies = 0',
        'sl:302_replies = 0',
        'sl:3xx_replies = 0',
        'sl:400_replies = 0',
        'sl:401_replies = 0',
        'sl:403_replies = 0',
        'sl:404_replies = 0',
        'sl:407_replies = 0',
        'sl:408_replies = 0',
        'sl:483_replies = 0',
        'sl:4xx_replies = 0',
        'sl:500_replies = 1',
        'sl:5xx_replies = 0',
        'sl:6xx_replies = 0',
        'sl:failures = 0',
        'sl:received_ACKs = 0',
        'sl:sent_err_replies = 0',
        'sl:sent_replies = 5',
        'sl:xxx_replies = 0',
        'tcp:con_reset = 0',
        'tcp:con_timeout = 0',
        'tcp:connect_failed = 0',
        'tcp:connect_success = 0',
        'tcp:current_opened_connections = 1',
        'tcp:current_write_queue_size = 0',
        'tcp:established = 5',
        'tcp:local_reject = 0',
        'tcp:passive_open = 5',
        'tcp:send_timeout = 0',
        'tcp:sendq_full = 0',
        'tmx:2xx_transactions = 0',
        'tmx:3xx_transactions = 0',
        'tmx:4xx_transactions = 0',
        'tmx:5xx_transactions = 0',
        'tmx:6xx_transactions = 0',
        'tmx:UAC_transactions = 0',
        'tmx:UAS_transactions = 0',
        'tmx:active_transactions = 0',
        'tmx:inuse_transactions = 0',
        'tmx:rpl_absorbed = 0',
        'tmx:rpl_generated = 0',
        'tmx:rpl_received = 0',
        'tmx:rpl_relayed = 0',
        'tmx:rpl_sent = 0',
        'uac:regactive = 0',
        'uac:regdisabled = 0',
        'uac:regtotal = 0',
        'usrloc:location_contacts = 0',
        'usrloc:location_expires = 0',
        'usrloc:location_users = 0',
        'usrloc:registered_users = 0',
        'websocket:ws_current_connections = 0',
        'websocket:ws_failed_connections = 0',
        'websocket:ws_failed_handshakes = 0',
        'websocket:ws_local_closed_connections = 0',
        'websocket:ws_max_concurrent_connections = 0',
        'websocket:ws_msrp_current_connections = 0',
        'websocket:ws_msrp_failed_connections = 0',
        'websocket:ws_msrp_local_closed_connections = 0',
        'websocket:ws_msrp_max_concurrent_connections = 0',
        'websocket:ws_msrp_received_frames = 0',
        'websocket:ws_msrp_remote_closed_connections = 0',
        'websocket:ws_msrp_successful_handshakes = 0',
        'websocket:ws_msrp_transmitted_frames = 0',
        'websocket:ws_received_frames = 0',
        'websocket:ws_remote_closed_connections = 0',
        'websocket:ws_sip_current_connections = 0',
        'websocket:ws_sip_failed_connections = 0',
        'websocket:ws_sip_local_closed_connections = 0',
        'websocket:ws_sip_max_concurrent_connections = 0',
        'websocket:ws_sip_received_frames = 0',
        'websocket:ws_sip_remote_closed_connections = 0',
        'websocket:ws_sip_successful_handshakes = 0',
        'websocket:ws_sip_transmitted_frames = 0',
        'websocket:ws_successful_handshakes = 0',
        'websocket:ws_transmitted_frames = 0',
    ],
    'id': 1,
}

MOCK_JSONRPC_RESPONSE_DISPATCHER_LIST = {
    'jsonrpc': '2.0',
    'result': {
        'NRSETS': 3,
        'RECORDS': [
            {
                'SET': {
                    'ID': 17,
                    'TARGETS': [
                        {
                            'DEST': {
                                'URI': 'sip:10.128.0.19:5080',
                                'FLAGS': 'IP',
                                'PRIORITY': 0,
                                'ATTRS': {
                                    'BODY': 'weight=',
                                    'DUID': None,
                                    'MAXLOAD': 0,
                                    'WEIGHT': 0,
                                    'RWEIGHT': 0,
                                    'SOCKET': None,
                                },
                                'LATENCY': {
                                    'AVG': 4999.99707,
                                    'STD': 0.413549,
                                    'EST': 4999.996582,
                                    'MAX': 5000,
                                    'TIMEOUT': 7956,
                                },
                            }
                        },
                        {
                            'DEST': {
                                'URI': 'sip:10.128.0.7:5080',
                                'FLAGS': 'AP',
                                'PRIORITY': 0,
                                'ATTRS': {
                                    'BODY': 'weight=',
                                    'DUID': None,
                                    'MAXLOAD': 0,
                                    'WEIGHT': 0,
                                    'RWEIGHT': 0,
                                    'SOCKET': None,
                                },
                                'LATENCY': {'AVG': 1.889734, 'STD': 0.498489, 'EST': 1.059474, 'MAX': 8, 'TIMEOUT': 0},
                            }
                        },
                        {
                            'DEST': {
                                'URI': 'sip:34.67.77.119:5080',
                                'FLAGS': 'IP',
                                'PRIORITY': 0,
                                'ATTRS': {
                                    'BODY': 'weight=',
                                    'DUID': None,
                                    'MAXLOAD': 0,
                                    'WEIGHT': 0,
                                    'RWEIGHT': 0,
                                    'SOCKET': None,
                                },
                                'LATENCY': {
                                    'AVG': 4999.796875,
                                    'STD': 0.456103,
                                    'EST': 4999.94873,
                                    'MAX': 5000,
                                    'TIMEOUT': 7956,
                                },
                            }
                        },
                        {
                            'DEST': {
                                'URI': 'sip:10.128.0.5:5080',
                                'FLAGS': 'IP',
                                'PRIORITY': 0,
                                'ATTRS': {
                                    'BODY': 'weight=',
                                    'DUID': None,
                                    'MAXLOAD': 0,
                                    'WEIGHT': 0,
                                    'RWEIGHT': 0,
                                    'SOCKET': None,
                                },
                                'LATENCY': {
                                    'AVG': 4999.796387,
                                    'STD': 0.478454,
                                    'EST': 4999.827637,
                                    'MAX': 5000,
                                    'TIMEOUT': 7956,
                                },
                            }
                        },
                        {
                            'DEST': {
                                'URI': 'sip:10.128.0.5:5060',
                                'FLAGS': 'IP',
                                'PRIORITY': 0,
                                'ATTRS': {
                                    'BODY': 'weight=',
                                    'DUID': None,
                                    'MAXLOAD': 0,
                                    'WEIGHT': 0,
                                    'RWEIGHT': 0,
                                    'SOCKET': None,
                                },
                                'LATENCY': {
                                    'AVG': 4999.796387,
                                    'STD': 0.484943,
                                    'EST': 4999.825195,
                                    'MAX': 5000,
                                    'TIMEOUT': 7956,
                                },
                            }
                        },
                    ],
                }
            },
            {
                'SET': {
                    'ID': 20,
                    'TARGETS': [
                        {
                            'DEST': {
                                'URI': 'sip:72.177.107.10:62104',
                                'FLAGS': 'IP',
                                'PRIORITY': 0,
                                'ATTRS': {
                                    'BODY': 'weight=',
                                    'DUID': None,
                                    'MAXLOAD': 0,
                                    'WEIGHT': 0,
                                    'RWEIGHT': 0,
                                    'SOCKET': None,
                                },
                                'LATENCY': {
                                    'AVG': 4999.796387,
                                    'STD': 0.486456,
                                    'EST': 4999.825195,
                                    'MAX': 5000,
                                    'TIMEOUT': 7956,
                                },
                            }
                        },
                        {
                            'DEST': {
                                'URI': 'sip:72.177.107.10:49412',
                                'FLAGS': 'IP',
                                'PRIORITY': 0,
                                'ATTRS': {
                                    'BODY': 'weight=',
                                    'DUID': None,
                                    'MAXLOAD': 0,
                                    'WEIGHT': 0,
                                    'RWEIGHT': 0,
                                    'SOCKET': None,
                                },
                                'LATENCY': {
                                    'AVG': 4999.796387,
                                    'STD': 0.487747,
                                    'EST': 4999.825195,
                                    'MAX': 5000,
                                    'TIMEOUT': 7956,
                                },
                            }
                        },
                        {
                            'DEST': {
                                'URI': 'sip:72.177.107.10:55633',
                                'FLAGS': 'IP',
                                'PRIORITY': 0,
                                'ATTRS': {
                                    'BODY': 'weight=',
                                    'DUID': None,
                                    'MAXLOAD': 0,
                                    'WEIGHT': 0,
                                    'RWEIGHT': 0,
                                    'SOCKET': None,
                                },
                                'LATENCY': {
                                    'AVG': 4999.796387,
                                    'STD': 0.489525,
                                    'EST': 4999.82373,
                                    'MAX': 5000,
                                    'TIMEOUT': 7956,
                                },
                            }
                        },
                    ],
                }
            },
            {
                'SET': {
                    'ID': 19,
                    'TARGETS': [
                        {
                            'DEST': {
                                'URI': 'sip:10.128.0.10:5060',
                                'FLAGS': 'AP',
                                'PRIORITY': 0,
                                'ATTRS': {
                                    'BODY': 'weight=',
                                    'DUID': None,
                                    'MAXLOAD': 0,
                                    'WEIGHT': 0,
                                    'RWEIGHT': 0,
                                    'SOCKET': None,
                                },
                                'LATENCY': {'AVG': 0.004903, 'STD': 0.084968, 'EST': 4.9e-05, 'MAX': 2, 'TIMEOUT': 0},
                            }
                        },
                        {
                            'DEST': {
                                'URI': 'sip:localhost:5060',
                                'FLAGS': 'AP',
                                'PRIORITY': 0,
                                'ATTRS': {
                                    'BODY': 'weight=',
                                    'DUID': None,
                                    'MAXLOAD': 0,
                                    'WEIGHT': 0,
                                    'RWEIGHT': 0,
                                    'SOCKET': None,
                                },
                                'LATENCY': {'AVG': 0.178059, 'STD': 0.286051, 'EST': 0.032152, 'MAX': 4, 'TIMEOUT': 0},
                            }
                        },
                    ],
                }
            },
        ],
    },
    'id': 1,
}

MOCK_JSONRPC_RESPONSE_TM_STATS = {
    'jsonrpc': '2.0',
    'result': {
        'current': 0,
        'waiting': 0,
        'total': 0,
        'total_local': 0,
        'rpl_received': 0,
        'rpl_generated': 0,
        'rpl_sent': 0,
        '6xx': 0,
        '5xx': 0,
        '4xx': 0,
        '3xx': 0,
        '2xx': 0,
        'created': 0,
        'freed': 0,
        'delayed_free': 0,
    },
    'id': 1,
}

MOCK_KAMCMD_RESPONSE_CORE_VERSION = b'kamailio 5.5.5 (x86_64/linux) \n'

MOCK_KAMCMD_RESPONSE_CORE_MODULES = (
    b'ndb_redis\nsiptrace\nwebsocket\ndispatcher\nkeepalive\ndrouting\npike\nrtpengine\nnathelper\ndomain'
    b'\nuac_redirect\nuac\npermissions\nauth_db\nauth\nsqlops\nrtimer\ndialog\nhtable\navpops\ncfgutils\nxmlops'
    b'\nhttp_async_client\njsonrpcs\njansson\njson\nxhttp\nacc\ncfg_rpc\nctl\nsanity\nxlog\nsiputils\ntextopsx'
    b'\ntextops\ndsiprouter\nregistrar\nusrloc\nmaxfwd\npv\npath\nrr\nsl\ntmx\ntm\ncorex\nkex\ndb_mysql\ntls\n '
)

MOCK_KAMCMD_RESPONSE_STATS_ALL = (
    b'core:bad_URIs_rcvd = 0\ncore:bad_msg_hdr = 0\ncore:drop_replies = 0\ncore:drop_requests = 91\ncore:err_replies = '
    b'0\ncore:err_requests = 0\ncore:fwd_replies = 0\ncore:fwd_requests = 0\ncore:rcv_replies = '
    b'0\ncore:rcv_replies_18x = 0\ncore:rcv_replies_1xx = 0\ncore:rcv_replies_1xx_bye = 0\ncore:rcv_replies_1xx_cancel '
    b'= 0\ncore:rcv_replies_1xx_invite = 0\ncore:rcv_replies_1xx_message = 0\ncore:rcv_replies_1xx_prack = '
    b'0\ncore:rcv_replies_1xx_refer = 0\ncore:rcv_replies_1xx_reg = 0\ncore:rcv_replies_1xx_update = '
    b'0\ncore:rcv_replies_2xx = 0\ncore:rcv_replies_2xx_bye = 0\ncore:rcv_replies_2xx_cancel = '
    b'0\ncore:rcv_replies_2xx_invite = 0\ncore:rcv_replies_2xx_message = 0\ncore:rcv_replies_2xx_prack = '
    b'0\ncore:rcv_replies_2xx_refer = 0\ncore:rcv_replies_2xx_reg = 0\ncore:rcv_replies_2xx_update = '
    b'0\ncore:rcv_replies_3xx = 0\ncore:rcv_replies_3xx_bye = 0\ncore:rcv_replies_3xx_cancel = '
    b'0\ncore:rcv_replies_3xx_invite = 0\ncore:rcv_replies_3xx_message = 0\ncore:rcv_replies_3xx_prack = '
    b'0\ncore:rcv_replies_3xx_refer = 0\ncore:rcv_replies_3xx_reg = 0\ncore:rcv_replies_3xx_update = '
    b'0\ncore:rcv_replies_401 = 0\ncore:rcv_replies_404 = 0\ncore:rcv_replies_407 = 0\ncore:rcv_replies_480 = '
    b'0\ncore:rcv_replies_486 = 0\ncore:rcv_replies_4xx = 0\ncore:rcv_replies_4xx_bye = 0\ncore:rcv_replies_4xx_cancel '
    b'= 0\ncore:rcv_replies_4xx_invite = 0\ncore:rcv_replies_4xx_message = 0\ncore:rcv_replies_4xx_prack = '
    b'0\ncore:rcv_replies_4xx_refer = 0\ncore:rcv_replies_4xx_reg = 0\ncore:rcv_replies_4xx_update = '
    b'0\ncore:rcv_replies_5xx = 0\ncore:rcv_replies_5xx_bye = 0\ncore:rcv_replies_5xx_cancel = '
    b'0\ncore:rcv_replies_5xx_invite = 0\ncore:rcv_replies_5xx_message = 0\ncore:rcv_replies_5xx_prack = '
    b'0\ncore:rcv_replies_5xx_refer = 0\ncore:rcv_replies_5xx_reg = 0\ncore:rcv_replies_5xx_update = '
    b'0\ncore:rcv_replies_6xx = 0\ncore:rcv_replies_6xx_bye = 0\ncore:rcv_replies_6xx_cancel = '
    b'0\ncore:rcv_replies_6xx_invite = 0\ncore:rcv_replies_6xx_message = 0\ncore:rcv_replies_6xx_prack = '
    b'0\ncore:rcv_replies_6xx_refer = 0\ncore:rcv_replies_6xx_reg = 0\ncore:rcv_replies_6xx_update = '
    b'0\ncore:rcv_requests = 239\ncore:rcv_requests_ack = 0\ncore:rcv_requests_bye = 0\ncore:rcv_requests_cancel = '
    b'0\ncore:rcv_requests_info = 0\ncore:rcv_requests_invite = 112\ncore:rcv_requests_message = '
    b'0\ncore:rcv_requests_notify = 0\ncore:rcv_requests_options = 118\ncore:rcv_requests_prack = '
    b'0\ncore:rcv_requests_publish = 0\ncore:rcv_requests_refer = 0\ncore:rcv_requests_register = '
    b'3\ncore:rcv_requests_subscribe = 0\ncore:rcv_requests_update = 0\ncore:unsupported_methods = '
    b'0\ndialog:active_dialogs = 0\ndialog:early_dialogs = 0\ndialog:expired_dialogs = 0\ndialog:failed_dialogs = '
    b'0\ndialog:processed_dialogs = 0\ndns:failed_dns_request = 1\ndns:slow_dns_request = 0\nhttp_async_client:errors '
    b'= 0\nhttp_async_client:replies = 0\nhttp_async_client:requests = 0\nhttp_async_client:timeouts = '
    b'0\nmysql:driver_errors = 0\npike:blocked_ips = 0\nregistrar:accepted_regs = 0\nregistrar:default_expire = '
    b'3600\nregistrar:default_expires_range = 0\nregistrar:expires_range = 0\nregistrar:max_contacts = '
    b'0\nregistrar:max_expires = 0\nregistrar:rejected_regs = 0\nshmem:fragments = 11\nshmem:free_size = '
    b'57191168\nshmem:max_used_size = 77165936\nshmem:real_used_size = 77026560\nshmem:total_size = '
    b'134217728\nshmem:used_size = 33318368\nsl:1xx_replies = 0\nsl:200_replies = 16\nsl:202_replies = '
    b'0\nsl:2xx_replies = 0\nsl:300_replies = 0\nsl:301_replies = 0\nsl:302_replies = 0\nsl:3xx_replies = '
    b'0\nsl:400_replies = 2\nsl:401_replies = 1\nsl:403_replies = 0\nsl:404_replies = 0\nsl:407_replies = '
    b'113\nsl:408_replies = 0\nsl:483_replies = 0\nsl:4xx_replies = 0\nsl:500_replies = 2\nsl:5xx_replies = '
    b'0\nsl:6xx_replies = 0\nsl:failures = 0\nsl:received_ACKs = 91\nsl:sent_err_replies = 0\nsl:sent_replies = '
    b'134\nsl:xxx_replies = 0\ntcp:con_reset = 3\ntcp:con_timeout = 0\ntcp:connect_failed = 0\ntcp:connect_success = '
    b'0\ntcp:current_opened_connections = 0\ntcp:current_write_queue_size = 0\ntcp:established = 9\ntcp:local_reject = '
    b'0\ntcp:passive_open = 9\ntcp:send_timeout = 0\ntcp:sendq_full = 0\ntmx:2xx_transactions = '
    b'0\ntmx:3xx_transactions = 0\ntmx:4xx_transactions = 0\ntmx:5xx_transactions = 0\ntmx:6xx_transactions = '
    b'0\ntmx:UAC_transactions = 0\ntmx:UAS_transactions = 0\ntmx:active_transactions = 0\ntmx:inuse_transactions = '
    b'0\ntmx:rpl_absorbed = 0\ntmx:rpl_generated = 0\ntmx:rpl_received = 0\ntmx:rpl_relayed = 0\ntmx:rpl_sent = '
    b'0\nuac:regactive = 0\nuac:regdisabled = 0\nuac:regtotal = 0\nusrloc:location_contacts = '
    b'0\nusrloc:location_expires = 0\nusrloc:location_users = 0\nusrloc:registered_users = '
    b'0\nwebsocket:ws_current_connections = 0\nwebsocket:ws_failed_connections = 0\nwebsocket:ws_failed_handshakes = '
    b'0\nwebsocket:ws_local_closed_connections = 0\nwebsocket:ws_max_concurrent_connections = '
    b'0\nwebsocket:ws_msrp_current_connections = 0\nwebsocket:ws_msrp_failed_connections = '
    b'0\nwebsocket:ws_msrp_local_closed_connections = 0\nwebsocket:ws_msrp_max_concurrent_connections = '
    b'0\nwebsocket:ws_msrp_received_frames = 0\nwebsocket:ws_msrp_remote_closed_connections = '
    b'0\nwebsocket:ws_msrp_successful_handshakes = 0\nwebsocket:ws_msrp_transmitted_frames = '
    b'0\nwebsocket:ws_received_frames = 0\nwebsocket:ws_remote_closed_connections = '
    b'0\nwebsocket:ws_sip_current_connections = 0\nwebsocket:ws_sip_failed_connections = '
    b'0\nwebsocket:ws_sip_local_closed_connections = 0\nwebsocket:ws_sip_max_concurrent_connections = '
    b'0\nwebsocket:ws_sip_received_frames = 0\nwebsocket:ws_sip_remote_closed_connections = '
    b'0\nwebsocket:ws_sip_successful_handshakes = 0\nwebsocket:ws_sip_transmitted_frames = '
    b'0\nwebsocket:ws_successful_handshakes = 0\nwebsocket:ws_transmitted_frames = 0\n '
)

MOCK_KAMCMD_RESPONSE_DISPATCHER_LIST = (
    b'{\n\tNRSETS: 3\n\tRECORDS: {\n\t\tSET: {\n\t\t\tID: 17\n\t\t\tTARGETS: {\n\t\t\t\tDEST: {\n\t\t\t\t\tURI: '
    b'sip:10.128.0.19:5080\n\t\t\t\t\tFLAGS: IP\n\t\t\t\t\tPRIORITY: 0\n\t\t\t\t\tATTRS: {\n\t\t\t\t\t\tBODY: '
    b'weight=\n\t\t\t\t\t\tDUID: <null string>\n\t\t\t\t\t\tMAXLOAD: 0\n\t\t\t\t\t\tWEIGHT: '
    b'0\n\t\t\t\t\t\tRWEIGHT: 0\n\t\t\t\t\t\tSOCKET: <null string>\n\t\t\t\t\t}\n\t\t\t\t\tLATENCY: {'
    b'\n\t\t\t\t\t\tAVG: 4999.997000\n\t\t\t\t\t\tSTD: 0.383000\n\t\t\t\t\t\tEST: 4999.996000\n\t\t\t\t\t\tMAX: '
    b'5002\n\t\t\t\t\t\tTIMEOUT: 10932\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t\tDEST: {\n\t\t\t\t\tURI: '
    b'sip:10.128.0.7:5080\n\t\t\t\t\tFLAGS: AP\n\t\t\t\t\tPRIORITY: 0\n\t\t\t\t\tATTRS: {\n\t\t\t\t\t\tBODY: '
    b'weight=\n\t\t\t\t\t\tDUID: <null string>\n\t\t\t\t\t\tMAXLOAD: 0\n\t\t\t\t\t\tWEIGHT: '
    b'0\n\t\t\t\t\t\tRWEIGHT: 0\n\t\t\t\t\t\tSOCKET: <null string>\n\t\t\t\t\t}\n\t\t\t\t\tLATENCY: {'
    b'\n\t\t\t\t\t\tAVG: 1.848000\n\t\t\t\t\t\tSTD: 0.532000\n\t\t\t\t\t\tEST: 1.453000\n\t\t\t\t\t\tMAX: '
    b'8\n\t\t\t\t\t\tTIMEOUT: 0\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t\tDEST: {\n\t\t\t\t\tURI: '
    b'sip:34.67.77.119:5080\n\t\t\t\t\tFLAGS: IP\n\t\t\t\t\tPRIORITY: 0\n\t\t\t\t\tATTRS: {\n\t\t\t\t\t\tBODY: '
    b'weight=\n\t\t\t\t\t\tDUID: <null string>\n\t\t\t\t\t\tMAXLOAD: 0\n\t\t\t\t\t\tWEIGHT: '
    b'0\n\t\t\t\t\t\tRWEIGHT: 0\n\t\t\t\t\t\tSOCKET: <null string>\n\t\t\t\t\t}\n\t\t\t\t\tLATENCY: {'
    b'\n\t\t\t\t\t\tAVG: 4999.796000\n\t\t\t\t\t\tSTD: 0.436000\n\t\t\t\t\t\tEST: 4999.826000\n\t\t\t\t\t\tMAX: '
    b'5001\n\t\t\t\t\t\tTIMEOUT: 10932\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t\tDEST: {\n\t\t\t\t\tURI: '
    b'sip:10.128.0.5:5080\n\t\t\t\t\tFLAGS: IP\n\t\t\t\t\tPRIORITY: 0\n\t\t\t\t\tATTRS: {\n\t\t\t\t\t\tBODY: '
    b'weight=\n\t\t\t\t\t\tDUID: <null string>\n\t\t\t\t\t\tMAXLOAD: 0\n\t\t\t\t\t\tWEIGHT: '
    b'0\n\t\t\t\t\t\tRWEIGHT: 0\n\t\t\t\t\t\tSOCKET: <null string>\n\t\t\t\t\t}\n\t\t\t\t\tLATENCY: {'
    b'\n\t\t\t\t\t\tAVG: 4999.796000\n\t\t\t\t\t\tSTD: 0.462000\n\t\t\t\t\t\tEST: 4999.826000\n\t\t\t\t\t\tMAX: '
    b'5001\n\t\t\t\t\t\tTIMEOUT: 10932\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t\tDEST: {\n\t\t\t\t\tURI: '
    b'sip:10.128.0.5:5060\n\t\t\t\t\tFLAGS: IP\n\t\t\t\t\tPRIORITY: 0\n\t\t\t\t\tATTRS: {\n\t\t\t\t\t\tBODY: '
    b'weight=\n\t\t\t\t\t\tDUID: <null string>\n\t\t\t\t\t\tMAXLOAD: 0\n\t\t\t\t\t\tWEIGHT: '
    b'0\n\t\t\t\t\t\tRWEIGHT: 0\n\t\t\t\t\t\tSOCKET: <null string>\n\t\t\t\t\t}\n\t\t\t\t\tLATENCY: {'
    b'\n\t\t\t\t\t\tAVG: 4999.796000\n\t\t\t\t\t\tSTD: 0.470000\n\t\t\t\t\t\tEST: 4999.826000\n\t\t\t\t\t\tMAX: '
    b'5001\n\t\t\t\t\t\tTIMEOUT: 10932\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n\t\t}\n\t\tSET: {\n\t\t\tID: '
    b'20\n\t\t\tTARGETS: {\n\t\t\t\tDEST: {\n\t\t\t\t\tURI: sip:72.177.107.10:62104\n\t\t\t\t\tFLAGS: '
    b'IP\n\t\t\t\t\tPRIORITY: 0\n\t\t\t\t\tATTRS: {\n\t\t\t\t\t\tBODY: weight=\n\t\t\t\t\t\tDUID: <null '
    b'string>\n\t\t\t\t\t\tMAXLOAD: 0\n\t\t\t\t\t\tWEIGHT: 0\n\t\t\t\t\t\tRWEIGHT: 0\n\t\t\t\t\t\tSOCKET: <null '
    b'string>\n\t\t\t\t\t}\n\t\t\t\t\tLATENCY: {\n\t\t\t\t\t\tAVG: 4999.796000\n\t\t\t\t\t\tSTD: '
    b'0.472000\n\t\t\t\t\t\tEST: 4999.825000\n\t\t\t\t\t\tMAX: 5001\n\t\t\t\t\t\tTIMEOUT: '
    b'10932\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t\tDEST: {\n\t\t\t\t\tURI: sip:72.177.107.10:49412\n\t\t\t\t\tFLAGS: '
    b'IP\n\t\t\t\t\tPRIORITY: 0\n\t\t\t\t\tATTRS: {\n\t\t\t\t\t\tBODY: weight=\n\t\t\t\t\t\tDUID: <null '
    b'string>\n\t\t\t\t\t\tMAXLOAD: 0\n\t\t\t\t\t\tWEIGHT: 0\n\t\t\t\t\t\tRWEIGHT: 0\n\t\t\t\t\t\tSOCKET: <null '
    b'string>\n\t\t\t\t\t}\n\t\t\t\t\tLATENCY: {\n\t\t\t\t\t\tAVG: 4999.796000\n\t\t\t\t\t\tSTD: '
    b'0.474000\n\t\t\t\t\t\tEST: 4999.825000\n\t\t\t\t\t\tMAX: 5001\n\t\t\t\t\t\tTIMEOUT: '
    b'10932\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t\tDEST: {\n\t\t\t\t\tURI: sip:72.177.107.10:55633\n\t\t\t\t\tFLAGS: '
    b'IP\n\t\t\t\t\tPRIORITY: 0\n\t\t\t\t\tATTRS: {\n\t\t\t\t\t\tBODY: weight=\n\t\t\t\t\t\tDUID: <null '
    b'string>\n\t\t\t\t\t\tMAXLOAD: 0\n\t\t\t\t\t\tWEIGHT: 0\n\t\t\t\t\t\tRWEIGHT: 0\n\t\t\t\t\t\tSOCKET: <null '
    b'string>\n\t\t\t\t\t}\n\t\t\t\t\tLATENCY: {\n\t\t\t\t\t\tAVG: 4999.796000\n\t\t\t\t\t\tSTD: '
    b'0.476000\n\t\t\t\t\t\tEST: 4999.825000\n\t\t\t\t\t\tMAX: 5001\n\t\t\t\t\t\tTIMEOUT: '
    b'10932\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n\t\t}\n\t\tSET: {\n\t\t\tID: 19\n\t\t\tTARGETS: {\n\t\t\t\tDEST: {'
    b'\n\t\t\t\t\tURI: sip:10.128.0.10:5060\n\t\t\t\t\tFLAGS: AP\n\t\t\t\t\tPRIORITY: 0\n\t\t\t\t\tATTRS: {'
    b'\n\t\t\t\t\t\tBODY: weight=\n\t\t\t\t\t\tDUID: <null string>\n\t\t\t\t\t\tMAXLOAD: 0\n\t\t\t\t\t\tWEIGHT: '
    b'0\n\t\t\t\t\t\tRWEIGHT: 0\n\t\t\t\t\t\tSOCKET: <null string>\n\t\t\t\t\t}\n\t\t\t\t\tLATENCY: {'
    b'\n\t\t\t\t\t\tAVG: 0.005000\n\t\t\t\t\t\tSTD: 0.087000\n\t\t\t\t\t\tEST: 0.000000\n\t\t\t\t\t\tMAX: '
    b'2\n\t\t\t\t\t\tTIMEOUT: 0\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t\tDEST: {\n\t\t\t\t\tURI: '
    b'sip:localhost:5060\n\t\t\t\t\tFLAGS: AP\n\t\t\t\t\tPRIORITY: 0\n\t\t\t\t\tATTRS: {\n\t\t\t\t\t\tBODY: '
    b'weight=\n\t\t\t\t\t\tDUID: <null string>\n\t\t\t\t\t\tMAXLOAD: 0\n\t\t\t\t\t\tWEIGHT: '
    b'0\n\t\t\t\t\t\tRWEIGHT: 0\n\t\t\t\t\t\tSOCKET: <null string>\n\t\t\t\t\t}\n\t\t\t\t\tLATENCY: {'
    b'\n\t\t\t\t\t\tAVG: 0.171000\n\t\t\t\t\t\tSTD: 0.305000\n\t\t\t\t\t\tEST: 0.017000\n\t\t\t\t\t\tMAX: '
    b'4\n\t\t\t\t\t\tTIMEOUT: 0\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n\t\t}\n\t}\n}\n '
)

MOCK_KAMCMD_RESPONSE_TM_STATS = (
    b'{\n\tcurrent: 0\n\twaiting: 0\n\ttotal: 0\n\ttotal_local: 0\n\trpl_received: 0\n\trpl_generated: 0\n\trpl_sent: '
    b'0\n\t6xx: 0\n\t5xx: 0\n\t4xx: 0\n\t3xx: 0\n\t2xx: 0\n\tcreated: 0\n\tfreed: 0\n\tdelayed_free: 0\n}\n '
)
