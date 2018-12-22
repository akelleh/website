from imgurpython import ImgurClient
from creds import CLIENT_ID, CLIENT_SECRET

client_id =  CLIENT_ID
client_secret = CLIENT_SECRET

client = ImgurClient(client_id, client_secret)

# Authorization flow, pin example (see docs for other auth types)
authorization_url = client.get_auth_url('pin')
print(authorization_url)
# ... redirect user to `authorization_url`, obtain pin (or code or token) ...

credentials = client.authorize('PIN OBTAINED FROM AUTHORIZATION', 'pin')
client.set_user_auth(credentials['access_token'], credentials['refresh_token'])
