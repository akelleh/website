docker build -t api_to_kafka_producer .
docker run \
--restart unless-stopped \
--name api_to_kafka_producer \
-p 8002:8002 \
-it api_to_kafka_producer
