#!/bin/bash
# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euxo pipefail
IFS=$'\n\t'

set +e
# Check if there are any new tag to push
ddev release tag all --dry-run
status=$?
set -e

# Only build packages if there were new releases
if [[ $status -eq 0 ]]; then
    # Order of steps matter as we want the tag to point to the signing commit.
    # 1. Sign
    # 2. Create tag(s)
    # 3. Trigger the build pipeline
    ./.gitlab/release/sign-release.sh
    ddev release tag all
    ./.gitlab/release/build-packages.sh
elif [[ $status -eq 2 ]]; then
    echo "No new releases, skipping the build pipeline trigger"
else
    exit $status
fi
