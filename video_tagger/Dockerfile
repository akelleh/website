FROM tensorflow/tensorflow:latest-gpu-py3 

COPY . /app

RUN apt-get update
RUN apt-get install -y \
    libavformat-dev libavcodec-dev libavdevice-dev \
    libavutil-dev libswscale-dev libswresample-dev libavfilter-dev
RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt

CMD ["python", "/app/tagger.py"]
