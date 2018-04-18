# (C) Datadog, Inc. 2010-2018
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib
from nose.plugins.attrib import attr

# 3p
import responses

# project
from tests.checks.common import AgentCheckTest


TEST_GEOCODE_RESPONSE = {
    "ip": "1.2.3.4",
    "country_code": "US",
    "country_name": "United States",
    "region_code": "NY",
    "region_name": "New York",
    "city": "New York",
    "zip_code": "10018",
    "time_zone": "EST",
    "latitude": 40.756102,
    "longitude": -73.9923769,
    "metro_code": 555
}


@attr(requires='dog_tracker')
class TestDogTracker(AgentCheckTest):
    """Basic Test for dog_tracker integration."""
    CHECK_NAME = 'dog_tracker'
    DOG_TRACKER_CHECK_CONFIG = {'instances': [
        {'url': 'http://localhost:8123/json', 'name': 'Dog McDoggerson'}
    ]}

    @attr('config')
    def test_load_from_config(self):
        """
        Test Dog Tracker Config Load
        """
        self.load_check(self.DOG_TRACKER_CHECK_CONFIG, {})
        self.check.update_from_config(self.DOG_TRACKER_CHECK_CONFIG['instances'][0])
        self.assertEqual('http://localhost:8123/json', self.check.geo_info_url)
        self.assertEqual('dog_mcdoggerson', self.check.dog_name)
        self.assertListEqual([], self.check.additional_tags)

    @attr('util')
    def test_get_or_default(self):
        """
        Test Dog Tracker Utility Function: get_or_default
        """
        self.load_check(self.DOG_TRACKER_CHECK_CONFIG, {})
        self.assertEqual('unknown', self.check.get_or_default({}, 'foo'))
        self.assertEqual('unknown', self.check.get_or_default({'foo': None}, 'foo'))
        self.assertEqual('bar_baz_1', self.check.get_or_default({'foo': 'Bar/Baz 1'}, 'foo'))

    @attr('check')
    @responses.activate
    def test_check(self):
        """
        Test Dog Tracker check.
        """
        self.load_check(self.DOG_TRACKER_CHECK_CONFIG, {})

        responses.add(
            responses.GET,
            'http://localhost:8123/json',
            json=TEST_GEOCODE_RESPONSE,
            status=200
        )

        # run your actual tests...
        self.run_check(self.DOG_TRACKER_CHECK_CONFIG['instances'][0])

        dog_name_tag = 'dog:dog_mcdoggerson'.format()

        count_tags = [
            dog_name_tag,
            'city:{}'.format('new_york'),
            'region_name:{}'.format('new_york'),
            'timezone:{}'.format('est'),
            'country:{}'.format('united_states'),
        ]

        lat_long_tags = [dog_name_tag]

        self.assertMetric('dog.tracker', 1, tags=count_tags, count=1)
        self.assertMetric('dog.tracker.latitude', 40.756102, tags=lat_long_tags, count=1)
        self.assertMetric('dog.tracker.longitude', -73.9923769, tags=lat_long_tags, count=1)

        # Raises when COVERAGE=true and coverage < 100%
        self.coverage_report()
