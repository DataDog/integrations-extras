FROM python:3.11-alpine3.16

WORKDIR /app

COPY metrics.txt requirements.txt app.py .

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 9797

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "9797"]