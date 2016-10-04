from pyllegro import AllegroWebApi

API_KEY = 'your api key'  # You should download this from your allegro account
COUNTRY = 'PL'  # Available values = ['PL', 'UA', 'CZ']
SANDBOX = True  # Do not change this before You sure, that You fully understand how allegro api works!
USERNAME = 'your username'  # email or username
PASSWORD = 'your password'  # I'm not recommend You to use plain password in practice

allegro_api = AllegroWebApi(API_KEY, SANDBOX, COUNTRY)
user = allegro_api.login(USERNAME, PASSWORD)
print(user)
