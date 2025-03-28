FROM python:3.9-slim

WORKDIR /app
COPY openmimic.py .
COPY metrics.txt .
RUN pip install Flask

CMD ["python", "openmimic.py"]