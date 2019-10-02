FROM maven:3.5.0-jdk-7


RUN curl -fsSL https://github.com/apache/storm/archive/v1.2.3.tar.gz -o storm.tar.gz \
    && tar -xf storm.tar.gz \
    && cd storm-*/examples/storm-starter \
    && mvn -Dmaven.test.skip=true package \
    && mv target/storm-starter-*.jar /topology.jar

ENTRYPOINT ["/bin/sleep"]
CMD ["120"]
