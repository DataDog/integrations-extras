#!/bin/bash
# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euxo pipefail
IFS=$'\n\t'
CURRENT_COMMIT=$(git rev-parse HEAD)
curl --request POST --form "token=$CI_JOB_TOKEN" --form ref=master \
    --form variables[ORIG_CI_BUILD_REF]=$CURRENT_COMMIT \
    --form variables[ROOT_LAYOUT_TYPE]=extras \
    --form variables[REPO_NAME]=integrations-extras \
    https://gitlab.ddbuild.io/api/v4/projects/138/trigger/pipeline
