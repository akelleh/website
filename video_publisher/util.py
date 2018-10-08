import cv2
from PIL import Image


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

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

    def show_image(self):
        img = Image.fromarray(self.video.read()[1])
        img.show()

    def messages(self, count=10):
        for _ in range(count):
            yield self.gen_frames()