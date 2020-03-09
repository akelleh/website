import os
import sys
import yaml
from tornado.httpclient import AsyncHTTPClient
import tornado.gen
import logging
from PIL import Image
import io
import numpy as np

# clone project from https://github.com/matterport/Mask_RCNN
ROOT_DIR = os.path.abspath("./Mask_RCNN")
# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn import utils
import mrcnn.model as modellib
# import coco config
sys.path.append(os.path.join(ROOT_DIR, "samples/coco/"))  # To find local version
import coco


with open(os.path.join(os.path.dirname(__file__), 'config.yml')) as config_file:
    config = yaml.load(config_file)


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


class InferenceConfig(coco.CocoConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


def load_model():
    # Local path to trained weights file
    COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
    # Directory to save logs and trained model
    MODEL_DIR = os.path.join(ROOT_DIR, "logs")
    # Download COCO trained weights from Releases if needed
    if not os.path.exists(COCO_MODEL_PATH):
        utils.download_trained_weights(COCO_MODEL_PATH)
    config = InferenceConfig()
    model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)
    model.load_weights(COCO_MODEL_PATH, by_name=True)
    return model


model = load_model()


@tornado.gen.coroutine
def poll_cameras():
    client = AsyncHTTPClient()
    for camera in config['cameras'].values():
        image_bytes = yield client.fetch("http://{}:{}/frame".format(camera['camera_ip'],
                                                                     camera['camera_port']))
        image = Image.open(io.BytesIO(image_bytes.body))
        X = np.asarray(image)
        logging.info('got image from {}, {}'.format(camera['camera_name'], np.asarray(image).shape))
        results = model.detect([X])
        detections = [{"detection_type": class_names[class_id],
                       "probability": probability} for class_id, probability in zip(results[0]['class_ids'],
                                                                                    results[0]['scores'])]
        logging.info(detections)
