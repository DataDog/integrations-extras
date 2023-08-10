FROM python:3

RUN pip install "celery[redis]"
COPY tasks.py /root
COPY entrypoint.sh /entrypoint.sh
RUN chmod 0755 /entrypoint.sh
WORKDIR /root

ENTRYPOINT ["/entrypoint.sh"]
