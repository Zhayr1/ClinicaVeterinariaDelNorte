FROM python:3.8.7

ENV APP=/usr/src/app

WORKDIR $APP

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN apt update

COPY ./app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . $APP