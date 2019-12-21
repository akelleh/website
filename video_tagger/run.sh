docker build -t video_tagger .
docker run \
--network="host" \
--runtime=nvidia \
--restart unless-stopped \
--name video_tagger \
-it video_tagger
