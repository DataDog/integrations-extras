# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib

# 3rd party
import os
import ast

# project
from checks import AgentCheck


EVENT_TYPE = SOURCE_TYPE_NAME = 'filebeat'


class FilebeatCheck(AgentCheck):

    def __init__(self, name, init_config, agentConfig, instances=None):
        AgentCheck.__init__(self, name, init_config, agentConfig, instances)

    def check(self, instance):
        registry_file_path = instance.get('registry_file_path')
        if registry_file_path is None:
            raise Exception('An absolute path to a filebeat registry path must be specified')

        registry_contents = self._parse_registry_file(registry_file_path)

        for item in registry_contents:
            self.log.debug("found item: %s" % item)
            self._process_registry_item(item)

    def _parse_registry_file(self, registry_file_path):
        try:
            # check that the collector user has permissions to read the file
            if os.access(registry_file_path ,os.R_OK):
                with open(registry_file_path) as registry_file:
                    return ast.literal_eval(registry_file.read()) # convert the content from str to list
            else:
                # no permissions, alert and return empty dict
                self.log.error("Cannot open the registry log file - check the file permissions")
                return {}
        except Exception as e:
            self.log.error("General error while reading the registry file,"
                           " the error message is: %s" % e.message)
            return {}

    def _process_registry_item(self, item):
        source = item['source']
        offset = item['offset']

        try:
            stats = os.stat(source)

            if self._is_same_file(stats, item['FileStateOS']):
                unprocessed_bytes = stats.st_size - offset

                self.gauge('filebeat.registry.unprocessed_bytes', unprocessed_bytes,
                           tags=["source:{0}".format(source)])
            else:
                self.log.debug("Filebeat source %s appears to have changed" % (source, ))
        except OSError:
            self.log.debug("Unable to get stats on filebeat source %s" % (source, ))

    def _is_same_file(self, stats, file_state_os):
        return stats.st_dev == file_state_os['device'] and stats.st_ino == file_state_os['inode']

