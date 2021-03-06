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
import confluent_kafka
import datetime
import json
import logging


with open(os.path.join(os.path.dirname(__file__), 'config.yml')) as config_file:
    config = yaml.load(config_file)


bootstrap_servers = '{}:{}'.format(config['kafka_host'], config['kafka_port'])
max_messages = 1
conf = {
        'bootstrap.servers': bootstrap_servers,
       }

kafka = confluent_kafka.Producer(**conf)


def get_and_add_frame(camera, frame_buffer):
    frame = camera.get_frame()
    frame_buffer.add_frame(frame)
    return frame

def array_to_image(X, filename='temp_image.png'):
    image = Image.fromarray(X, 'RGB')
    image.save(filename)

def pub_record_event(frame_buffer, frame):
    message = {"time": datetime.datetime.now().strftime('%Y-%m-%d'),
               "s3_path": os.path.join('security_camera', config['host_name'], frame_buffer.last_recording_name.split('/')[-1]),
               "host": config["host_name"],
               "service": "security_camera"}
    kafka.produce(config['kafka_topic'], value=json.dumps(message))
    kafka.flush(timeout=1./120.)
    print("message published.")

def frame_is_different(frame_buffer):
    current_time = time.time()
    with open("log.txt", "a+") as f:
        f.write(f'called at {current_time}\n')
        if len(frame_buffer.buffer_times) <= 2:
            return False
        f.write("\trunning the rest.\n")
        threshold = config['pixel_fraction'] * frame_buffer.buffer.array.shape[1:][0] * frame_buffer.buffer.array.shape[1:][1]
        background = frame_buffer.buffer[:int(len(frame_buffer.buffer.array) / 2)].mean(axis=0).astype(int)
        frame = frame_buffer.buffer[int(len(frame_buffer.buffer.array) / 2):].mean(axis=0).astype(int)
        background_anomalous_count = (get_diff(frame, background) > 0.15).sum()
        captured_stream_change = (get_diff(frame_buffer.buffer[-2], frame_buffer.buffer[-1]) > 0).sum()
        f.write("\tbackground: {}. Threshold: {}.\n".format(background_anomalous_count, threshold))
        if background_anomalous_count > threshold and captured_stream_change > 0:
            f.write("\tanomalous. {} > {}\n".format(background_anomalous_count, threshold))
            return True
        else:
            return False


def start_or_stop_recording(frame_buffer, frame):
    if not frame_buffer.is_recording:
        if frame_is_different(frame_buffer):
            frame_buffer.saw_motion()
            frame_buffer.start_recording()
    if frame_buffer.is_recording:
        if time.time() - frame_buffer.time_of_last_motion > config.get("motion_frame", 5):
            if not frame_is_different(frame_buffer):
                frame_buffer.stop_recording()
            else:
                frame_buffer.saw_motion()


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
    def __init__(self, camera=0, initialize_thread=False):
        self.video = cv2.VideoCapture(camera)
        self.success, self.image = self.video.read()
        self.last_frame_time = -1

    def __del__(self):
        self.video.release()

    def get_frame(self, should_resize=False):
        self.success = False
        while not self.success:
            frame_grabbed = self.video.grab()
            if frame_grabbed:
                time_s = self.video.get(cv2.CAP_PROP_POS_MSEC) / 1000
                if time_s > self.last_frame_time:
                    self.success = True
                    self.last_frame_time = time_s
                    _, self.image = self.video.retrieve()
                if should_resize:
                    self.image = self.resize(self.image)
            else:
                break
        return self.image

    def get_image(self):
        image_array = self.get_frame()
        logging.info(image_array.shape)
        image_array = image_array[:, :, [2,1,0]]
        return Image.fromarray(image_array, mode='RGB')

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
        im = image.resize(new_size, Image.ANTIALIAS)
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
    def __init__(self, shape, window=10., callbacks=[], verbose=False, max_buffer_frames=150):
        self.buffer = CircularBuffer(shape=shape, maxlen=max_buffer_frames)
        self.max_buffer_frames = max_buffer_frames
        self.buffer_times = deque(maxlen=max_buffer_frames)
        self.window = window
        self.callbacks = callbacks
        self.recording = None
        self.last_recording_name = None
        self.time_of_last_motion = -np.inf
        self.power_on = True
        self.is_recording = False
        self.is_saving = False
        self.verbose = verbose
        self.shape = shape

    def start_recording(self):
        filename = f'{time.time()}.avi'
        self.recording = Video(filename,
                               self.buffer,
                               self.buffer_times)
        self.is_recording = True

    def stop_recording(self):
        if not self.is_saving:  # make sure it wasn't called from another thread
            self.is_saving = True
            self.save_recording()
            self.clear_recording()
            self.is_recording = False
        self.is_saving = False

    def should_execute_callbacks(self):
        if self.power_on:
            return True
        else:
            return False

    def power(self, power_on):
        self.power_on = power_on
        if not power_on:
            self.clear_recording()
            self.buffer = CircularBuffer(shape=self.shape,
                                         maxlen=self.max_buffer_frames)
            self.buffer_times = deque(maxlen=self.max_buffer_frames)

    def add_frame(self, frame):
        self.buffer_times.append(time.time())
        self.buffer.append(np.uint8(np.array(frame, dtype=np.uint8)))
        if self.verbose:
            logging.info(f"Added frame to buffer. {len(self.buffer_times)} frames.")
        if self.is_recording:
            self.record(frame)

    def execute_callbacks(self, frame):
        for callback in self.callbacks:
            callback(self, frame)

    def record(self, frame):
        self.recording.write_frame(np.uint8(np.array(frame, dtype=np.uint8)))
        if self.verbose:
            logging.info(f"Added frame to recording. {self.recording.frame_count} frames.")

    def clear_recording(self):
        self.recording = None

    def save_recording(self):
        print("saving recording.")
        if self.recording:
            self.last_recording_name = self.recording.filename
            save_to_s3(self.recording.filename)
            os.remove(self.recording.filename)

    def saw_motion(self):
        self.time_of_last_motion = time.time()


class Video(object):
    def __init__(self, filename, buffer, buffer_times, codec='DIVX'):
        height, width, layers = buffer.array.shape[1:]
        logging.info(f"Video writing as {width}, {height}, {layers}")
        frame_rate = len(buffer_times)/(buffer_times[-1] - buffer_times[0])
        self.writer = cv2.VideoWriter(filename,
                                      cv2.VideoWriter_fourcc(*codec),
                                      frame_rate,
                                      (width, height))
        self.frame_count = 0
        for i in range(len(buffer.array)):
            frame = buffer[i]
            self.write_frame(frame)
        self.filename = filename

    def write_frame(self, frame):
        logging.info(f"Writing frame: {type(frame)}")
        logging.info(f"Writing frame: {frame.shape}")
        self.writer.write(np.uint8(frame))
        self.frame_count += 1

    def __del__(self):
        self.writer.release()


class CircularBuffer(object):
    def __init__(self, shape, maxlen=10):
        """
        A deque as a numpy array with elements of shape `shape`
        """
        self.array = np.zeros((maxlen, *shape))
        self.start = 0
        self.end = 0
        self.maxlen = maxlen
        self.full = False

    def reorder_index(self, start, end, step):
        start = self.start + start
        end = self.start + end
        indices = []
        for i in range(start, end, step):
            indices.append(i % self.maxlen)
        return indices

    def __getitem__(self, key):
        if isinstance(key, slice):
            start, end, step = key.indices(len(self.array))
            if not self.full:
                return self.array[start:end:step]
            else:
                return self.array[self.reorder_index(start - 1, end - 1, step)]
        elif isinstance(key, int):
            if not self.full:
                return self.array[(key + self.start) % self.maxlen]
            else:
                return self.array[(key + self.start - 1) % self.maxlen]
        else:
            raise Exception('Invalid argument type: {}'.format(type(key)))

    def append(self, x):
        self.array[self.end] = x
        self.end = (self.end + 1) % self.maxlen
        if self.end == 0:
            self.full = True
        if self.full:
            self.start = (self.end + 1) % self.maxlen
