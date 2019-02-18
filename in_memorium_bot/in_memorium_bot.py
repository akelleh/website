from tornado.ioloop import IOLoop
import json
from post import ImgurPoster
import logging
import time
from util import get_run_time


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel("INFO")

    with open("/app/config.json", "r") as fp:
        config = json.loads(fp.read())

    poster = ImgurPoster()

    ioloop = IOLoop()

    for post in config:
        when = get_run_time(post['when'])
        if when > time.time():
            logging.info("Posting {} at {}. Current time is {}.".format(post["post"],
                                                                        when,
                                                                        time.time()))
            ioloop.call_at(when, poster.post, post['post'])
    ioloop.start()
