import base64
import hashlib

from pyllegro import AllegroWebApi

API_KEY = 'your api key'  # You should download this from your allegro account
COUNTRY = 'PL'  # Available values = ['PL', 'UA', 'CZ']
SANDBOX = True  # Do not change this before You sure, that You fully understand how allegro api works!
USERNAME = 'your username'  # email or username
PASSWORD = 'your password'  # I'm not recommend You to use plain password in practice

# LOGIN

allegro_api = AllegroWebApi(API_KEY, SANDBOX, COUNTRY)
# You can login using plain password
user = allegro_api.login(USERNAME, PASSWORD)
# You can login using hash
password_hash = base64.b64encode(hashlib.sha256(PASSWORD.encode()).hexdigest()).encode()
user = allegro_api.login_encoded(USERNAME, password_hash)


# USER REQUESTS
# TODO: Write some examples
