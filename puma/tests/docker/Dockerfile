FROM ruby:3.1-bookworm
COPY ./Gemfile /Gemfile
COPY ./Gemfile.lock /Gemfile.lock
RUN bundle install
COPY ./config /config
COPY ./config.ru /config.ru
ENTRYPOINT ["puma"]
