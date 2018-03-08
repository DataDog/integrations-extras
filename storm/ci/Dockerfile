FROM maven:3.5.0-jdk-7

RUN curl -fsSL https://archive.apache.org/dist/storm/apache-storm-1.1.1/apache-storm-1.1.1.tar.gz -o storm.tar.gz \
    && tar -xf storm.tar.gz \
    && mv ./apache* storm \
    && cd storm/examples/storm-starter \
    && mvn package \
    && mv target/storm-starter-*.jar /topology.jar

ENTRYPOINT ["/bin/sleep"]
CMD ["120"]
