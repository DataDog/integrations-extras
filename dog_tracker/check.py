# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib

# 3rd party
import requests

# project
from checks import AgentCheck

EVENT_TYPE = SOURCE_TYPE_NAME = 'dog_tracker'


class DogTrackerCheck(AgentCheck):

    DEFAULT_URL = 'https://freegeoip.net/json'
    DEFAULT_DOG_TAG = 'anonymous'

    def __init__(self, name, init_config, agentConfig, instances=None):
        AgentCheck.__init__(self, name, init_config, agentConfig, instances)

    def get_or_default(self, d, s, default='Unknown'):
        """ Get an item from a dict or Default to some value

        :param d: the dict
        :param s:
        :param default:
        :return:
        """
        result = d.get(s, default) or default
        return result.replace('/', '_').replace(' ', '_').lower()

    def update_from_config(self, instance):
        """ Update Configuration tunables from instance configuration.

        :param instance: Agent config instance.
        :return: None
        """

        self.geo_info_url = instance.get('url', self.init_config.get('url', DogTrackerCheck.DEFAULT_URL))
        self.dog_name = instance.get('name', DogTrackerCheck.DEFAULT_DOG_TAG).\
            replace('/', '_').replace(' ', '_').lower()
        self.additional_tags = []
        self.additional_tags.extend(instance.get('tags', []))

    def check(self, instance):
        # Setup
        self.update_from_config(instance)

        # Perform Geo-Lookup
        r = requests.get(self.geo_info_url)
        geo_info = r.json()

        dog_tag = 'dog:{}'.format(self.dog_name)
        tags = [
            dog_tag,
            'city:{}'.format(self.get_or_default(geo_info, 'city')),
            'region_name:{}'.format(self.get_or_default(geo_info, 'region_name')),
            'timezone:{}'.format(self.get_or_default(geo_info, 'time_zone')),
            'country:{}'.format(self.get_or_default(geo_info, 'country_name'))
        ] + self.additional_tags
        location_tags = [dog_tag] + self.additional_tags

        # Record Stats.
        self.count('dog.tracker', 1, tags=tags)
        self.gauge('dog.tracker.latitude', geo_info.get('latitude', 0.0), tags=location_tags)
        self.gauge('dog.tracker.longitude', geo_info.get('longitude', 0.0), tags=location_tags)
