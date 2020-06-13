import logging
import numpy as np
import cv2
from util import (ThreadedVideoCamera,
                  FrameBuffer,
                  start_or_stop_recording,
                  pub_record_event,
                  array_to_image)
import yaml
import tornado.ioloop
import tornado.web
from concurrent.futures import ThreadPoolExecutor
import logging
import os
from io import BytesIO


with open(os.path.join(os.path.dirname(__file__), 'config.yml')) as config_file:
    config = yaml.load(config_file)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("html/index.html")


class PowerHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        power_on = bool(int(self.get_argument('on', True)))
        self.application.frame_buffer.power(power_on)
        self.write("Recording turned on: {}.".format(self.application.frame_buffer.should_execute_callbacks))


class FrameHandler(tornado.web.RequestHandler):
    def get(self):
        frame = self.application.camera.get_image()
        logging.info(frame)
        file_object = BytesIO()
        frame.save(file_object, format="png")
        image = file_object.getvalue()
        self.write(image)
        file_object.close()
        self.set_header("Content-type", "image/png")


class StatusHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        if self.application.frame_buffer.should_execute_callbacks:
            self.write("On")
        else:
            self.write("Off")


class Application(tornado.web.Application):
    def __init__(self):
        app_settings = {
            'default_handler_args': dict(status_code=404),
            "static_path": os.path.join(os.path.dirname(__file__), "html")
        }

        app_handlers = [
            (r'^/$', MainHandler),
            (r'^/power$', PowerHandler),
            (r'/html/(.*)', tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), "html")}),
            (r'^/status', StatusHandler),
            (r'^/frame', FrameHandler),
        ]
    
        self.frame_buffer = FrameBuffer(callbacks=[start_or_stop_recording,],
                                        window=5.)
        camera = config.get('camera_address', -1)
        self.camera = ThreadedVideoCamera(camera, initialize_thread=True)
        thread_count = config.get('pool_threads', 2)
        self.pool = ThreadPoolExecutor(thread_count)

        super(Application, self).__init__(app_handlers, **app_settings)

    def next_frame(self):
        image = self.camera.get_frame()
        if config.get('show_video', False):
            cv2.imshow('VIDEO', image)
            cv2.waitKey(1)
        self.frame_buffer.add_frame(image)

    def create_empty_file(self):
        with open("test.txt", "w+") as f:
            f.write('test')

    async def check_and_execute_callbacks(self):
        if self.frame_buffer.should_execute_callbacks():
            frame = self.frame_buffer.buffer[-1][1]
            await tornado.ioloop.IOLoop.current().run_in_executor(self.pool, self.frame_buffer.execute_callbacks, frame)


if __name__ == "__main__":
    port = 8000
    logging_level = logging.getLevelName('INFO')
    logging.getLogger().setLevel(logging_level)
    logging.info('starting camera api on port %d', port)

    app = Application()

    http_server = tornado.httpserver.HTTPServer(
        request_callback=app, xheaders=True)
    http_server.listen(port)
    ioloop = tornado.ioloop.IOLoop.instance()

    tornado.ioloop.PeriodicCallback(app.next_frame, 1000. / 60.).start()
    tornado.ioloop.PeriodicCallback(app.check_and_execute_callbacks, 1000).start()
    
    ioloop.start()
