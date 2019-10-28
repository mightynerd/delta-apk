FROM python:3.7

RUN mkdir /src/

RUN apt-get clean \
    && apt-get -y update

WORKDIR /src
ADD uwsgi.ini /src
ADD requirements.txt /src
RUN pip install -r requirements.txt
ADD src /src