docker build -t video_tagger_consumer .
docker run \
--runtime=nvidia \
--network="host" \
--restart unless-stopped \
--name video_tagger_consumer \
-it video_tagger_consumer
