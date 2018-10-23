# CHANGELOG - Filebeat Integration

0.2.0
=====

### Making the filebeat check compatible with versions > 5.x, and making it able to use the HTTP profiler

* [BUG] This patch makes the filebeat check compatible with the new syntax Filebeat started using in versions 5.x and later for its registry file. It still maintains backward compatibility with the syntax from previous versions.
* [FEATURE] Makes it possible to push to Datadog the metrics Filebeat exposes via its HTTP profiler, when started with the `--httpprof [HOST]:PORT` option (see https://www.elastic.co/guide/en/beats/filebeat/current/command-line-options.html)

0.1.0 
=====
### Initial version

* [FEATURE] Initial Filebeat integration, using Filebeat's registry files.
