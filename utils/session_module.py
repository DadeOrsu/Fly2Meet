import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Crea un oggetto Session di requests
session = requests.Session()

# Crea un oggetto Retry per riprovare la richiesta in caso di errore
retries = Retry(
    total=10,  # numero massimo di tentativi
    backoff_factor=0.5,  # fattore di ritardo trai tentativi
    status_forcelist=[500, 502, 503, 504]  # codici di errore per cui riprovare
)


# Crea un oggetto Adapter per gestire le richieste
adapter = HTTPAdapter(max_retries=retries)

# registra l'Adapter per la sessione
session.mount('http://', adapter)
session.mount('https://', adapter)

# Richiesta di access token
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

# Aggiungi access token a header di ogni richiesta
session.headers['Authorization'] = f'Bearer {access_token}'
