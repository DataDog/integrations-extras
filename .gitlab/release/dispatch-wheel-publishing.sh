#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

SOURCE_REPO_REF=$(git rev-parse HEAD)
if [[ ! "$SOURCE_REPO_REF" =~ ^[0-9a-f]{40}$ ]]; then
    echo "Expected a full signed commit SHA, got: $SOURCE_REPO_REF" >&2
    exit 1
fi

payload=$(printf '{"ref":"master","inputs":{"source-repo-ref":"%s"}}' "$SOURCE_REPO_REF")

echo "Dispatching autonomous wheel publishing for integrations-extras@$SOURCE_REPO_REF"
set +x
DISPATCH_TOKEN=$(dd-octo-sts token \
    --scope DataDog/integrations-extras \
    --policy self.gitlab.release.dispatch-wheel-publishing)
trap 'set +x; dd-octo-sts revoke -t "$DISPATCH_TOKEN" 2>/dev/null || true' EXIT

curl --fail-with-body --silent --show-error \
    --retry 3 --retry-all-errors --retry-delay 2 --max-time 30 \
    --request POST \
    --header "Accept: application/vnd.github+json" \
    --header "Authorization: Bearer $DISPATCH_TOKEN" \
    --header "X-GitHub-Api-Version: 2022-11-28" \
    --data "$payload" \
    https://api.github.com/repos/DataDog/integrations-extras/actions/workflows/release-trigger.yml/dispatches
