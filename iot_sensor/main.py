import util
import gc

wlan = util.do_connect()

while True:
    if wlan.isconnected():
        message_dict = util.get_message()
        util.post_message(message_dict)
    else:
        wlan = util.do_connect()
    gc.collect()
