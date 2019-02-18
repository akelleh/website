import tornado.ioloop
import tornado.web
import logging
from util import get_client


class ChartHandler(tornado.web.RequestHandler):
    def get(self, chart):
        client = get_client()
        if chart == 'pageviews':
            self.write(client.get_pageview_ts().to_json(orient='records'))
        elif chart == 'uniques':
            self.write(client.get_uv_ts().to_json(orient='records'))
        else:
            self.write("Chart type {} not supported.".format(chart))


class Application(tornado.web.Application):
    def __init__(self):
        app_settings = {
            'default_handler_args': dict(status_code=404),
        }

        app_handlers = [
            (r'^/([a-z]*)$', ChartHandler),
        ]

        super(Application, self).__init__(app_handlers, **app_settings)


if __name__ == "__main__":
    port = 8000
    address = '0.0.0.0'
    logging_level = logging.getLevelName('INFO')
    logging.getLogger().setLevel(logging_level)
    logging.info('starting event logger on %s:%d', address, port)

    http_server = tornado.httpserver.HTTPServer(
        request_callback=Application(), xheaders=True)
    http_server.listen(port, address=address)

    tornado.ioloop.IOLoop.instance().start()
