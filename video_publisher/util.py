import cv2
from PIL import Image
import pickle
from threading import Thread


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.image = None
        self.success = None
        Thread(target=self.get_frame()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        self.success, self.image = self.video.read()
        if self.success:
            self.image = self.resize(image)

    def gen_frames(self):
        try:
            while True:
                yield self.image
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
        for i, frame in enumerate(self.gen_frames()):
            frame = self.resize(Image.fromarray(frame))
            frame = pickle.dumps(frame)
            if i >= count:
                return frame
            else:
                yield frame


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
