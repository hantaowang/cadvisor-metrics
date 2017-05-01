FROM ubuntu:14.04
RUN \
  apt-get update && \
  apt-get install -y python3-pip && \
  rm -rf /var/lib/apt/lists/*

ADD requirements.txt /requirements.txt
ADD *.py /

RUN pip3 install -r requirements.txt

CMD python3 collector.py
