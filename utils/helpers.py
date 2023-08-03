import csv
from datetime import timedelta
from isodate import parse_duration
import requests
from utils.session_module import APISession
import json
import pycountry

# Create the session
api_key = 'kMotx0vA8lrM8jQ0P3xZA8mAwgYMQXDS'
api_secret = '2JatjYoMT1mSeL0i'
api_session = APISession(api_key, api_secret)


# Function to get the flight offers from json dump
def flight_from_json(file_path):
    flights = []
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        # ensure that the data is a list of flights
        if isinstance(data, list):
            flights = data
        else:
            print("Il file JSON non contiene una lista di voli.")
    except FileNotFoundError:
        print("File non trovato.")
    except json.JSONDecodeError:
        print("Errore durante la decodifica del file JSON.")
    return flights


# Function to write the flight offers on a json file
def write_flights_to_json(flights, file_path):
    try:
        with open(file_path, 'w') as file:
            json.dump(flights, file, indent=4)
    except FileNotFoundError:
        print("File non trovato.")
    except json.JSONDecodeError:
        print("Errore durante la decodifica del file JSON.")


# Function to get the flight inspirations using flight inspiration search API
def get_flight_inspirations(_origin, _departure_date, _max_price):
    url = 'https://test.api.amadeus.com/v1/shopping/flight-destinations'

    params = {
        'origin': _origin,
        'departureDate': _departure_date,
        'nonStop': 'true',
    }
    if _max_price is not None:
        params['maxPrice'] = _max_price
    try:
        response = api_session.get(url, params=params)
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


# Function to get the flight offers using Flight Offer Search API
def get_flight_offers(_origin, _destination, _departure_date, _return_date, _max_base_price):
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    params = {
        "originLocationCode": _origin,
        "destinationLocationCode": _destination,
        "departureDate": _departure_date,
        "currencyCode": "EUR",
        "nonStop": "true",
        "adults": 1
    }
    if _return_date is not None:
        params["returnDate"] = _return_date
    if _max_base_price is not None:
        params["maxPrice"] = _max_base_price
    try:
        response = api_session.get(url, params=params)
        if response is None:
            print(f"Errore durante la richiesta di Flight Offers: ")
            return None
        else:
            data = response.json()
            # Restituisci i dati delle offerte di volo
            return data
    except requests.exceptions.RequestException as e:
        print(f"Errore durante la richiesta di Flight Offers: {e}")
        return None


# Function used to get the iata code from the name of a city using Airport & City search API
def get_iata_code(name):
    url = "https://test.api.amadeus.com/v1/reference-data/locations"
    params = {
        "subType": "CITY",
        "keyword": name,
        "view": "LIGHT"
    }

    try:
        response = api_session.get(url, params=params)
        if response.status_code != 200:
            print(f"Errore durante la richiesta di IATA: {response.json()['errors'][0]['detail']}")
            return None
        else:
            data = response.json()
            # Restituisci i dati delle offerte di volo
            if data['meta']['count'] == 0:
                return None
            else:
                return data['data'][0]['iataCode']
    except requests.exceptions.RequestException as e:
        print(f"Errore durante la richiesta di IATA: {e}")
        return None


def get_airports_from_country_name(country_name):
    country_data = pycountry.countries.get(name=country_name)
    if country_data:
        filename = "utils/airport-codes.csv"
        with open(filename, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            # Skip the header
            next(reader, None)
            iata_codes = set()
            for row in reader:
                atype = row[1]
                iso_country = row[5]
                iata_code = row[9]
                # Puoi elaborare i dati come preferisci per ogni riga
                if iata_code != "" and iso_country == country_data.alpha_2 and atype == "large_airport":
                    iata_codes.add(iata_code)
            return iata_codes


# Function used to compare two hours expressed in ISO format
def compare_duration_with_hours(hour, duration_iso):
    duration_timedelta = parse_duration(duration_iso)
    hour_timedelta = timedelta(hours=hour)
    return duration_timedelta < hour_timedelta


# Function used to filter the flight offers based on the duration
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
                    break  # Exit the inner loop if at least one segment satisfies the condition
    return filtered_flight_offers


# get flight offers and update the iata codes
def get_flight_offers_and_update_iata_codes(origin, destination, departure_date, return_date, max_base_price,
                                            iata_codes):
    fo = get_flight_offers(origin, destination, departure_date, return_date, max_base_price)
    if fo is None:
        return None
    else:
        for tmp in fo['data']:
            for itinerary in tmp['itineraries']:
                for segment in itinerary['segments']:
                    iata_codes.add(segment['departure']['iataCode'])
                    iata_codes.add(segment['arrival']['iataCode'])
        return fo['data']
