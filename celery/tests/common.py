import os

HERE = os.path.dirname(os.path.abspath(__file__))

DOCKER_COMPOSE_PATH = os.path.join(HERE, "compose", "docker-compose.yml")
CELERY_PACKAGE_PATH = os.path.join(HERE, "compose", "celery")
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_BACKEND_DB = 1
