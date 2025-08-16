FROM python:3.9.2-alpine

ENV PYTHONUNBUFFERED=1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && apk add gdal-dev geos-dev proj-dev \
    && apk add gdal geos proj

RUN mkdir /project

WORKDIR /project

COPY requirements.txt /project/

RUN pip install -r requirements.txt

COPY . /project/
