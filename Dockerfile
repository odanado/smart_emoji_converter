FROM python:3.6

RUN apt update && apt upgrade -y
RUN apt install -y fonts-mplus

RUN pip install requests pillow tqdm rtmbot numpy scipy

ADD _server.patch /root

RUN cd /usr/local/lib/python3.6/site-packages/slackclient && \
    patch -u < /root/_server.patch

WORKDIR /src
