import logging
import numpy as np
from util import (ThreadedVideoCamera,
                  FrameBuffer,
                  get_diff)
import yaml

with open('config.yml') as config_file:
    config = yaml.load(config_file)


def frame_is_different(frame_buffer, frame):
    memory = frame_buffer.get_buffer()
    if len(memory) <= 2:
        return False
    threshold = config['pixel_fraction'] * memory[-1].shape[0] * memory[-1].shape[1]
    background = np.array([np.array(memory_image) for memory_image in memory]).mean(axis=0).astype(int)
    background_anomalous_count = (get_diff(frame, background) > 0.15).sum()
    captured_stream_change = (get_diff(memory[-2], frame) > 0).sum()
    print("background: {}. Threshold: {}.".format(background_anomalous_count, threshold))
    if background_anomalous_count > threshold and captured_stream_change > 0:
        print("anomalous. {} > {}".format(background_anomalous_count, threshold))
        return True
    else:
        return False


def check_and_record(frame_buffer, frame):
    if frame_is_different(frame_buffer, frame):
        if len(frame_buffer.recording) == 0:
            frame_buffer.record_buffer()
            frame_buffer.record(frame)
        else:
            frame_buffer.record(frame)
    elif not frame_is_different(frame_buffer, frame) and len(frame_buffer.recording) > 0:
        frame_buffer.save_recording()
        frame_buffer.clear_recording()
    else:
        pass


frame_buffer = FrameBuffer(callbacks=[check_and_record],
                           window=5.)

if __name__ == "__main__":
    camera = ThreadedVideoCamera(-1)
    print("initialized. monitoring...")
    for image in camera.arrays():
        frame_buffer.add_frame(image)
