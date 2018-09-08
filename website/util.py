import urllib3


class LoggerClient(object):
    def __init__(self):
        self.url = 'logger:8889/'
        self.http = urllib3.PoolManager()

    def log(self, event):
        self.http.request('GET', self.url, fields=event)