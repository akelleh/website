import logging
from util import ImagenetModel
import uuid
import confluent_kafka
import pickle
import time


model = ImagenetModel()


def message_handler(message):
    message = pickle.loads(message.value())
    logging.info("message received.")
    logging.info(model.predict(message))


if __name__ == "__main__":
    # set qr config
    topic = 'Video'
    address = '192.168.1.134'  # 'localhost'
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
    start = time.time(); count = 0
    while True:
        messages = kafka.consume(num_messages=max_messages, timeout=1./100.)  # 3. / 60.)
        for message in messages:
            if message is None:
                continue
            if message.error():
                logging.error('Error {}'.format(message.error().code()))
            else:
                count += 1
                logging.info("running at {} fps.".format(float(count) / (time.time() - start)))
                if count > 1000:
                    start = time.time(); count = 0
                message_handler(message)






