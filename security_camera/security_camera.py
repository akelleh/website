import logging
import numpy as np
from util import ThreadedVideoCamera, initialize, get_diff, write_video, put_video
import time
import sys


if __name__ == "__main__":

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(handler)

    camera = ThreadedVideoCamera(-1)
    logging.info("camera started")
    memory, capture = initialize(camera)
    threshold = 0.1 * memory[-1].size[0] * memory[-1].size[1]
    time_of_last_capture = time.time()
    for image in camera.images():
        background = np.array([np.array(memory_image) for memory_image in memory]).mean(axis=0).astype(int)
        background_anomalous_count = (get_diff(image, background) > 0.05).sum()
        captured_stream_change = (get_diff(capture[-1], image) > 0).sum()
        if background_anomalous_count > threshold and captured_stream_change > 0:
            logging.info("adding image: {} > {}".format(background_anomalous_count, threshold))
            capture.append(image)
            time_of_last_capture = time.time()
        else:
            if len(capture) > 50 and time.time() - time_of_last_capture > 5:
                logging.info('writing out video.')
                local_file_path = '{}.avi'.format(time.time())
                write_video(local_file_path, capture, frame_rate=30)
                put_video(local_file_path)
                capture = [image]
            memory.append(image)
            memory.popleft()


"""
import confluent_kafka

def pub(message):
    kafka.produce(topic, value=message)
    kafka.flush(timeout=1./120.)
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
    start = time.time(); count = 0.
    for message in ThreadedVideoCamera().messages():
        count += 1
        pub(message)
        logging.info("Publishing at {} fps.".format(count / (time.time() - start)))
"""
