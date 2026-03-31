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
