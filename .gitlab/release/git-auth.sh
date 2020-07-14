#!/bin/bash
# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euxo pipefail
IFS=$'\n\t'

echo "Grabbing GitHub deploy key"
set +x
aws ssm get-parameter --region us-east-1 --name ci.integrations-extras.github_deploy_key --with-decryption --query "Parameter.Value" --out text | ssh-add -
set -x

git remote set-url origin git@github.com:DataDog/integrations-extras.git
git config --global user.email "$TAGGER_EMAIL"
git config --global user.name "$TAGGER_NAME"
git checkout master
