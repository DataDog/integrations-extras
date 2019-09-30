FROM maven:3.5.0-jdk-7


RUN git clone git://github.com/apache/storm.git \
    && cd storm/examples/storm-starter \
    && git checkout v1.2.3 \
    && mvn -Dmaven.test.skip=true package \
    && mv target/storm-starter-*.jar /topology.jar

ENTRYPOINT ["/bin/sleep"]
CMD ["120"]
