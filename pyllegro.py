import json
from base64 import b64encode
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse
from urllib.request import Request, urlopen

from suds.client import Client

from allegro_user import AllegroUser, SafeAllegroUser


class AllegroWebApi(object):
    def __init__(self, api_key, sandbox=True, country='PL',
                 new_client_id=None, new_client_secret=None, new_api_key=None, new_redirect_uri=None):
        if country.upper() == 'CZ':
            self.country_code = 56
        elif country.upper() == 'UA':
            self.country_code = 209
        else:  # PL
            self.country_code = 1
        self.sandbox = sandbox
        if sandbox:
            self.client = Client('https://webapi.allegro.pl.webapisandbox.pl/service.php?wsdl')
        else:
            self.client = Client('https://webapi.allegro.pl/service.php?wsdl')
        self.api_key = api_key
        # version # You should first call check_status() if request need some of this
        self.program_version = None
        self.cats_version = None
        self.api_version = None
        self.attrib_version = None
        self.form_sell_version = None
        self.site_version = None
        self.ver_key = None  # This one is most important

        # New API things (required for safe login user using OAuth2)
        self.new_client_id = new_client_id
        self.new_client_secret = new_client_secret
        self.new_api_key = new_api_key
        self.new_redirect_uri = new_redirect_uri

    def login(self, login, password):
        """WARNING: Using this method in apps for other user is fucking stupid due to plain-text password
        This is factory method produces AllegroUser"""
        if self.ver_key is None:
            self.check_status()
        user_login_data = self.client.service.doLogin(userLogin=login, userPassword=password,
                                                      countryCode=self.country_code,
                                                      webapiKey=self.api_key, localVersion=self.ver_key)
        session_id = user_login_data['sessionHandlePart']
        user_id = user_login_data['userId']
        start_time = user_login_data['serverTime']
        return AllegroUser(self, user_id, session_id, start_time)

    def login_encoded(self, login, password_hash):
        """ WARNING: Using this method in apps for other users is twice fucking stupid
                     due to other db leaks contains exactly hashes \n
        This is factory method produces AllegroUser\n
        :param login: username or email\n
        :param password_hash: sha256 password hash encoded with base64 - base64(sha256(password))\n
        """
        if self.ver_key is None:
            self.check_status()
        user_login_data = self.client.service.doLoginEnc(userLogin=login, userHashPassword=password_hash,
                                                         countryCode=self.country_code,
                                                         webapiKey=self.api_key, localVersion=self.ver_key)
        session_id = user_login_data['sessionHandlePart']
        user_id = user_login_data['userId']
        start_time = user_login_data['serverTime']
        return AllegroUser(self, user_id, session_id, start_time)

    def get_url_to_auth(self):
        url = 'https://ssl.allegro.pl/auth/oauth/authorize' \
              '?response_type=code' \
              '&client_id={}' \
              '&api-key={}' \
              '&redirect_uri={}'.format(self.new_client_id, self.new_api_key, self.new_redirect_uri)
        return url

    def get_token_to_login(self, port=8000):
        # WARNING: This method is NOT thread-safe
        # FIXME: find another way to store token and ensure method works properly
        class AllegroRequestHandler(BaseHTTPRequestHandler):
            user_token = None

            def do_GET(self):
                token = self.path.rsplit('?code=', 1)[-1]
                AllegroRequestHandler.user_token = token

        server = HTTPServer(('0.0.0.0', port), AllegroRequestHandler)
        server.handle_request()
        user_token = AllegroRequestHandler.user_token
        AllegroRequestHandler.user_token = None
        return user_token

    def login_with_token(self, token):
        url = 'https://ssl.allegro.pl/auth/oauth/token'
        post_data = {'grant_type': 'authorization_code',
                     'code': token,
                     'api-key': self.new_api_key,
                     'redirect-uri': self.new_redirect_uri
                     }
        post_data = parse.urlencode(post_data).encode()
        basic_auth = 'Basic ' + b64encode((self.new_client_id + ':' + self.new_client_secret).encode('utf-8')).decode()
        headers = {'Authorization': basic_auth}

        request = Request(url, post_data, headers=headers)

        response = urlopen(request).read().decode()
        response_json = json.loads(response)

        user_login_data = self.client.service.doLoginWithAccessToken(
            accessToken=token,
            countryCode=self.country_code,
            webapiKey=self.api_key)

        session_id = user_login_data['sessionHandlePart']
        user_id = user_login_data['userId']
        start_time = user_login_data['serverTime']
        access_token = response_json['access_token']
        refresh_token = response_json['refresh_token']
        expires_in = response_json['expires_in']
        return SafeAllegroUser(self, user_id, session_id, start_time, access_token, refresh_token, expires_in)

    def get_user_id(self, user_login):
        return self.client.service.doGetUserID(self.country_code, user_login, webapiKey=self.api_key)

    def check_status(self):
        """Check versions on server """
        # TODO: call this if self.ver_key is None when is needed
        version = self.client.service.doQueryAllSysStatus(countryId=self.country_code, webapiKey=self.api_key)
        for app in version[0]:
            if app['countryId'] == self.country_code:
                self.program_version = app['programVersion']
                self.cats_version = app['catsVersion']
                self.api_version = app['apiVersion']
                self.attrib_version = app['attribVersion']
                self.form_sell_version = app['formSellVersion']
                self.site_version = app['siteVersion']
                self.ver_key = app['verKey']
                break
        return version
