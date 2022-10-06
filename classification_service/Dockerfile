from python:3.7.8-buster
MAINTAINER kyoungwon

RUN apt-get update
RUN python -m pip install --upgrade pip
RUN pip install pika
RUN pip install numpy
COPY ./classification_labeling_service ./classification_labeling_service
COPY ./start.sh /data/start.sh 
VOLUME ["/DATA"]
WORKDIR /classification_labeling_service

#CMD /data/start.sh 192.168.0.116 5672 1 
#CMD /data/start.sh 192.168.0.120 5672 1 
#
