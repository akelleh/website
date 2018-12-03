from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from flask_dashboard import server
import logging

port = 8051
address = '0.0.0.0'

logging.info("Starting tornado server on {}:{}".format(address, port))
http_server = HTTPServer(WSGIContainer(server))
http_server.listen(port, address=address)
IOLoop.instance().start()
