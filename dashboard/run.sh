docker build -t dashboard .
docker run -p 8889:8889 --restart unless-stopped --link website -it dashboard
