import os
import av
import sys
import random
import math
import numpy as np
import skimage.io
import boto3

from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize

from pycocotools import coco
from mrcnn.config import Config


ROOT_DIR = os.path.abspath("./")  # "/app/")
sys.path.append(ROOT_DIR)  # To find local version of the library
MODEL_DIR = os.path.join(ROOT_DIR, "logs")
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)


class CocoConfig(Config):
    """Configuration for training on MS COCO.
    Derives from the base Config class and overrides values specific
    to the COCO dataset.
    """
    NAME = "coco"
    IMAGES_PER_GPU = 2
    NUM_CLASSES = 81


class InferenceConfig(CocoConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    POST_NMS_ROIS_TRAINING = 1000
    POST_NMS_ROIS_INFERENCE = 500
    IMAGE_MIN_DIM = 400 #really much faster but bad results
    IMAGE_MAX_DIM = 512


config = InferenceConfig()
config.display()


model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)
model.load_weights(COCO_MODEL_PATH, by_name=True)


class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
               'bus', 'train', 'truck', 'boat', 'traffic light',
               'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
               'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
               'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
               'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
               'kite', 'baseball bat', 'baseball glove', 'skateboard',
               'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
               'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
               'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
               'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
               'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
               'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
               'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
               'teddy bear', 'hair drier', 'toothbrush']


def detect(image):
    results = model.detect([image], verbose=1)
    r = results[0]
    detections = [{class_names[class_id]: class_probability} for class_id, class_probability in zip(r['class_ids'], r['scores'])]
    return detections


def load_and_detect(video_path):
    video = av.open(video_path)
    detections = []
    for packet in video.demux():
        for frame in packet.decode():
            arr = frame.to_rgb().to_nd_array()
            detections += detect(arr)
    return detections

def download_from_s3(s3_bucket, s3_key):
    s3 = boto3.client('s3')
    local_path = './tmp/{}'.format(s3_key.split('/')[-1])
    s3.download_file(s3_bucket, s3_key, local_path)
    return local_path
