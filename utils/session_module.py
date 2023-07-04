import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Create an object session of requests
session = requests.Session()

# Create a Retry object to retry the request in case of an error
retries = Retry(
    total=10,  # max retries
    backoff_factor=0.5,  # wait 0.5, 1, 2, 4, 8, ... seconds between retries
    status_forcelist=[500, 502, 503, 504]  # retry on these status codes
)


# Create an Adapter object to handle requests
adapter = HTTPAdapter(max_retries=retries)

# Register the adapter to the session
session.mount('http://', adapter)
session.mount('https://', adapter)

# Request of the access token
api_key = 'kMotx0vA8lrM8jQ0P3xZA8mAwgYMQXDS'
api_secret = '2JatjYoMT1mSeL0i'

url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}
data = {
    'grant_type': 'client_credentials',
    'client_id': api_key,
    'client_secret': api_secret
}
try:
    response = session.post(url, headers=headers, data=data)
    if response.status_code == 200:
        access_token = response.json()['access_token']
    else:
        print('Errore durante la richiesta di access token')
except requests.exceptions.RequestException as e:
    print(f'Errore durante la richiesta di access token: {e}')

# Add the access token to the session headers
session.headers['Authorization'] = f'Bearer {access_token}'
