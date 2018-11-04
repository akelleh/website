FROM mohaseeb/raspberrypi3-python-opencv
#FROM python:3.6-slim

COPY . /app

RUN apt-get update
RUN apt-get install -y libsm6 libxext6 libxrender-dev python3-pip python-dev python3-dev
RUN wget https://github.com/edenhill/librdkafka/archive/v0.11.6.tar.gz
RUN gzip -d v0.11.6.tar.gz && tar -xvf v0.11.6.tar && cd librdkafka-0.11.6/ &&  ./configure --prefix=/usr && make -j && sudo make install
RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt

CMD ["python3", "/app/video_producer.py"]
