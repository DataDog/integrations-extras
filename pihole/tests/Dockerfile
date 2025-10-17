FROM python:3.7

COPY fake-hole.py /code/
COPY requirements.txt /code/
WORKDIR /code/
RUN pip install -r requirements.txt

CMD [ "python", "./fake-hole.py" ]