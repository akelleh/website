docker build -t security_camera .
docker run \
--network="host" \
--restart unless-stopped \
--name security_camera \
--device /dev/video1:/dev/video1 \
-it security_camera
