from tornado.ioloop import IOLoop
import json
from post import ImgurPoster
import logging
import pandas as pd
import time
import datetime


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel("INFO")

    with open("config.json", "r") as fp:
        config = json.loads(fp.read())

    poster = ImgurPoster()

    ioloop = IOLoop()
    for post in config:
        when = time.time() + 10
        when = (pd.to_datetime(post['when']) - datetime.datetime(year=1969, month=12, day=31, hour=19)).total_seconds() # time minus ET zero point
        ioloop.call_at(when, poster.post, post['post'])
    ioloop.start()
