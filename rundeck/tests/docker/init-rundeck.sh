#!/bin/sh

run_rundeck_job() {
	local jobid="$1"
	if curl -fsS \
		-H "X-Rundeck-Auth-Token: my-static-token-123" \
		-X POST \
		"http://rundeck:4440/api/30/job/${jobid}/run"; then
		echo "Job execution succeeded."
	else
		echo "Job execution failed."
		exit 1
	fi
}

echo "Waiting for Rundeck..."
until curl -s -f -H "X-Rundeck-Auth-Token: my-static-token-123" http://rundeck:4440/api/47/system/info; do
	sleep 5
done

echo "Creating Project..."
curl -X POST http://rundeck:4440/api/47/projects \
	-H "X-Rundeck-Auth-Token: my-static-token-123" \
	-H "Content-Type: application/json" \
	-d '{"name": "Test-Project", "config": {"project.description": "Auto-created"}}'
sleep 5

echo "Importing Job File..."
if
	curl -s -X POST "http://rundeck:4440/api/47/project/Test-Project/jobs/import?format=yaml" \
		-H "X-Rundeck-Auth-Token: my-static-token-123" \
		-F "xmlBatch=@/tmp/jobs.yaml" | grep -q "succeeded"
then
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
