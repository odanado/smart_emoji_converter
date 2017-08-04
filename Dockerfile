FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN apt update && apt upgrade -y
RUN apt install -y fonts-mplus

RUN pip install requests pillow tqdm rtmbot numpy scipy grequests

ADD _server.patch /root

RUN cd /usr/local/lib/python3.6/site-packages/slackclient && \
    patch -u < /root/_server.patch

ENV NB_USER user
ENV NB_UID 1001

RUN useradd -m -s /bin/bash -N -u $NB_UID $NB_USER && \
    mkdir -p /src && \
    chown $NB_USER /src

USER $NB_USER

WORKDIR /src
