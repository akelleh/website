import tornado.ioloop
import tornado.web
import logging
import os

from handlers.writing import WritingHandler
from handlers.projects import ProjectHandler
from util import LoggerClient


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("html/index.html")


class Application(tornado.web.Application):
    def __init__(self):
        app_settings = {
            'default_handler_args': dict(status_code=404),
            'static_path': os.path.join(os.path.dirname(__file__), 'static')
        }

        app_handlers = [
            (r'^/$', WritingHandler),
            (r'^/writing$', WritingHandler),
            (r'^/projects$', ProjectHandler),
        ]

        self.logger_client = LoggerClient()
        super(Application, self).__init__(app_handlers, **app_settings)


if __name__ == "__main__":
    port = 8888
    address = '0.0.0.0'
    logging_level = logging.getLevelName('INFO')
    logging.getLogger().setLevel(logging_level)
    logging.info('starting foo_web_ui on %s:%d', address, port)

    http_server = tornado.httpserver.HTTPServer(
        request_callback=Application(), xheaders=True)
    http_server.listen(port, address=address)

    tornado.ioloop.IOLoop.instance().start()
