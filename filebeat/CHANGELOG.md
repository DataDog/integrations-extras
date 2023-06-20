# CHANGELOG - Filebeat Integration

1.3.0 
=====
* [FEATURE] Add support for Filebeat file registry post version 7.x

1.2.0 
=====
* [BUG] Send config instance tags along with checks

1.1.0 
=====
* [FEATURE] Add option to ignore the registry file check

1.0.0 
=====

0.3.0 / Unreleased
=====

### Add service check

* [FEATURE] Add [Service check](https://docs.datadoghq.com/developers/service_checks/agent_service_checks_submission/)

0.2.0 / Unreleased
=====

### Making the filebeat check compatible with versions > 5.x, and making it able to use the HTTP profiler

* [BUG] This patch makes the filebeat check compatible with the new syntax Filebeat started using in versions 5.x and later for its registry file. It still maintains backward compatibility with the syntax from previous versions.
* [FEATURE] Makes it possible to push to Datadog the metrics Filebeat exposes via its HTTP profiler, when started with the `--httpprof [HOST]:PORT` option (see https://www.elastic.co/guide/en/beats/filebeat/current/command-line-options.html)

0.1.0 / Unreleased
=====
### Initial version

* [FEATURE] Initial Filebeat integration, using Filebeat's registry files.
