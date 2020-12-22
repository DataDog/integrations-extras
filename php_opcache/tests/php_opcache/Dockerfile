FROM php:7.2-apache

RUN docker-php-ext-install opcache

COPY ./src /var/www/html/
COPY ./opcache.ini /usr/local/etc/php/conf.d/opcache.ini

