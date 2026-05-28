FROM mockoon/cli:latest

# Embed the Huntress mock data for standalone use (docker build).
# The docker-compose.yml mounts the file directly for development,
# so rebuilds are not required when huntress_mockoon.json changes.
COPY huntress_mockoon.json /data/huntress_mockoon.json

EXPOSE 3002

ENTRYPOINT ["mockoon-cli", "start", "--data", "/data/huntress_mockoon.json", "--port", "3002", "--hostname", "0.0.0.0"]
