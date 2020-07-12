FROM python:3.8.3-alpine3.12

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt
