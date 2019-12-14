docker build -t security_camera .
docker run \
--network="host" \
--restart unless-stopped \
--name security_camera \
--device /dev/video0:/dev/video0 \
-e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
-e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
-it security_camera
