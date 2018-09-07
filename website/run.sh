docker build -t website .
docker run -p 8888:8888 --restart unless-stopped website
