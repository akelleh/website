FROM python:3.6-slim

COPY . /app

RUN apt-get update
RUN apt-get install -y libsm6 libxext6 libxrender-dev libglib2.0-0 git build-essential libopencv-core-dev
RUN pip3 install --upgrade pip
RUN pip3 install cython numpy
RUN pip3 install -r /app/requirements_no_avc.txt
WORKDIR /app
CMD ["python3", "/app/tagger.py"]
