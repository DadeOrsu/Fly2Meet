import requests
from utils.session_module import session
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
def get_flight_inspirations(_origin):
    url = 'https://test.api.amadeus.com/v1/shopping/flight-destinations'

    print(session.headers['Authorization'])
    params = {
        'origin': _origin,
    }

    try:
        response = session.get(url, params=params)
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
def get_flight_offers(_origin, _destination, _departure_date, _return_date, _max_base_price):
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
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
        response = session.get(url, params=params)
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
