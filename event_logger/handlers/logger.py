import tornado.web
from util import event_args


class EventHandler(tornado.web.RequestHandler):
    def get(self):
        event = {}
        event_type = self.get_argument("event_type", "bad_event")
        for arg in event_args[event_type]:
            val = self.get_argument(arg, default=None)
            event[arg] = val
        self.application.event_logger[event_type].log(event)
