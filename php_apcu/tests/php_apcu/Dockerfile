FROM php:7.2-apache

COPY ./src /var/www/html/

RUN pecl install apcu \
  && docker-php-ext-enable apcu

