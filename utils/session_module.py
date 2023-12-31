import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class APISession:
    def __init__(self, api_key, api_secret):
        self.session = self._create_session()
        self.access_token = self._get_access_token(api_key, api_secret)
        self.api_key = api_key
        self.api_secret = api_secret
        self.session.headers['Authorization'] = f'Bearer {self.access_token}'
        self.session.headers['Content-Type'] = 'application/json'

    # method to create a session with retrying
    @staticmethod
    def _create_session():
        retries = Retry(
            total=10,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504]
        )
        session = requests.Session()
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    # method to get the access token using client credentials grant
    def _get_access_token(self, api_key, api_secret):
        url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
        data = {
            'grant_type': 'client_credentials',
            'client_id': api_key,
            'client_secret': api_secret
        }
        try:
            response = self.session.post(url, data=data)
            response.raise_for_status()
            # save the time when the token expires
            self.expires_in = int(response.json()['expires_in']) + time.time()
            return response.json()['access_token']
        except requests.exceptions.RequestException as e:
            print(f'Error requesting access token: {e}')
            return None

    # method to make a GET request
    def get(self, url, params=None):
        try:
            # if the access token is expired, get a new one
            if time.time() > self.expires_in:
                self.session.headers.pop('Authorization', None)
                self.session.headers.pop('Content-Type', None)
                self.access_token = self._get_access_token(self.api_key, self.api_secret)
                self.session.headers['Authorization'] = f'Bearer {self.access_token}'
                self.session.headers['Content-Type'] = 'application/json'
            # make the request
            response = self.session.get(url, params=params)
            response.raise_for_status()
            # if the response is successful, return it
            return response
        except requests.exceptions.RequestException as e:
            print(f'Error during GET request: {e}')
            return None
