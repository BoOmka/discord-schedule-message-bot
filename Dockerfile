FROM python:3.8.3-alpine3.12

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt