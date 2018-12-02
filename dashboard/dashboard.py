from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from flask_dashboard import server
import logging

port = 8051

logging.info("Starting tornado server on {}".format(port))
http_server = HTTPServer(WSGIContainer(server))
http_server.listen(port)
IOLoop.instance().start()
