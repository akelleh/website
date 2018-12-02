import tornado.web
from util import Event


class TrafficHandler(tornado.web.RequestHandler):
    def get(self):
        event = Event(self, page_id=2)
        event.log()

        self.redirect('0.0.0.0:8051')
