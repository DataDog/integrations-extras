#!/bin/bash
# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euxo pipefail
IFS=$'\n\t'

export IN_TOTO_SIGNING_KEY_PATH=/tmp/key.pem

echo "Grabbing robot signing key and password"
set +x
aws ssm get-parameter --region us-east-1 --name ci.integrations-extras.signing_key --with-decryption --query "Parameter.Value" --out text > "$IN_TOTO_SIGNING_KEY_PATH"
export IN_TOTO_SIGNING_KEY_PASSWORD=$(aws ssm get-parameter --region us-east-1 --name ci.integrations-extras.signing_password --with-decryption --query "Parameter.Value" --out text)
set -x

ddev release make all --sign-only
git push origin ${CI_COMMIT_BRANCH:-master}
