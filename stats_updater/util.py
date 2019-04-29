import redis
import logging


class RedisClient(redis.Redis):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_stats(self, message):
        for k, v in message.items():
            with self.lock('updater_lock', timeout=1):
                value = self.get(k)
                if value:
                    value = float(value)
                else:
                    value = 0.
                self.set(k, value + v)
                logging.info("updated the data for key {} from {} to {}.".format(k,
                                                                                 value,
                                                                                 value + v))
