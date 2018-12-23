import pandas as pd
import datetime


def get_run_time(when):
    when = pd.to_datetime(when)
    now = datetime.datetime.now()
    run_time = datetime.datetime(year=now.year,
                                 month=when.month,
                                 day=when.day,
                                 hour=when.hour,
                                 minute=when.minute,
                                 second=when.second)
    zero = datetime.datetime(year=1969, month=12, day=31, hour=19)
    when = (run_time - zero).total_seconds()  # time minus ET zero point
    return when


