docker build -t imagenet_tagger .
docker run \
--network="host" \
--runtime=nvidia \
--restart unless-stopped \
--name imagenet_tagger \
-it imagenet_tagger
