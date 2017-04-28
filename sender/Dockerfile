FROM ubuntu:14.04

RUN \
  apt-get update && \
  apt-get install -y rsyslog python-pip

ADD requirements.txt requirements.txt
ADD sender.py sender.py
ADD sender-setup.py sender-setup.py

RUN pip install -r requirements.txt

CMD python3 sender-setup.py
