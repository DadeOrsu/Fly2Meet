import csv
from datetime import timedelta
from isodate import parse_duration
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
            print("The JSON file does not contain a flight list.")
    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON file.")
    return flights


# Function to write the flight offers on a json file
def write_flights_to_json(flights, file_path):
    try:
        with open(file_path, 'w') as file:
            json.dump(flights, file, indent=4)
    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON file.")


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
    response = api_session.get(url, params=params)
    if response is not None:
        data = response.json()
        return data['data']
    else:
        print("Error requesting Flight Inspirations")
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

    response = api_session.get(url, params=params)
    if response is None:
        print("Error requesting Flight Offers")
        return None
    else:
        data = response.json()
        # Restituisci i dati delle offerte di volo
        return data


# Function used to get the iata code from the name of a city using Airport & City search API
def get_iata_code(name):
    url = "https://test.api.amadeus.com/v1/reference-data/locations"
    params = {
        "subType": "CITY",
        "keyword": name,
        "view": "LIGHT"
    }
    response = api_session.get(url, params=params)
    if response is None:
        print("Error requesting IATA")
        return None
    else:
        data = response.json()
        if data['meta']['count'] == 0:
            print(f"No IATA code found for {name}")
            return None
        else:
            return data['data'][0]['iataCode']


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
        if itineraries:
            first_itinerary = itineraries[0]
            segments = first_itinerary['segments']
            if segments:
                first_segment = segments[0]
                duration_iso = first_segment['duration']
                if compare_duration_with_hours(hour, duration_iso):
                    filtered_flight_offers.append(flight_offer)
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
