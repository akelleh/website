import tornado.web

args = ['event_id', 'ts', 'page_id', 'user_id']

class EventHandler(tornado.web.RequestHandler):
    def get(self):
        event = {}
        for arg in args:
            val = self.get_argument(arg, default=None)
            event[arg] = val
        self.application.event_logger.log(event)
