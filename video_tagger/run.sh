docker build -t video_tagger .
docker run \
--runtime=nvidia \
--network="host" \
--restart unless-stopped \
--name video_tagger \
-it video_tagger
