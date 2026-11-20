import os

HERE = os.path.dirname(os.path.abspath(__file__))

SCHEDULER_METRICS = [
    'volcano.action_scheduling_latency.bucket',
    'volcano.action_scheduling_latency.count',
    'volcano.action_scheduling_latency.sum',
    'volcano.e2e_job_scheduling_duration',
    'volcano.e2e_job_scheduling_latency.bucket',
    'volcano.e2e_job_scheduling_latency.count',
    'volcano.e2e_job_scheduling_latency.sum',
    'volcano.e2e_scheduling_latency.bucket',
    'volcano.e2e_scheduling_latency.count',
    'volcano.e2e_scheduling_latency.sum',
    'volcano.job.share',
    'volcano.open_session_duration.bucket',
    'volcano.open_session_duration.count',
    'volcano.open_session_duration.sum',
    'volcano.plugin_scheduling_latency.bucket',
    'volcano.plugin_scheduling_latency.count',
    'volcano.plugin_scheduling_latency.sum',
    'volcano.preemption.attempts.count',
    'volcano.preemption.victims',
    'volcano.queue.allocated.memory',
    'volcano.queue.allocated.milli_cpu',
    'volcano.queue.allocated.scalar_resources',
    'volcano.queue.deserved.memory',
    'volcano.queue.deserved.milli_cpu',
    'volcano.queue.deserved.scalar_resources',
    'volcano.queue.inqueue.memory',
    'volcano.queue.inqueue.milli_cpu',
    'volcano.queue.inqueue.scalar_resources',
    'volcano.queue.overused',
    'volcano.queue.request.memory',
    'volcano.queue.request.milli_cpu',
    'volcano.queue.request.scalar_resources',
    'volcano.queue.session_start_tasks',
    'volcano.queue.share',
    'volcano.scheduling_stage_duration.bucket',
    'volcano.scheduling_stage_duration.count',
    'volcano.scheduling_stage_duration.sum',
    'volcano.task_scheduling_latency.bucket',
    'volcano.task_scheduling_latency.count',
    'volcano.task_scheduling_latency.sum',
    'volcano.unschedulable.jobs',
    'volcano.unschedulable.tasks',
]

# Only reported when the scheduler runs the proportion plugin.
PROPORTION_METRICS = [
    'volcano.queue.weight',
]

# Only reported when the scheduler runs the capacity plugin.
CAPACITY_METRICS = [
    'volcano.queue.capacity.memory',
    'volcano.queue.capacity.milli_cpu',
    'volcano.queue.capacity.scalar_resources',
    'volcano.queue.real_capacity.memory',
    'volcano.queue.real_capacity.milli_cpu',
    'volcano.queue.real_capacity.scalar_resources',
]

CONTROLLER_METRICS = [
    'volcano.controller.job_to_pod_creation_latency.bucket',
    'volcano.controller.job_to_pod_creation_latency.count',
    'volcano.controller.job_to_pod_creation_latency.sum',
    'volcano.job.completed.count',
    'volcano.job.failed.count',
    'volcano.queue.pod_group.completed',
    'volcano.queue.pod_group.inqueue',
    'volcano.queue.pod_group.pending',
    'volcano.queue.pod_group.running',
    'volcano.queue.pod_group.unknown',
]

BAD_HOSTNAME_INSTANCE = {'openmetrics_endpoint': 'http://invalid-hostname:8080/metrics'}


def get_fixture_path(filename):
    return os.path.join(HERE, 'fixtures', filename)
