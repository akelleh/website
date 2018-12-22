from imgurpython import ImgurClient
import logging
from creds import CLIENT_ID, CLIENT_SECRET, CREDENTIALS

client_id = CLIENT_ID
client_secret = CLIENT_SECRET
access_token = CREDENTIALS['access_token']
refresh_token = CREDENTIALS['refresh_token']


def get_client():
    return build_client(client_id, client_secret, access_token, refresh_token)


def build_client(client_id, client_secret, access_token=None, refresh_token=None, auth_pin=None):
    if auth_pin:
        credentials = authenticate(auth_pin)
        access_token = credentials['access_token']
        refresh_token = credentials['refresh_token']
        client = ImgurClient(client_id, client_secret, access_token, refresh_token)
    elif not (access_token and refresh_token):
        init_auth(client_id, client_secret)
    elif access_token and refresh_token:
        client = ImgurClient(client_id, client_secret, access_token, refresh_token)
    else:
        raise Exception("you must pass creds")
    return client


def init_auth(client_id, client_secret):
    client = ImgurClient(client_id, client_secret)
    authorization_url = client.get_auth_url('pin')
    logging.info("visit {} to authenticate".format(authorization_url))


def authenticate(auth_pin):
    credentials = client.authorize(auth_pin, 'pin')
    client.set_user_auth(credentials['access_token'], credentials['refresh_token'])
    return credentials