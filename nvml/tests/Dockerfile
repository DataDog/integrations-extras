# Use an intermediate step to build the nvml datadog integration
# Setup taken from https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
#
# You will need to change this version to whichever datadog version you want to install
# For example:
#   docker build --build-arg=DD_AGENT_VERSION=7.18.0 .
ARG DD_AGENT_VERSION=latest
ARG PY_VERSION=3.8
ARG INTEGRATIONS_VERSION=master

FROM python:${PY_VERSION} AS wheel_builder
ARG INTEGRATIONS_VERSION
ARG DD_AGENT_VERSION
WORKDIR /wheels

RUN pip install "datadog-checks-dev[cli]==3.1.0"
RUN git clone https://github.com/datadog/integrations-extras.git && cd integrations-extras && git status && git reset --hard ${INTEGRATIONS_VERSION}

RUN ddev config set extras ./integrations-extras
RUN ddev -e release build nvml

FROM datadog/agent:${DD_AGENT_VERSION}

COPY --from=wheel_builder /wheels/integrations-extras/nvml/dist/ /dist
COPY --from=wheel_builder /wheels/integrations-extras/nvml/requirements.in /requirements.in

# Work around bug https://github.com/DataDog/datadog-agent/issues/4142
RUN ln -s /etc/datadog-agent/datadog-docker.yaml /etc/datadog-agent/datadog.yaml && \
	agent integration install -r -w /dist/*.whl && \
	rm /etc/datadog-agent/datadog.yaml

# The command 'agent integration install' does not capture dependencies.  This is strange
# to me.  Install those on their own
RUN /opt/datadog-agent/embedded/bin/pip3 install -r /requirements.in

# Why do you need these variables: See https://github.com/NVIDIA/nvidia-docker/wiki/Usage
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES all
ENV INTEGRATIONS_VERSION $INTEGRATIONS_VERSION
