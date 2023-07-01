from datetime import timedelta
from isodate import parse_duration
import requests
from utils.session_module import session
from geopy import Nominatim
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
    params = {
        "originLocationCode": _origin,
        "destinationLocationCode": _destination,
        "departureDate": _departure_date,
        "maxPrice": _max_base_price,
        "currencyCode": "EUR",
        "nonStop": "true",
        "adults": 1
    }
    if _return_date is not None:
        params["returnDate"] = _return_date
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


# Funzione che restituisce il codice iata di una città in base al nome
def get_iata_code(name):
    url = "https://test.api.amadeus.com/v1/reference-data/locations"
    params = {
        "subType": "CITY",
        "keyword": name,
        "view": "LIGHT"
    }
    try:
        response = session.get(url, params=params)
        if response.status_code != 200:
            print(f"Errore durante la richiesta di IATA: {response.json()['errors'][0]['detail']}")
            return None
        else:
            data = response.json()
            # Restituisci i dati delle offerte di volo
            return data['data'][0]['iataCode']
    except requests.exceptions.RequestException as e:
        print(f"Errore durante la richiesta di IATA: {e}")
        return None


# Funzione per ottenere le coordinate geografiche a partire dal country name
def get_country_center_coordinates(country_name):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(country_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None


# Funzione per ottenere a partire dalle coordinate del centro di una nazione tutti gli aeroporti di quella nazione
def get_airports_from_country_center_coordinates(latitude, longitude):
    url = "https://test.api.amadeus.com/v1/reference-data/locations/airports"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "radius": 200
    }
    try:
        response = session.get(url, params=params)
        if response.status_code != 200:
            print(f"Errore durante la richiesta di AIRPORTS: {response.json()['errors'][0]['detail']}")
            return None
        else:
            data = response.json()
            # Restituisci i dati delle offerte di volo
            return data['data']
    except requests.exceptions.RequestException as e:
        print(f"Errore durante la richiesta di AIRPORTS: {e}")
        return None


# Funzione per comparare ora in input e durata in formato iso
def compare_duration_with_hours(hour, duration_iso):
    duration_timedelta = parse_duration(duration_iso)
    hour_timedelta = timedelta(hours=hour)
    return duration_timedelta < hour_timedelta


# funzione per filtrare i voli in base alla durata
def filter_flight_offers_by_duration(flight_offers, hour):
    filtered_flight_offers = []
    for flight_offer in flight_offers:
        itineraries = flight_offer['itineraries']
        for itinerary in itineraries:
            segments = itinerary['segments']
            for segment in segments:
                duration_iso = segment['duration']
                if compare_duration_with_hours(hour, duration_iso):
                    filtered_flight_offers.append(flight_offer)
                    break  # Esci dal ciclo interno se almeno un segmento soddisfa la condizione
    return filtered_flight_offers
