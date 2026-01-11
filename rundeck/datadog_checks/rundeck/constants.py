SYSTEM_INFO_TAG_MAP = {
    "executions_active": ["executions", "active"],
    "executions_execution_mode": ["executions", "executionMode"],
    "rundeck_version": ["rundeck", "version"],
    "rundeck_api_version": ["rundeck", "apiversion"],
    "rundeck_build": ["rundeck", "build"],
    "rundeck_node": ["rundeck", "node"],
    "rundeck_base": ["rundeck", "base"],
    "rundeck_server_uuid": ["rundeck", "serverUUID"],
    "os_arch": ["os", "arch"],
    "os_name": ["os", "name"],
    "os_version": ["os", "version"],
    "jvm_name": ["jvm", "name"],
    "jvm_vendor": ["jvm", "vendor"],
    "jvm_version": ["jvm", "version"],
}
SYSTEM_TAG_KEY_PREFIX = "system"

SYSTEM_METRICS_TAG_MAP = {
    "cpu.load_average.average": ["cpu", "loadAverage", "average"],
    "cpu.processors": ["cpu", "processors"],
    "memory.free": ["memory", "free"],
    "memory.max": ["memory", "max"],
    "memory.total": ["memory", "total"],
    "scheduler.running": ["scheduler", "running"],
    "scheduler.thread_pool_size": ["scheduler", "threadPoolSize"],
    "threads.active": ["threads", "active"],
}
SYSTEM_METRIC_NAME_PREFIX = "system.stats"

RUNNING_EXECUTIONS_TAG_MAP = {
    "id": ["id"],
    "status": ["status"],
    "project_name": ["project"],
    "type": ["executionType"],
    "user": ["user"],
    "job_id": ["job", "id"],
    "job_name": ["job", "name"],
    "job_group": ["job", "group"],
}
EXECUTION_TAG_KEY_PREFIX = "execution"
EXECUTIONS_RUNNING_METRIC_NAME_PREFIX = "project.executions.running"
EXECUTIONS_RUNNING_DURATION_METRIC_NAME_PREFIX = f"{EXECUTIONS_RUNNING_METRIC_NAME_PREFIX}.duration"

METRICS_METRICS_METRIC_NAME_PREFIX = "metrics.metrics"

DEFAULT_API_VERSION = 30
