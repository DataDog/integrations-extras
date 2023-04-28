import time

import pytest
from celery import Celery

from datadog_checks.celery import CeleryCheck
from .common import REDIS_DB, REDIS_HOST, REDIS_PORT, REDIS_BACKEND_DB

pytestmark = [pytest.mark.integration, pytest.mark.usefixtures("dd_environment")]


def test_celery_default(aggregator, dd_run_check, check, worker_instance):
    # # we need to do this magic, so celery can find the tasks
    # if CELERY_PACKAGE_PATH not in sys.path:
    #     sys.path.insert(0, CELERY_PACKAGE_PATH)
    # # we set the broker and backend in env so tasks.py can read it
    celery_broker = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    celery_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_BACKEND_DB}"
    # os.environ["CELERY_BROKER"] = celery_broker
    # os.environ["CELERY_BACKEND"] = celery_backend
    # # finally import
    # from tasks import add, slow_add

    expected_tags = ["app:tasks", f"worker:celery@worker"]

    celery_check = check(worker_instance)

    with Celery('tasks', broker=celery_broker, backend=celery_backend, set_as_current=False) as app:
        # run a normal task and wait for it to finish
        task = app.send_task('tasks.add', args=(1, 2))
        task.get()

        dd_run_check(celery_check)
        # assert service check
        aggregator.assert_service_check('celery.worker.ping', CeleryCheck.OK, count=1, tags=expected_tags)
        # assert task metrics
        aggregator.assert_metric('celery.worker.tasks.active', value=0, count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.tasks.scheduled', value=0, count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.tasks.reserved', value=0, count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.tasks.revoked', value=0, count=1, tags=expected_tags)
        # assert worker metrics
        aggregator.assert_metric('celery.worker.uptime', count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.prefetch_count', count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.task_count',
                                 value=1, count=1, tags=expected_tags + ["task:tasks.add"])
        aggregator.assert_metric('celery.worker.task_count',
                                 value=0, count=0, tags=expected_tags + ["task:tasks.slow_add"])
        # assert rusage metrics
        aggregator.assert_metric('celery.worker.rusage.utime', count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.rusage.stime', count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.rusage.maxrss', count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.rusage.ixrss', count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.rusage.idrss', count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.rusage.isrss', count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.rusage.minflt', count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.rusage.majflt', count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.rusage.nswap', count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.rusage.inblock', count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.rusage.oublock', count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.rusage.msgsnd', count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.rusage.msgrcv', count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.rusage.nsignals', count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.rusage.nvcsw', count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.rusage.nivcsw', count=1, tags=expected_tags)

        aggregator.reset()
        task.forget()

        # run a slow task and check if we see it as active
        task = app.send_task('tasks.slow_add', args=(1, 2), kwargs={'wait': 20})
        time.sleep(5)
        dd_run_check(celery_check)
        # assert task metrics
        aggregator.assert_metric('celery.worker.tasks.active', value=1, count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.tasks.scheduled', value=0, count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.tasks.reserved', value=0, count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.tasks.revoked', value=0, count=1, tags=expected_tags)

        task.get()  # wait for the slow task to finish and see if 'task_count' was updated
        aggregator.assert_metric('celery.worker.task_count',
                                 value=1, count=1, tags=expected_tags + ["task:tasks.add"])
        aggregator.assert_metric('celery.worker.task_count',
                                 value=1, count=1, tags=expected_tags + ["task:tasks.slow_add"])

        aggregator.reset()
        task.forget()

        # schedule a task and check if we see it as scheduled
        task = app.send_task('tasks.add', args=(1, 2), countdown=20)
        time.sleep(5)
        dd_run_check(celery_check)

        # assert task metrics
        aggregator.assert_metric('celery.worker.tasks.active', value=0, count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.tasks.scheduled', value=1, count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.tasks.reserved', value=0, count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.tasks.revoked', value=0, count=1, tags=expected_tags)

        # wait for the task and check that it got counted
        task.get()
        time.sleep(1)
        dd_run_check(celery_check)
        aggregator.assert_metric('celery.worker.task_count',
                                 value=2, count=1, tags=expected_tags + ["task:tasks.add"])
        aggregator.assert_metric('celery.worker.task_count',
                                 value=1, count=2, tags=expected_tags + ["task:tasks.slow_add"])

        aggregator.reset()
        task.forget()

        # schedule a task, revoke it and check if we see it as revoked
        task = app.send_task('tasks.add', args=(1, 2), countdown=20)
        time.sleep(5)
        task.revoke()
        time.sleep(15)
        dd_run_check(celery_check)

        # assert task metrics
        aggregator.assert_metric('celery.worker.tasks.active', value=0, count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.tasks.scheduled', value=0, count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.tasks.reserved', value=0, count=1, tags=expected_tags)
        aggregator.assert_metric('celery.worker.tasks.revoked', value=1, count=1, tags=expected_tags)

        # wait for the task and check that it did not get counted
        task.wait(propagate=False)
        time.sleep(1)
        dd_run_check(celery_check)
        aggregator.assert_metric('celery.worker.task_count',
                                 value=2, count=2, tags=expected_tags + ["task:tasks.add"])
        aggregator.assert_metric('celery.worker.task_count',
                                 value=1, count=2, tags=expected_tags + ["task:tasks.slow_add"])

        aggregator.reset()
        task.forget()
