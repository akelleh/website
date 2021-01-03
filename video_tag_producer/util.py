import os
import yaml
from tornado.httpclient import AsyncHTTPClient
import tornado.gen
import logging
from PIL import Image
import io
import torch
import torchvision.models as models
import numpy as np
import cv2 as cv


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
    model = models.detection.maskrcnn_resnet50_fpn(pretrained=True,
                                                   progress=True,
                                                   num_classes=91,
                                                   pretrained_backbone=True,
                                                   trainable_backbone_layers=3).eval()
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
    images_to_tag = []
    locations = []
    for camera in config['cameras'].values():
        image = get_image(camera['camera_ip'])
        images_to_tag.append(preprocess_image(image))
        locations.append(camera['camera_name'])
        logging.info('got image from {}, {}'.format(camera['camera_name'], np.asarray(image).shape))
    results = model(images_to_tag)
    detections = []
    for location, result in zip(locations, results):
        detections += [{"detection_type": class_names[class_id],
                        "probability": probability} for class_id, probability in zip(result['labels'],
                                                                                     result['scores'])]
    if (result['scores'] > 0.6).any():
        logging.info(detections)
