docker build -t video_producer .
docker run \
--network="host" \
--restart unless-stopped \
--name video_producer \
--device /dev/video0:/dev/video0 \
-it video_producer 
