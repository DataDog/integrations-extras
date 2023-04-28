FROM python:3

RUN pip install "celery[redis]"
COPY tasks.py /root
WORKDIR /root

CMD ["celery", "-A", "tasks", "worker", "--loglevel=INFO"]
