import tornado.ioloop
import tornado.web
import logging
from util import import_logs, backfill_logs


if __name__ == "__main__":
    import_every = 15

    logging_level = logging.getLevelName('INFO')
    logging.getLogger().setLevel(logging_level)
    logging.info('Starting sql import service.')
    logging.info('Back-filling logs...')
    #backfill_logs()

    logging.info('Importing logs every {} minutes.'.format(import_every))

    ioloop = tornado.ioloop.IOLoop.instance()
    callback = tornado.ioloop.PeriodicCallback(import_logs, 1000. * 60. * import_every)
    callback.start()
    ioloop.start()
