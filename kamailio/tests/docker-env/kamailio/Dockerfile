FROM alpine

# alpine doesn't require explicit locale-file generation
ENV LANG en_US.utf8

COPY ./configs/* /etc/kamailio/
COPY ./.tmp/scripts/* /opt/datadog-agent/scripts/
COPY ./.tmp/sudoers.d/* /etc/sudoers.d/
#COPY ./entrypoint.sh /entrypoint.sh

RUN set -eux -o pipefail; \
    \
    apk add --no-cache \
        kamailio \
        kamailio-db \
        kamailio-extras \
        kamailio-http_async \
        kamailio-json \
        kamailio-mysql \
        kamailio-sqlite \
        kamailio-tls \
        kamailio-utils \
        kamailio-websocket \
        openssl \
        shadow \
        sqlite \
        sudo; \
    \
    mkdir -p /run/kamailio; \
    OLD_UID=$(getent passwd kamailio | cut -s -d ':' -f 3); \
    OLD_GID=$(getent group kamailio | cut -s -d ':' -f 3); \
    usermod -u 1000 kamailio; \
    groupmod -g 1000 kamailio; \
    find / -user ${OLD_UID} -exec chown -h kamailio {} +; \
    find / -group ${OLD_GID} -exec chgrp -h kamailio {} +; \
    kamdbctl create; \
    sqlite3 /etc/kamailio/kamailio.db "insert into dispatcher values(NULL, '0', 'sip:127.0.0.1:5060', '0', '0', '', 'localhost-5060');"; \
    chown kamailio:kamailio /run/kamailio; \
    chown -R root:kamailio /etc/kamailio; \
    \
    mkdir -p /run/nginx; \
    addgroup -S -g 1001 nginx; \
    adduser -S -H -D -h /run/nginx -s /sbin/nologin -G nginx -u 1001 nginx; \
    chown nginx:nginx /run/nginx; \
    \
    mkdir -p /opt/datadog-agent/scripts; \
    addgroup -S -g 1002 dd-agent; \
    adduser -S -H -D -h /opt/datadog-agent -s /sbin/nologin -G dd-agent -u 1002 dd-agent; \
    chown -R dd-agent:dd-agent /opt/datadog-agent; \
    find /opt/datadog-agent/scripts/ -type f -exec chmod 500 {} +; \
    \
    chown -R root:root /etc/sudoers.d/; \
    \
    mkdir -p /etc/ssl/kamailio; \
    dd if=/dev/urandom of="${HOME}/.rnd" bs=1024 count=1 2>/dev/null; \
    openssl req -new -newkey rsa:2048 -x509 -sha256 -days 365 -nodes -out /etc/ssl/kamailio/cert.pem -keyout /etc/ssl/kamailio/key.pem -subj "/CN=kamailio.org"; \
    chown -R root:kamailio /etc/ssl/kamailio; \
    chmod 751 /etc/ssl/kamailio; \
    chmod 644 /etc/ssl/kamailio/cert.pem; \
    chmod 640 /etc/ssl/kamailio/key.pem;

VOLUME /run/kamailio
#VOLUME /etc/kamailio
#VOLUME /opt/datadog-agent/scripts
#VOLUME /etc/sudoers.d

STOPSIGNAL SIGTERM

EXPOSE 5060/udp
EXPOSE 5060/tcp
EXPOSE 5061/tcp

#ENTRYPOINT ["/entrypoint.sh"]
CMD ["/usr/sbin/kamailio", "-f", "/etc/kamailio/kamailio.cfg", "-DD", "-u", "kamailio", "-g", "kamailio", "-m", "256"]