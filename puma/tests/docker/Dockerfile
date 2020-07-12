FROM ruby
COPY ./Gemfile /Gemfile
COPY ./Gemfile.lock /Gemfile.lock
RUN bundle install
COPY ./config /config
COPY ./config.ru /config.ru
ENTRYPOINT ["puma"]
