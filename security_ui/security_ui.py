import logging
import yaml
import tornado.ioloop
import tornado.web
import logging


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("html/index.html")


class Application(tornado.web.Application):
    def __init__(self):
        app_settings = {
            'default_handler_args': dict(status_code=404),
        }

        app_handlers = [
            (r'^/$', MainHandler),
            (r'/html/(.*)', tornado.web.StaticFileHandler, {'path': 'html'}),
        ]

        super(Application, self).__init__(app_handlers, **app_settings)


if __name__ == "__main__":
    port = 8000
    logging_level = logging.getLevelName('INFO')
    logging.getLogger().setLevel(logging_level)
    logging.info('starting security_ui on port %d', port)

    app = Application()

    http_server = tornado.httpserver.HTTPServer(
        request_callback=app, xheaders=True)
    http_server.listen(port)
    ioloop = tornado.ioloop.IOLoop.instance()

    ioloop.start()

