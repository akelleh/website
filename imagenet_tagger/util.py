import tensorflow as tf
from keras import backend as K
import numpy as np
from keras.applications import vgg16
from keras.preprocessing.image import img_to_array
from keras.applications.imagenet_utils import decode_predictions
import io
from PIL import Image


class ImagenetModel(object):
    def __init__(self, GPU=True, num_cores=8, initialize_model=True):
        if GPU:
            num_GPU = 1
            num_CPU = 1
        else:
            num_CPU = 1
            num_GPU = 0

        if initialize_model:
            config = tf.ConfigProto(intra_op_parallelism_threads=num_cores,
                                    inter_op_parallelism_threads=num_cores, allow_soft_placement=True,
                                    device_count={'CPU': num_CPU, 'GPU': num_GPU},
                                    gpu_options={'per_process_gpu_memory_fraction': 0.4, 'allow_growth': True})
            session = tf.Session(config=config)
            K.set_session(session)
            self.model = vgg16.VGG16(weights='imagenet')

    def predict(self, image):
        #numpy_image = img_to_array(image)
        image_batch = np.expand_dims(image, axis=0)
        processed_image = vgg16.preprocess_input(image_batch.copy())
        predictions = self.model.predict(processed_image)
        label = decode_predictions(predictions)
        return label

    def bytes_to_image(self, byte_string, shape=(500, 375), mode='RGB'):
        print(type(byte_string))
        image = Image.open(io.BytesIO(byte_string))#mode, shape, byte_string)
        return image


import cv2
from PIL import Image
import pickle
from threading import Thread
import time


class ThreadedVideoCamera(object):
    """
    Largely based on https://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/
    """
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.success, self.image = self.video.read()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        self.success, self.image = self.video.read()
        # if self.success:
        #    self.image = self.resize(image)

    def thread_stream(self):
        Thread(target=self.get_frames, args=()).start()
        return self

    def get_frames(self):
        start = time.time()
        count = 0
        try:
            while True:
                self.get_frame()
        except KeyboardInterrupt:
            pass

    def resize(self, image, shape=(224, 224)):
        old_size = image.size  # old_size[0] is in (width, height) format
        ratio = float(max(shape)) / max(old_size)
        new_size = tuple([int(x * ratio) for x in old_size])
        # use thumbnail() or resize() method to resize the input image
        # thumbnail is a in-place operation
        # im.thumbnail(new_size, Image.ANTIALIAS)
        im = image.resize(new_size, Image.ANTIALIAS)
        # create a new image and paste the resized on it
        new_im = Image.new("RGB", shape)
        new_im.paste(im, ((shape[0] - new_size[0]) // 2,
                          (shape[1] - new_size[1]) // 2))
        return new_im

    def show_image(self):
        img = Image.fromarray(self.video.read()[1])
        img.show()

    def messages(self, count=10000):
        self.thread_stream()
        while True:
            frame = self.resize(Image.fromarray(self.read()))
            frame = pickle.dumps(frame)
            yield frame

    def read(self):
        return self.image