AWS_ACCESS_KEY_ID=$(aws --profile default configure get aws_access_key_id)
AWS_SECRET_ACCESS_KEY=$(aws --profile default configure get aws_secret_access_key)

docker build -t security_camera .
docker run \
-e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
-e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
--network="host" \
--restart unless-stopped \
--name security_camera \
--device /dev/video0:/dev/video0 \
--network="host" \
-p 8000:8000 \
-it security_camera
