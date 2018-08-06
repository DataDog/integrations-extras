# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

from datadog_checks.checks import AgentCheck


class bind9_check(AgentCheck):

    def check(self, instance):
    	dns_url = instance.get('url')
    	if dns_url is None :
    		raise Exception('The statistic channel URL must be specified in the configuration')
		
		self.service_check("Status", AgentCheck.OK,
                           message='Connection to %s was successful' % dns_url)

		xmlStats = self.getStatsFromUrl(dns_url)

	def getStatsFromUrl(self, dns_url) :

		try:
			xmlStats = urllib.urlopen(url)

		except (URLError, HTTPError) as e:
			self.service_check("status", message= "not connected due to " + e.reason)
			raise

		return xmlStats