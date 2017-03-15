# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib

# 3rd party
import requests
import simplejson

# project
from checks import AgentCheck

EVENT_TYPE = SOURCE_TYPE_NAME = 'helloworld'


class HelloworldCheck(AgentCheck):


    def check(self, instance):
        url = instance['url']
	value = requests.get(url).json()['value']
	tags = ["url:{}".format(url)]
	self.gauge('helloworld.value', value, tags=tags)
