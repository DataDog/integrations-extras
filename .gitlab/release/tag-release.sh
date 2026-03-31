#!/bin/bash
# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euxo pipefail
IFS=$'\n\t'

echo "Obtaining GitHub token via dd-octo-sts"
set +x
GITHUB_TOKEN=$(dd-octo-sts token --scope DataDog/integrations-extras --policy self.gitlab.release.master)
trap 'set +x; dd-octo-sts revoke -t "$GITHUB_TOKEN" 2>/dev/null || true' EXIT
export GITHUB_TOKEN
git remote set-url origin "https://x-access-token:${GITHUB_TOKEN}@github.com/DataDog/integrations-extras.git"
set -x

git config --global user.email "$TAGGER_EMAIL"
git config --global user.name "$TAGGER_NAME"
git checkout master

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
