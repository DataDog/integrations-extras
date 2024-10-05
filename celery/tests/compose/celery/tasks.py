#!/usr/bin/env python3
import os
import time

from celery import Celery

app = Celery('tasks', broker=os.environ.get("CELERY_BROKER"), backend=os.environ.get("CELERY_BACKEND"))


@app.task
def add(x, y):
    return x + y


@app.task
def slow_add(x, y, wait=10):
    time.sleep(wait)
    return x + y
