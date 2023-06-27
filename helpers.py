import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json


# Funzione per ottenere i dati dei voli da file json
def flight_from_json(file_path):
    flights = []
    try:
        # Apri il file JSON in modalità lettura
        with open(file_path, 'r') as file:
            # Carica il contenuto del file JSON
            data = json.load(file)

        # Assicurati che il file contenga una lista di voli
        if isinstance(data, list):
            flights = data
        else:
            print("Il file JSON non contiene una lista di voli.")
    except FileNotFoundError:
        print("File non trovato.")
    except json.JSONDecodeError:
        print("Errore durante la decodifica del file JSON.")

    return flights


# Funzione che restituisce flight inspirations
def get_flight_inspirations(_origin, _access_token):
    base_url = 'https://test.api.amadeus.com/v1'
    endpoint = '/shopping/flight-destinations'

    # Crea un oggetto Session di requests
    session = requests.Session()

    # Crea un oggetto Retry per riprovare la richiesta in caso di errore
    retries = Retry(
        total=5,  # numero massimo di tentativi
        backoff_factor=0.1,  # fattore di ritardo trai tentativi
        status_forcelist=[500, 502, 503, 504]  # codici di errore per cui riprovare
    )

    # Crea un oggetto Adapter per gestire le richieste
    adapter = HTTPAdapter(max_retries=retries)

    # registra l'Adapter per la sessione
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    url = base_url + endpoint
    headers = {
        'Authorization': f'Bearer {_access_token}'
    }
    params = {
        'origin': _origin,
    }

    try:
        response = session.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return data['data']
        else:
            error_message = response.json()['errors'][0]['detail']
            print(f'Errore durante la richiesta di Flight Inspirations: {error_message}')
            return None
    except requests.exceptions.RequestException as e:
        print(f'Errore durante la richiesta di Flight Inspirations: {e}')
        return None


# Funzione che restituisce le flight offers
def get_flight_offers(_origin, _destination, _departure_date, _return_date, _max_base_price, _access_token):
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    # Crea un oggetto Session di requests
    session = requests.Session()

    # Crea un oggetto Retry per riprovare la richiesta in caso di errore
    retries = Retry(
        total=5,  # numero massimo di tentativi
        backoff_factor=0.1,  # fattore di ritardo trai tentativi
        status_forcelist=[500, 502, 503, 504]  # codici di errore per cui riprovare
    )

    # Crea un oggetto Adapter per gestire le richieste
    adapter = HTTPAdapter(max_retries=retries)

    # registra l'Adapter per la sessione
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    headers = {
        "Authorization": f"Bearer {_access_token}",
        "Content-Type": "application/json"
    }
    if _return_date is not None:
        params = {
            "originLocationCode": _origin,  # Codice IATA dell'aeroporto di partenza
            "destinationLocationCode": _destination,  # Codice IATA dell'aeroporto di destinazione
            "departureDate": _departure_date,  # Formato: YYYY-MM-DD
            "returnDate": _return_date,  # Formato: YYYY-MM-DD
            "maxPrice": _max_base_price,  # Prezzo massimo
            "currencyCode": "EUR",  # Valuta
            "nonStop": "true",  # Solo voli diretti
            "adults": 1  # Numero di adulti
        }
    else:
        params = {
            "originLocationCode": _origin,  # Codice IATA dell'aeroporto di partenza
            "destinationLocationCode": _destination,  # Codice IATA dell'aeroporto di destinazione
            "departureDate": _departure_date,  # Formato: YYYY-MM-DD
            "maxPrice": _max_base_price,  # Prezzo massimo
            "currencyCode": "EUR",  # Valuta
            "nonStop": "true",  # Solo voli diretti
            "adults": 1  # Numero di adulti
        }
    try:
        response = session.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Errore durante la richiesta di Flight Offers: {response.json()['errors'][0]['detail']}")
            return None
        else:
            data = response.json()
            # Restituisci i dati delle offerte di volo
            return data
    except requests.exceptions.RequestException as e:
        print(f"Errore durante la richiesta di Flight Offers: {e}")
        return None


# Funzione che restituisce access token
def get_access_token(api_key, api_secret):
    base_url = 'https://test.api.amadeus.com'
    endpoint = '/v1/security/oauth2/token'

    # Crea un oggetto Session di requests
    session = requests.Session()

    # Crea un oggetto Retry per riprovare la richiesta in caso di errore
    retries = Retry(
        total=5,  # numero massimo di tentativi
        backoff_factor=0.1,  # fattore di ritardo trai tentativi
        status_forcelist=[500, 502, 503, 504]  # codici di errore per cui riprovare
    )

    # Crea un oggetto Adapter per gestire le richieste
    adapter = HTTPAdapter(max_retries=retries)

    # registra l'Adapter per la sessione
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    url = base_url + endpoint
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
            token = response.json()['access_token']
            return token
        else:
            print('Errore durante la richiesta di access token')
            return None
    except requests.exceptions.RequestException as e:
        print(f'Errore durante la richiesta di access token: {e}')
        return None
