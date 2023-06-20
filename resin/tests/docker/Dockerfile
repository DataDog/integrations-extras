FROM adoptopenjdk/openjdk8:jdk8u232-b09-alpine-slim as builder

ENV RESIN_HOME /opt/resin
ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$JAVA_HOME/bin:$RESIN_HOME/bin

RUN apk add --update \
    curl \
    g++ \
    gcc \
    gnupg \
    linux-headers \
    libgcc \
    make \
    alpine-sdk \
    && rm -rf /var/cache/apk/*

RUN CHK_SUM=05461c51fa94ab1a304481d0d9cbab64f5772eb9119289db696b868e4adba57d && \
  curl -Lo /tmp/resin.tar.gz 'https://caucho.com/download/resin-4.0.62.tar.gz' && \
  sha256sum /tmp/resin.tar.gz && \
  echo "${CHK_SUM}  /tmp/resin.tar.gz" | sha256sum -c - && \
  mkdir -p /opt/resin && \
  tar -xzf /tmp/resin.tar.gz -C /opt/resin --strip-components=1 && \
  cd /opt/resin && \
  ./configure --prefix=`pwd`; make; make install && \
  mkdir -p /opt/resin/watchdog-data && \
  mkdir -p /opt/resin/log && \
  mkdir -p /opt/resin/resin-data && \
  rm -rf /tmp/resin.tar.gz

FROM adoptopenjdk/openjdk8:jdk8u232-b09-alpine-slim

EXPOSE 8080
EXPOSE 7199

ENV RESIN_HOME /opt/resin
ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$JAVA_HOME/bin:$RESIN_HOME/bin

COPY --from=builder /opt/resin /opt/resin
COPY resin.jmx.xml /opt/resin/conf/resin.xml

ENTRYPOINT ["resinctl", "start-with-foreground"]
