#!/bin/bash
# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euxo pipefail
IFS=$'\n\t'

set +e
ddev release tag all
status=$?
set -e

# Only build packages if there were new releases
if [[ $status -eq 0 ]]; then
    ./.gitlab/release/build-packages.sh
    ./.gitlab/release/sign-release.sh
elif [[ $status -eq 2 ]]; then
    echo "No new releases, skipping the build pipeline trigger"
else
    exit $status
fi
