import logging
import numpy as np
from util import (ThreadedVideoCamera,
                  FrameBuffer,
                  check_and_record)
import yaml


frame_buffer = FrameBuffer(callbacks=[check_and_record],
                           window=5.)

if __name__ == "__main__":
    camera = ThreadedVideoCamera(-1)
    print("initialized. monitoring...")
    for image in camera.arrays():
        frame_buffer.add_frame(image)
