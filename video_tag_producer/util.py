import os
import yaml
import tornado.gen
import logging
import torch
import torchvision.models as models
import numpy as np
import cv2 as cv
import confluent_kafka
import json
import datetime
import boto3


with open(os.path.join(os.path.dirname(__file__), 'config.yml')) as config_file:
    config = yaml.load(config_file)


class_names = np.array([
                        '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
                        'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
                        'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
                        'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
                        'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
                        'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
                        'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
                        'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
                        'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
                        'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
                        'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
                        'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
                        ])


def load_model():
    logging.info('Loading model.')
    model = models.detection.maskrcnn_resnet50_fpn(pretrained=True,
                                                   progress=True,
                                                   num_classes=91,
                                                   pretrained_backbone=True,
                                                   trainable_backbone_layers=3).eval()
    logging.info('Loaded.')
    return model


def preprocess_image(image):
    return torch.from_numpy(np.transpose(image/255., (2, 1, 0)).astype('float32'))


def get_image(camera_ip):
    camera = cv.VideoCapture(f"rtsp://admin:@{camera_ip}/")
    captured = False
    while not captured:
        captured, frame = camera.read()
    return frame


model = load_model()


@tornado.gen.coroutine
def poll_cameras():
    logging.info('Polling cameras.')
    images_to_tag = []
    locations = []
    for camera in config['cameras'].values():
        image = get_image(camera['camera_ip'])
        images_to_tag.append(preprocess_image(image))
        locations.append(camera['camera_name'])
        logging.info('got image from {}, {}'.format(camera['camera_name'], np.asarray(image).shape))
    logging.info('Tagging images.')
    results = model(images_to_tag)
    detections = []
    for location, result in zip(locations, results):
        detections += [{"detection_type": class_names[class_id],
                        "probability": float(probability)} for class_id, probability in zip(result['labels'],
                                                                                            result['scores'])]
    logging.info("raw detections:")
    logging.info(detections)
    if (result['scores'] > config['detection_probability_threshold']).any():
        logging.info(detections)
        message = {'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                   'detections': detections}
        pub(json.dumps(message))

        if should_alert(detections):
            logging.info("sending SMS.")
            send_sms(message, '18437371257')

def should_alert(detections):
    for detection in detections:
        if 'person' in detection and detection.get('person', 0.) > config['detection_probability_threshold']:
            return True
    return False


def pub(message):
    conf = {
        'bootstrap.servers': f"{config['kafka_server']['ip']}:{config['kafka_server']['port']}",
    }
    kafka = confluent_kafka.Producer(**conf)
    kafka.produce(config['kafka_topic'],
                  value=message)
    kafka.flush(timeout=1.)
    logging.info("message published.")

def send_sms(message, phone_number):
    sns = boto3.client('sns', region_name='us-east-1')
    response = sns.publish(
        PhoneNumber=phone_number,
        Message=message,
    )
    logging.info(f"SMS response: {response}")