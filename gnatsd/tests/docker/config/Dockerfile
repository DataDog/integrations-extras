FROM ruby:latest

COPY script.sh /opt/local/script.sh

RUN chmod 755 /opt/local/script.sh

RUN gem install nats

CMD ["/opt/local/script.sh"]
