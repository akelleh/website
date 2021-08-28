import tornado.ioloop
import tornado.web
import logging


class MainHandler(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-type", "application/json")
        data = self.get_argument('body', 'No data received')
        self.write(data)

    def get(self):
        self.write("OK")


class Application(tornado.web.Application):
    def __init__(self):
        app_settings = {
            'default_handler_args': dict(status_code=404),
        }

        app_handlers = [
            (r'^/sensor_logger$', MainHandler),
        ]

        super(Application, self).__init__(app_handlers, **app_settings)


if __name__ == "__main__":
    port = 8002
    logging_level = logging.getLevelName('INFO')
    logging.getLogger().setLevel(logging_level)
    logging.info('starting tagging api on port %d', port)

    app = Application()

    http_server = tornado.httpserver.HTTPServer(
        request_callback=app, xheaders=True)
    http_server.listen(port)
    ioloop = tornado.ioloop.IOLoop.instance()

    ioloop.start()

