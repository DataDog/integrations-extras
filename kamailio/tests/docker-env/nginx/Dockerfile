FROM nginx:alpine

# alpine doesn't require explicit locale-file generation
ENV LANG en_US.utf8

RUN set -eux -o pipefail; \
    \
    apk add --no-cache openssl shadow; \
    \
    mkdir -p /run/kamailio; \
    addgroup -S -g 1000 kamailio; \
    adduser -S -H -D -h /run/kamailio -s /sbin/nologin -G kamailio -u 1000 kamailio; \
    chown kamailio:kamailio /run/kamailio; \
    mkdir -p /run/nginx; \
    OLD_UID=$(getent passwd nginx | cut -s -d ':' -f 3); \
    OLD_GID=$(getent group nginx | cut -s -d ':' -f 3); \
    usermod -u 1001 nginx; \
    groupmod -g 1001 nginx; \
    find / -user ${OLD_UID} -exec chown -h nginx {} +; \
    find / -group ${OLD_GID} -exec chgrp -h nginx {} +; \
    chown nginx:nginx /run/nginx; \
    \
    apk add --no-cache openssl; \
    \
    mkdir -p /etc/ssl/nginx; \
    dd if=/dev/urandom of="${HOME}/.rnd" bs=1024 count=1 2>/dev/null; \
    openssl req -new -newkey rsa:2048 -x509 -sha256 -days 365 -nodes -out /etc/ssl/nginx/cert.pem -keyout /etc/ssl/nginx/key.pem -subj "/CN=nginx"; \
    chown nginx:root /etc/ssl/nginx; \
    chown nginx:root /etc/ssl/nginx/cert.pem; \
    chown nginx:root /etc/ssl/nginx/key.pem; \
    chmod 170 /etc/ssl/nginx; \
    chmod 464 /etc/ssl/nginx/cert.pem; \
    chmod 460 /etc/ssl/nginx/key.pem; \
    \
    mkdir -p /var/cache/nginx; \
    mkdir -p /var/log/nginx; \
    mkdir -p /run/nginx; \
    chown nginx:root /var/cache/nginx; \
    chown nginx:root /var/log/nginx; \
    chown nginx:nginx /run/nginx; \
    chmod 751 /var/cache/nginx;

COPY --chown=root:root ./configs/* /etc/nginx/
#VOLUME /etc/nginx
VOLUME /run/kamailio

STOPSIGNAL SIGTERM

EXPOSE 80/udp
EXPOSE 80/tcp
EXPOSE 443/tcp

CMD ["/usr/sbin/nginx", "-g", "daemon off; master_process on; user nginx kamailio;"]