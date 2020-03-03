from datadog_checks.dev import get_docker_hostname, get_here

CHECK_NAME = 'jboss_wildfly'

HERE = get_here()
HOST = get_docker_hostname()
