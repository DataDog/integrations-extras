#!/bin/bash

# Usage
# setup.sh [kind|none]

# setting up colors
BLU='\033[0;104m'
YLW='\033[0;33m'
GRN='\033[0;32m'
RED='\033[0;31m'
NOC='\033[0m' # No Color

echo_info(){
    printf "\n${BLU}%s${NOC}\n" "$1"
}
echo_step(){
    printf "\n${BLU}>>>>>>> %s${NOC}\n" "$1"
}
echo_step_completed(){
    printf "${GRN} [✔] %s${NOC}\n" "$1"
}

SCRIPT_DIR=$( cd -- $( dirname -- "${BASH_SOURCE[0]}" ) &> /dev/null && pwd )
MODE="kind"

if [[ $# -gt 1 ]]; then
    echo "usage: $0 [kind|none]"
    exit
fi

if [[ $# -eq 1 ]]; then
    case "$1" in
	"kind")
	    MODE="kind"
	    ;;
	"none")
            MODE="none"
            ;;
	*)
            echo "usage: $0 [kind|none]"
            exit
    esac
fi

echo_info "Hatch Config"
KUBERNETES_PRESENT=$(hatch run pip3.9 list|grep kubernetes)
if [[ ${KUBERNETES_PRESENT} == "Checking dependencies" ]]; then
    hatch run pip3.9 install kubernetes
    hatch run pip3.9 install datadog_agent
fi
echo_step_completed "Hatch Config"

echo_info "Checking for DATADOG_API_KEY and DATADOG_APP_KEY"
hatch run export DATADOG_API_KEY=${DATADOG_API_KEY}
hatch run export DATADOG_APP_KEY=${DATADOG_APP_KEY}
hatch run export DATADOG_SECRET_NAME=${DATADOG_SECRET_NAME}
if [[ ${DATADOG_API_KEY} == "" ]]; then
    echo "export DATADOG_API_KEY in your environment"
    exit
fi
if [[ ${DATADOG_APP_KEY} == "" ]]; then
    echo "export DATADOG_APP_KEY in your environment"
    exit
fi
echo_step_completed "Found DATADOG_API_KEY and DATADOG_APP_KEY"

KUBECONFIG="/tmp/uxp.kubeconfig"
if [[ ${MODE} == "kind" ]]; then
    echo_info "Creating local kind test UXP cluster"
    kind create cluster --name uxp --kubeconfig ${KUBECONFIG}
fi
KUBECTL="kubectl --kubeconfig ${KUBECONFIG}"
HELM="helm --kubeconfig ${KUBECONFIG}"

echo_info "Installing UXP"
up uxp --kubeconfig ${KUBECONFIG} install --set metrics.enabled=true
echo_info "Waiting for UXP Pod readiness"
${KUBECTL} wait -n upbound-system pods --all --for condition=Ready --timeout=15m
echo_step_completed "Installed Universal Crossplane"

CRDS_NOT_READY=true
while [[ "$CRDS_NOT_READY" == "true" ]]; do
    sleep 5
    echo_step "Waiting for CRDs to be available"
    PROVIDERS=$(${KUBECTL} get crds|grep providers.pkg.crossplane.io)
    if [[ "$PROVIDERS" != "" ]]; then
	CRDS_NOT_READY=false
    fi
done
echo_step_completed "CRDs are available"

echo_info "Installing providers"
${KUBECTL} apply -f ${SCRIPT_DIR}/provider-helm.yaml
${KUBECTL} apply -f ${SCRIPT_DIR}/providers-aws.yaml
echo_info "Waiting for provider readiness ... this will take a moment"
${KUBECTL} wait provider.pkg --all --for condition=Healthy --timeout=15m
NUM_CRDS=$(${KUBECTL} get crds|wc -l)
echo_step_completed "Installed providers using ${NUM_CRDS} CRDs"

CRDS_NOT_READY=true
while [[ "$CRDS_NOT_READY" == "true" ]]; do
    sleep 5
    echo_step "Waiting for CRDs to be available"
    CRDS=$(${KUBECTL} get crds|grep upbound)
    if [[ "$CRDS" != "" ]]; then
	CRDS_NOT_READY=false
    fi
done

echo_info "Creating Monitoring Namespace"
${KUBECTL} create namespace monitoring
echo_step_completed "Created Monitoring Namespace"

echo_info "Installing Datadog Agent"

echo_step "Creating Datadog Secret"
${KUBECTL} create secret generic $DATADOG_SECRET_NAME \
    --namespace monitoring \
    --from-literal api-key=$DATADOG_API_KEY \
    --from-literal app-key=$DATADOG_APP_KEY
echo_step_completed "Created Datadog Secret ${DATADOG_SECRET_NAME}"

echo_step "Installing Datadog Agent Pod"
${HELM} install datadog-upbound \
    -f ${SCRIPT_DIR}/datadog-values.yaml \
    --namespace monitoring \
    --set datadog.site='datadoghq.com' \
    --set datadog.apiKeyExistingSecret=$DATADOG_SECRET_NAME \
    --set datadog.appKeyExistingSecret=$DATADOG_SECRET_NAME \
    datadog/datadog
echo_step_completed "Installed Datadog Agent Pod"

echo_info "Waiting for Datadog Pod readiness"
${KUBECTL} wait -n monitoring pods --all --for condition=Ready --timeout=15m
echo_step_completed "Installed Datadog Pods"

echo_info "Load upbound_uxp.py and auto_conf.yaml into Datadog Agent"
SRC_DIR=${SCRIPT_DIR}/../../datadog_checks/upbound_uxp
export DATADOG_POD=$(${KUBECTL} get pods -n monitoring|grep datadog-upbound|awk '{print $1}'|grep -v cluster)
if [[ ${DATADOG_POD} == "" ]]; then
    echo "Datadog Pod not found"
else
    ${KUBECTL} -n monitoring exec ${DATADOG_POD} -- mkdir -p /home/root/dd
    WHEEL_PATH=$(ls -1 ${SCRIPT_DIR}/../../dist/*whl|head -1)
    WHEEL_NAME=$(cd ${SCRIPT_DIR}/../../dist && ls *whl|head -1)
    ${KUBECTL} -n monitoring cp ${WHEEL_PATH} ${DATADOG_POD}:/home/root/dd
    ${KUBECTL} -n monitoring exec ${DATADOG_POD} -- agent integration install -r -w /home/root/dd/${WHEEL_NAME}
fi
sleep 5
echo_step_completed "Uploaded upbound_uxp.py and auto_conf.yaml"

echo_info "Creating Service Account, Cluster Role and Role Binding"
cat <<EOF | ${KUBECTL} apply -f -
apiVersion: v1
kind: ServiceAccount
metadata:
  name: datadog-upbound
  namespace: monitoring
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: apiserver-cluster-role
  namespace: monitoring
rules:
  - apiGroups:
      - ""
    resources:
      - pods
    verbs: ["get", "list" ]
  - nonResourceURLs: ["/metrics"]
    verbs: ["get"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: apiserver-cluster-role-binding
subjects:
- namespace: monitoring
  kind: ServiceAccount
  name: datadog-upbound
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: apiserver-cluster-role
EOF
echo_step_completed "Created Service Account, Cluster Role and Role Binding"

echo_info "Creating Datadog ddev test environment in the Datadog Agent Container"
echo_step_completed "Created Datadog ddev test environment in the Datadog Agent Container"

echo_info "Checking Datadog Agent Upbound UXP Check"
export DATADOG_POD=$(${KUBECTL} get pods -n monitoring|grep datadog-upbound|awk '{print $1}'|grep -v cluster)
if [[ ${DATADOG_POD} == "" ]]; then
    echo "Datadog Agent Pod not found"
else
    ${KUBECTL} -n monitoring exec ${DATADOG_POD} -- agent check upbound_uxp
fi
echo_step_completed "Checked Datadog Agent Upbound UXP Check"

exit 0
