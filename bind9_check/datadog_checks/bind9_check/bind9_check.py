# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

from datadog_checks.checks import AgentCheck


class bind9_check(AgentCheck):

    def check(self, instance):
    	url = instance['URL']
    	if url is None :
    		raise Exception('The statistic channel URL must be specified in the configuration')
		    	

