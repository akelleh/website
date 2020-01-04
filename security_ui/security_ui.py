import logging
import yaml
import tornado.ioloop
import tornado.web
import logging
import os


with open(os.path.join(os.path.dirname(__file__), 'config.yml')) as config_file:
    config = yaml.load(config_file)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        cameras = config['cameras']
        self.render("html/index.html", cameras=cameras)


class Application(tornado.web.Application):
    def __init__(self):
        app_settings = {
            'default_handler_args': dict(status_code=404),
            'static_path': os.path.join(os.path.dirname(__file__), 'html')
        }

        app_handlers = [
            (r'^/$', MainHandler),
            (r'/html/(.*)', tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), "html")}),
        ]

        super(Application, self).__init__(app_handlers, **app_settings)


if __name__ == "__main__":
    port = 8001
    logging_level = logging.getLevelName('INFO')
    logging.getLogger().setLevel(logging_level)
    logging.info('starting security_ui on port %d', port)

    app = Application()

    http_server = tornado.httpserver.HTTPServer(
        request_callback=app, xheaders=True)
    http_server.listen(port)
    ioloop = tornado.ioloop.IOLoop.instance()

    ioloop.start()
