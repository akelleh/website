import logging
import confluent_kafka
from util import VideoCamera


def pub(message):
    kafka.produce(topic, value=message)
    karka.flush(timeout=1. / 120.)
    logging.info("message published.")


if __name__ == "__main__":
    # set producer config
    topic = 'Video'
    address = '192.168.1.134'  # 'localhost'
    zookeeper_port = 9092
    bootstrap_servers = '{}:{}'.format(address, zookeeper_port)
    max_messages = 1
    conf = {
        'bootstrap.servers': bootstrap_servers,
    }

    logging.info(conf)

    # set up logging
    logging_level = logging.getLevelName('INFO')
    logging.getLogger().setLevel(logging_level)

    # build the consumer
    kafka = confluent_kafka.Producer(**conf)

    # consume messages
    while True:
        for message in VideoCamera().messages():
            pub(message)




