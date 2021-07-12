import os
from time import sleep

import pytest
import requests

from datadog_checks.dev import docker_run, get_docker_hostname, get_here

BOOTSTRAP = {
    'action': 'create_cluster',
    'cluster': {'name': 'demo.local'},
    'node': {'paths': {'persistent_path': '/var/opt/redislabs/persist', 'ephemeral_path': '/var/opt/redislabs/tmp'}},
    'credentials': {'username': 'demo@redislabs.com', 'password': '123456'},
}

DATABASE = {
    'name': 'db01',
    'memory_size': 100000000,
    'replication': False,
    'eviction_policy': 'volatile-lru',
    'sharding': False,
    'shards_count': 1,
    'port': 12000,
    'data_persistence': 'aof',
    'aof_policy': 'appendfsync-always',
}


@pytest.fixture(scope='session')
def dd_environment():
    compose_file = os.path.join(get_here(), 'docker-compose.yml')
    with docker_run(compose_file, log_patterns='MainThread: Done'):

        # Let the cluster settle first
        sleep(10)
        # Bootstrap the cluster
        url = 'https://{}:9443/v1/bootstrap/create_cluster'.format(get_docker_hostname())
        r = requests.post(url, json=BOOTSTRAP, verify=False)
        if r.status_code != 200:
            print("Error: Unable to bootstrap")
        counter = 0
        # Check to ensure it's running properly
        while True:
            counter += 1
            try:
                j = requests.get(
                    'https://{}:9443/v1/cluster'.format("localhost"),
                    auth=(BOOTSTRAP['credentials']['username'], BOOTSTRAP['credentials']['password']),
                    headers={'Content-Type': 'application/json'},
                    timeout=10,
                    verify=False,
                )
                if j.status_code == 200:
                    break
                else:
                    print("Retrying:", counter)
                    sleep(5)
            except Exception as e:
                print("Retrying:", counter, " Error:", str(e))
                sleep(5)
            if counter > 9:
                break
        # Create a database
        x = requests.post(
            'https://{}:9443/v1/bdbs'.format("localhost"),
            auth=(BOOTSTRAP['credentials']['username'], BOOTSTRAP['credentials']['password']),
            headers={'Content-Type': 'application/json'},
            timeout=10,
            verify=False,
            json=DATABASE,
        )
        if x.status_code != 200:
            print("Error: Unable to create database")
        print("OK: bootstrap complete")
        yield


@pytest.fixture
def instance():
    return {
        'host': get_docker_hostname(),
        'port': 9443,
        'username': BOOTSTRAP['credentials']['username'],
        'password': BOOTSTRAP['credentials']['password'],
    }
