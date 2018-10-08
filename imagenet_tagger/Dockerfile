FROM tensorflow/tensorflow:latest-gpu-py3 

COPY . /app

RUN apt-get update
RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt

CMD ["python", "/app/imagenet.py"]
