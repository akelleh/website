docker build -t security_camera .
docker run \
--network="host" \
--restart unless-stopped \
--name security_camera \
--device /dev/video0:/dev/video0 \
-it security_camera
