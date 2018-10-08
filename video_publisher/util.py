import cv2
from PIL import Image


class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        return image

    def gen_frames(self):
        try:
            while True:
                yield self.get_frame()
        except KeyboardInterrupt:
            pass

    def show_image(self, array):
        img = Image.fromarray(camera.video.read()[1])
        img.show()
