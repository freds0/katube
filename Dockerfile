# docker build -t ubuntu1604py36
FROM ubuntu:18.04

RUN set -x \
      && apt-get update \
      && apt-get install -y espeak ffmpeg libespeak-dev libsndfile1 libsndfile1-dev python python-dev python-pip python-numpy python-lxml \
      && rm -rf /var/lib/apt/lists/*
RUN apt-get update
RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv sox
RUN apt-get install -y wget git nano

# update pip
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 10

RUN export PYTHONIOENCODING=UTF-8