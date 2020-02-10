import json
import os
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))


class APIMockClient:
    def containers(self):
        all_containers = {}
        with open(os.path.join(HERE, 'fixtures', 'all_containers.json'), 'r') as f:
            all_containers = json.load(f)

        return all_containers

    def stats(self, container_id):
        stats = {}
        with open(os.path.join(HERE, 'fixtures', 'stats.json'), 'r') as f:
            stats = json.load(f)
        return stats[container_id]

    def events(
        self,
        since=0,
        until=int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds()),
        filters=json.dumps({"type": ["container"]}),
    ):
        all_events = []
        with open(os.path.join(HERE, 'fixtures', 'events.json'), 'r') as f:
            all_events = json.load(f)

        return all_events
