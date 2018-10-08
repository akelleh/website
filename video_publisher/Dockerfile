FROM tensorflow/tensorflow:latest-gpu-py3 

COPY . /app

RUN apt-get update
RUN apt-get install -y libsm6 libxext6 libxrender-dev
RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt

CMD ["python", "/app/video_producer.py"]
