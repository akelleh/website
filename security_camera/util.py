import numpy as np
from collections import deque
import cv2
from PIL import Image
import pickle
from threading import Thread
import time
import os
import boto3
import yaml


with open('config.yml') as config_file:
    config = yaml.load(config_file)


def save_to_s3(filename, bucket='aws-website-adamkelleher-q9wlb'):
    s3 = boto3.client('s3')
    key = os.path.join('security_camera', config['host_name'], filename.split('/')[-1])
    print('uploading to s3')
    s3.upload_file(filename, Bucket=bucket, Key=key)


def get_diff(image, background, threshold=0.05):
    delta = np.abs((np.array(image) / 255.) - (np.array(background) / 255.))
    delta_zero = delta < threshold
    delta[delta_zero] = 0
    return delta


def write_video(name, capture, frame_rate=15, codec='DIVX'):
    height, width, layers = capture[-1].shape
    writer = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*codec), frame_rate, (width, height))
    for frame in capture:
        writer.write(frame)
    writer.release()


def initialize(camera):
    memory = deque()
    for image in camera.images():
        memory.append(image)
        break

    for image in camera.images():
        if len(memory) > 10:
            break
        else:
            if np.any(get_diff(image, memory[-1]) > 0):
                memory.append(image)
    capture = [memory[-1]]
    return memory, capture


class ThreadedVideoCamera(object):
    """
    Largely based on https://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/
    """
    def __init__(self, camera=0):
        self.video = cv2.VideoCapture(camera)
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

    def images(self, count=10000, resize=False):
        self.thread_stream()
        while True:
            try:
                if resize:
                    frame = self.resize(Image.fromarray(self.read()))
                else:
                    frame = Image.fromarray(self.read())
                yield frame
            except AttributeError:
                pass

    def arrays(self, count=10000):
        self.thread_stream()
        while True:
            frame = self.read()
            yield frame

    def read(self):
        return self.image


class FrameBuffer(object):
    def __init__(self, window=60., callbacks=[]):
        self.buffer = deque()
        self.window = window
        self.callbacks = callbacks
        self.recording = []

    def add_frame(self, frame):
        self.buffer.append((time.time(), frame))
        while len(self.buffer) > 2 and self.buffer[-1][0] - self.buffer[0][0] > self.window:
            self.buffer.popleft()
        self.execute_callbacks(frame)

    def get_buffer(self):
        return np.array([frame[1] for frame in self.buffer])

    def record_buffer(self):
        self.recording = [frame[1] for frame in self.buffer]

    def execute_callbacks(self, frame):
        for callback in self.callbacks:
            callback(self, frame)

    def record(self, frame):
        self.recording.append(np.array(frame))

    def clear_recording(self):
        self.recording = []

    def save_recording(self):
        print("saving recording")
        filename = '{}.avi'.format(time.time())
        write_video(filename, self.recording, frame_rate=30)
        save_to_s3(filename)
