docker build -t video_producer_rpi .
docker run \
--network="host" \
--restart unless-stopped \
--name video_producer_rpi \
--device /dev/video0:/dev/video0 \
-it video_producer_rpi 
