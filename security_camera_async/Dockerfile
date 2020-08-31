FROM python:3.7-slim

COPY . /app

RUN apt-get update
RUN apt-get install -y libgl1-mesa-glx libsm6 libxext6 libxrender-dev libglib2.0-0
RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt

CMD ["python", "/app/security_camera_async.py"]
