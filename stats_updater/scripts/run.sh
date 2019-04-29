docker build -t stats_updater .
docker run \
--network="host" \
--restart unless-stopped \
--name stats_updater \
-it stats_updater
