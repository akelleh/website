import logging
from util import load_and_detect, download_from_s3 
import uuid
import confluent_kafka
import time
import json


def message_handler(message):
    message = json.loads(message.value())
    logging.info("message received.")
    s3_bucket = 'aws-website-adamkelleher-q9wlb'
    local_path = download_from_s3(s3_bucket, message['s3_path'])
    detections = load_and_detect(local_path)
    logging.info(detections)


if __name__ == "__main__":
    # set qr config
    topic = 'video_events'
    address = '192.168.1.11'
    zookeeper_port = 9092
    bootstrap_servers = '{}:{}'.format(address, zookeeper_port)
    max_messages = 1
    conf = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': uuid.uuid1(),
        'session.timeout.ms': 6000,
        'default.topic.config': {
            'auto.offset.reset': 'latest'
        }
    }

    logging.info(conf)

    # set up logging
    logging_level = logging.getLevelName('INFO')
    logging.getLogger().setLevel(logging_level)

    # build the consumer
    kafka = confluent_kafka.Consumer(**conf)
    kafka.subscribe([topic])

    # consume messages
    while True:
        messages = kafka.consume(num_messages=max_messages, timeout=1./100.)
        for message in messages:
            if message is None:
                continue
            if message.error():
                logging.error('Error {}'.format(message.error().code()))
            else:
                message_handler(message)






