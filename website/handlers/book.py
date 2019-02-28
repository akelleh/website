import tornado.web
from util import Event


class BookHandler(tornado.web.RequestHandler):
    def get(self):
        event = Event(self, page_id=2)
        event.log()

        self.render("../html/book.html", title="Machine Learning in Production")
