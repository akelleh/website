FROM tensorflow/tensorflow:latest-gpu-py3 

COPY . /app

RUN apt-get update
RUN apt-get install -y apt-utils python-dev pkg-config
RUN apt-get install -y libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev libswscale-dev libswresample-dev libavfilter-dev
RUN apt-get install -y autoconf \
    automake \
    build-essential \
    cmake \
    libass-dev \
    libfreetype6-dev \
    libjpeg-dev \
    libtheora-dev \
    libtool \
    libvorbis-dev \
    libx264-dev \
    pkg-config \
    wget \
    yasm \
    zlib1g-dev
RUN wget http://ffmpeg.org/releases/ffmpeg-3.2.tar.bz2
RUN tar -xjf ffmpeg-3.2.tar.bz2
WORKDIR ffmpeg-3.2
RUN ./configure --disable-static --enable-shared --disable-doc
RUN make
RUN make install
RUN apt-get install -y ffmpeg libav-tools
RUN pip3 install --upgrade pip
RUN pip3 install ffmpeg Cython
RUN pip3 install -r /app/requirements.txt

CMD ["python3", "/app/tagger.py"]
#CMD ["python", "/app/while.py"]
