import config
import network
import urequests
import ujson


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(config.wifi['wifi_essid'],
                     config.wifi['wifi_password'])
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    return wlan

def get_message():
    message = {'sensor': config.sensor['name']}
    return message

def post_message(message_dict):
    post_data = ujson.dumps(message_dict)
    request_url = config.api['url']
    res = urequests.post(request_url,
                         headers={'content-type': 'application/json'},
                         data=post_data)
