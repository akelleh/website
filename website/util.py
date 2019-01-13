import urllib3
import time
import uuid


class CookieNotSet(Exception):
    pass


class LoggerClient(object):
    def __init__(self):
        self.url = 'logger:8889/'
        self.http = urllib3.PoolManager()

    def log(self, event):
        self.http.request('GET', self.url, fields=event)


class Event(object):
    def __init__(self, request_handler, event_type='unset', page_id=None):
        self.request_handler = request_handler
        self.event_features = {}
        self.get_or_set_cookie()
        self.event_features['event_id'] = str(uuid.uuid4())
        self.event_features['ts'] = time.time()
        self.event_features['page_id'] = page_id
        self.event_features['event_type'] = event_type
        print(self.event_features)

    def log(self):
        self.request_handler.application.logger_client.log(self.event_features)

    def get_or_set_cookie(self):
        try:
            self.event_features['user_id'] = self.request_handler.get_cookie("user_id")
            if not self.event_features['user_id']:
                raise CookieNotSet
        except CookieNotSet:
            self.event_features['user_id'] = str(uuid.uuid4())
            self.request_handler.set_cookie("user_id", self.event_features['user_id'])