# FROM python:3.9-alpine
FROM ubuntu:20.04

ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0
ENV C_FORCE_ROOT true

COPY . /queue
WORKDIR /queue

RUN apt-get update && apt-get install -y gcc g++ make libseccomp-dev python3 python3-pip && \
    cd judger && \
    make && \
    cd ..

RUN echo "deb http://th.archive.ubuntu.com/ubuntu jammy main" >> /etc/apt/sources.list
RUN  apt update && \
     apt install -y libc6

RUN pip3 install -U setuptools pip
RUN pip3 install -r requirements.txt

CMD celery -A tasks worker -l info -E