import logging
import numpy as np
from util import (ThreadedVideoCamera,
                  FrameBuffer,
                  check_and_record,
                  pub_record_event)
import yaml
import tornado.ioloop
import tornado.web
import logging



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, World!")


class Application(tornado.web.Application):
    def __init__(self):
        app_settings = {
            'default_handler_args': dict(status_code=404),
        }

        app_handlers = [
            (r'^/$', MainHandler),
        ]
        
        super(Application, self).__init__(app_handlers, **app_settings)


if __name__ == "__main__":
    port = 8000
    address = 'localhost'
    logging_level = logging.getLevelName('INFO')
    logging.getLogger().setLevel(logging_level)
    logging.info('starting camera api on %s:%d', address, port)

    http_server = tornado.httpserver.HTTPServer(
        request_callback=Application(), xheaders=True)
    http_server.listen(port, address=address)
    ioloop = tornado.ioloop.IOLoop.instance()

    frame_buffer = FrameBuffer(callbacks=[check_and_record,],
                                    window=5.)
    camera = ThreadedVideoCamera(-1, initialize_thread=True)
    def next_frame():
        image = camera.get_frame()
        frame_buffer.add_frame(image)
    tornado.ioloop.PeriodicCallback(next_frame, 1000. / 60.).start()
    
    ioloop.start()

