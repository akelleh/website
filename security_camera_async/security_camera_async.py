import logging
import numpy as np
from util import (ThreadedVideoCamera,
                  FrameBuffer,
                  check_and_record,
                  pub_record_event,
                  array_to_image)
import yaml
import tornado.ioloop
import tornado.web
import logging


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("html/index.html")


class PowerHandler(tornado.web.RequestHandler):
    def get(self):
        power_on = bool(int(self.get_argument('on', True)))
        self.application.frame_buffer.power(power_on)
        self.write("Recording turned on: {}.".format(self.application.frame_buffer.should_execute_callbacks))


class FrameHandler(tornado.web.RequestHandler):
    def get(self):
        frame = self.application.camera.get_frame()
        array_to_image(frame, filename='temp_image.png')
        
class StatusHandler(tornado.web.RequestHandler):
    def get(self):
        if self.application.frame_buffer.should_execute_callbacks:
            self.write("On")
        else:
            self.write("Off")

class Application(tornado.web.Application):
    def __init__(self):
        app_settings = {
            'default_handler_args': dict(status_code=404),
        }

        app_handlers = [
            (r'^/$', MainHandler),
            (r'^/power$', PowerHandler),
            (r'/html/(.*)', tornado.web.StaticFileHandler, {'path': 'html'}),
            (r'^/status', StatusHandler),
        ]
    
        self.frame_buffer = FrameBuffer(callbacks=[check_and_record,],
                                        window=5.)
        self.camera = ThreadedVideoCamera(-1, initialize_thread=True)

        super(Application, self).__init__(app_handlers, **app_settings)

    def next_frame(self):
        image = self.camera.get_frame()
        self.frame_buffer.add_frame(image)


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
    
    ioloop.start()

