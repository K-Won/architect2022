from python:3.7.8-buster
MAINTAINER kyoungwon

RUN apt-get update
RUN python -m pip install --upgrade pip
RUN pip install pika
RUN pip install numpy
COPY ./classification_labeling_service ./classification_labeling_service
VOLUME ["/DATA"]
WORKDIR /classification_labeling_service
CMD python3 main.py

