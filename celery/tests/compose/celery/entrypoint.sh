#!/bin/bash

shift

QUEUE="$(echo \"$*\" | grep -oP '(?<=-Q )\w+')"
if [[ -z "${TASK_SLOT}" || -z "${DOCKER_NODE_HOSTNAME}" ]]; then
  WORKER_NAME="${QUEUE}@%h"
else
  WORKER_NAME="${QUEUE}-${TASK_SLOT}@%h.${DOCKER_NODE_HOSTNAME}"
fi
exec celery -A tasks worker -l info -n "${WORKER_NAME}" "$@"
