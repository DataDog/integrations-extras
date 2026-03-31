#!/bin/sh

run_rundeck_job() {
	local jobid="$1"
	if curl -fsS \
		-H "X-Rundeck-Auth-Token: my-static-token-123" \
		-H "Accept: application/json" \
		-X POST \
		"http://rundeck:4440/api/30/job/${jobid}/run"; then
		echo "Job execution succeeded."
	else
		echo "Job execution failed."
		exit 1
	fi
}

echo "Waiting for Rundeck..."
until curl -s -f -H "X-Rundeck-Auth-Token: my-static-token-123" -H "Accept: application/json" http://rundeck:4440/api/30/system/info; do
	echo "Rundeck not ready yet, retrying in 5s..."
	sleep 5
done

echo "Creating Project..."
curl -X POST http://rundeck:4440/api/30/projects \
	-H "X-Rundeck-Auth-Token: my-static-token-123" \
	-H "Accept: application/json" \
	-H "Content-Type: application/json" \
	-d '{"name": "Test-Project", "config": {"project.description": "Auto-created"}}'
sleep 5

echo "Importing Job File..."
response=$(curl -X POST "http://rundeck:4440/api/30/project/Test-Project/jobs/import?format=yaml" \
		-H "X-Rundeck-Auth-Token: my-static-token-123" \
		-H "Accept: application/json" \
		-H "Content-Type: application/yaml" \
		--data-binary @/tmp/jobs.yaml)
if echo "$response" | grep -q '"failed":\[\]'; then
	echo "Import succeeded."
else
	echo "Import failed."
	exit 1
fi
sleep 5

echo "Run the Jobs..."
run_rundeck_job "1fastjob-pass-1111-1111-111111111111"
run_rundeck_job "1fastjob-fail-1111-1111-111111111111"
run_rundeck_job "1slowjob-pass-fail-1111-111111111111"
sleep 5

echo "Completed Rundeck initialization"
