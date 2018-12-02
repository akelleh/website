from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from flask_dashboard import server


port = 8051

http_server = HTTPServer(WSGIContainer(server))
http_server.listen(port)
IOLoop.instance().start()