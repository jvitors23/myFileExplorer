FROM python:3.8.5-alpine
MAINTAINER JvitorS23

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./requirements-dev.txt /requirements-dev.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt
RUN pip install -r /requirements-dev.txt
RUN apk del .tmp-build-deps
RUN apk update && apk add bash

RUN mkdir /app
WORKDIR /app
COPY ./my_file_explorer /app

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
# For security (don't run app with root user)
RUN adduser -D user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
USER user