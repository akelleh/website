FROM python:3.6-slim

COPY . /app

RUN apt-get update
RUN apt-get install -y build-essential gcc
RUN apt-get install -y libmysqlclient-dev 
RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt

CMD ["python", "/app/importer.py"]
