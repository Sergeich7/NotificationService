FROM python:3.10-slim
LABEL maintainer="Vitaly Belashov pl3@yandex.ru"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update

RUN mkdir app
WORKDIR /app
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r requirements.txt
#COPY . /app/
#EXPOSE 8000


