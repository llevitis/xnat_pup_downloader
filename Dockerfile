FROM ubuntu:16.04

RUN apt-get update -qqq &&\
    apt-get install -y git python-dev python-pip &&\
    mkdir -p /opt/

COPY requirements.txt /opt/requirements.txt
RUN pip install -r /opt/requirements.txt

COPY xnat_PUP_downloader.py /opt/xnat_PUP_downloader.py

ENTRYPOINT [ "python", "/opt/xnat_PUP_downloader.py" ]