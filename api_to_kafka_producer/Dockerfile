FROM python:3.6-slim

COPY . /app

RUN apt-get update
RUN apt-get install -y build-essential
RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt
WORKDIR /app
CMD ["python3", "/app/api_to_kafka_producer.py"]
