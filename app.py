from datetime import datetime
from flask import Flask, render_template, request
from utils.helpers import *
from utils.prolog_parser import FlightParser
import time
import re

app = Flask(__name__, static_folder='static', template_folder='templates')


# Filter for Jinja to format the price
def format_price(value):
    return f"{value} €"


app.jinja_env.filters['format_price'] = format_price


# Filter for Jinja to format the duration of the flights
def format_duration(value):
    hours_match = re.search(r'(\d+)H', value)
    minutes_match = re.search(r'(\d+)M', value)

    hours = int(hours_match.group(1)) if hours_match else 0
    minutes = int(minutes_match.group(1)) if minutes_match else 0

    return f"{hours}h {minutes}m"


app.jinja_env.filters['format_duration'] = format_duration


# Filter for Jinja to format the departure and arrival time
def format_datetime(value):
    date_obj = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
    formatted_date = date_obj.strftime("%d/%m/%Y")
    formatted_time = date_obj.strftime("%H:%M")
    return f"{formatted_date} alle {formatted_time}"


app.jinja_env.filters['format_datetime'] = format_datetime


@app.route('/search_flights', methods=['POST'])
def search_flights():
    # Collect the data from index.html template
    departure_city_1 = request.form.get('departure_city_1')
    departure_city_2 = request.form.get('departure_city_2')
    departure_date = request.form.get('departure_date')
    return_date = request.form.get('return_date')
    if return_date == '':
        return_date = None
    max_base_price = request.form.get('max_base_price')
    if max_base_price == '':
        max_base_price = None
    max_duration = request.form.get('max_duration')
    if max_duration == '':
        max_duration = None
    max_wait_time = request.form.get('max_wait_time')
    if max_wait_time == '':
        max_wait_time = None
    target_cities = request.form.get('target_cities')
    if target_cities == '':
        target_cities = None
    target_countries = request.form.get('target_countries')
    if target_countries == '':
        target_countries = None
    same_airport = request.form.get('same_airport')
    # Print the collected datas on the console
    print(
        f"departure_city_1: {departure_city_1}\n"
        f"departure_city_2: {departure_city_2}\n"
        f"departure_date: {departure_date}\n"
        f"return_date: {return_date}\n"
        f"max_base_price: {max_base_price}\n"
        f"max_duration: {max_duration}\n"
        f"max_wait_time: {max_wait_time}\n"
        f"destination: {target_cities}\n"
        f"destination_country: {target_countries}\n"
        f"same_airport: {same_airport}\n"
    )

    # Get the iata code for the first city
    iata_departure_city_1 = get_iata_code(departure_city_1)
    time.sleep(2)
    # Get the iata code for the second city
    iata_departure_city_2 = get_iata_code(departure_city_2)
    time.sleep(2)
    # Arrays of the flight offers from the two departure cities
    first_city_offers = []
    second_city_offers = []
    # set of the iata codes of the airports
    iata_codes = set()
    # the destination city and destination country are not specified, the system chooses the destination
    if target_cities is None and target_countries is None:
        # API call to get the flight inspirations for the first city
        flight_inspirations = get_flight_inspirations(iata_departure_city_1, departure_date, max_base_price)
        # Array that collects all the offers of the first departure city
        first_city_offers = []
        # Set of all destinations for the flights of the first departure city
        first_city_destinations = set()
        for flight in flight_inspirations:
            time.sleep(2)
            # API call to get all the flight offers using the information of the flight inspiration search
            fo = get_flight_offers_and_update_iata_codes(iata_departure_city_1, flight['destination'], departure_date,
                                                         return_date, max_base_price, iata_codes)
            first_city_offers.extend(fo)
            # if there are flights for that destination, add it to the destination set
            if flight['destination'] not in first_city_destinations and len(fo) > 0:
                first_city_destinations.add(flight['destination'])
        # Add the flight offers for the first city with the second city as destination
        fo = get_flight_offers_and_update_iata_codes(iata_departure_city_1, iata_departure_city_2, departure_date,
                                                     return_date, max_base_price, iata_codes)
        first_city_offers.extend(fo)
        # Search of the flight offers for the second departure city using the destinations set of the first search
        second_city_offers = []
        for target_cities in first_city_destinations:
            time.sleep(2)
            # API call to get the flight offers of the second departure city
            fo = get_flight_offers_and_update_iata_codes(iata_departure_city_2, target_cities, departure_date,
                                                         return_date, max_base_price, iata_codes)
            second_city_offers.extend(fo)
        # Add the flight offers for the second city with the first city as destination
        fo = get_flight_offers_and_update_iata_codes(iata_departure_city_2, iata_departure_city_1, departure_date,
                                                     return_date, max_base_price, iata_codes)
        second_city_offers.extend(fo)

    else:
        # if the destination city is specified
        if target_cities is not None:
            destinations = target_cities.split(", ")

            for dest in destinations:
                time.sleep(2)
                iata_destination = get_iata_code(dest)
                # if no iata found for the destination, continue with the next destination
                if iata_destination is None:
                    continue
                time.sleep(2)
                response = get_flight_offers_and_update_iata_codes(iata_departure_city_1, iata_destination,
                                                                   departure_date, return_date, max_base_price,
                                                                   iata_codes)
                first_city_offers.extend(response)
                time.sleep(2)
                response = get_flight_offers_and_update_iata_codes(iata_departure_city_2, iata_destination,
                                                                   departure_date, return_date, max_base_price,
                                                                   iata_codes)
                second_city_offers.extend(response)

        # if the destination country is specified
        if target_countries is not None:
            countries = target_countries.split(", ")
            for dest in countries:
                # get the coordinates of the center of the country
                lat, lon = get_country_center_coordinates(dest)
                time.sleep(2)
                # get the airports in a certain radius from the center of the country
                target_country_airports = get_airports_from_country_center_coordinates(lat, lon, dest)
                # get the iata code of the airports found, if the airport is already in the iata_codes array, skip it
                target_country_airports_iata = [airport['iataCode'] for airport in target_country_airports
                                                if airport['iataCode'] not in iata_codes]
                for iata in target_country_airports_iata:
                    time.sleep(2)
                    # get the flight offers for those airports from the first departure city
                    response = get_flight_offers_and_update_iata_codes(iata_departure_city_1, iata, departure_date,
                                                                       return_date, max_base_price, iata_codes)
                    first_city_offers.extend(response)
                    time.sleep(2)
                    # get the flight offers for those airports from the second departure city
                    response = get_flight_offers_and_update_iata_codes(iata_departure_city_2, iata, departure_date,
                                                                       return_date, max_base_price, iata_codes)
                    second_city_offers.extend(response)

    # filter the flight offers based on the max duration
    if max_duration is not None:
        first_city_offers = filter_flight_offers_by_duration(first_city_offers, int(max_duration))
        second_city_offers = filter_flight_offers_by_duration(second_city_offers, int(max_duration))

    # write the offers on a json dump
    write_flights_to_json(first_city_offers, 'jsonDumps/' + departure_city_1 + departure_date + '.json')
    write_flights_to_json(second_city_offers, 'jsonDumps/' + departure_city_2 + departure_date + '.json')
    # convert the flight offers to prolog facts
    flight_parser = FlightParser()
    airport_facts = flight_parser.prolog_airport_parser(iata_codes)
    prolog_facts = flight_parser.prolog_flight_parser(first_city_offers + second_city_offers)
    # write the prolog facts on a file
    prolog_file = open('prologFacts/prolog_facts.pl', 'w')
    prolog_file.write('\n'.join(airport_facts + prolog_facts))
    prolog_file.close()
    return render_template("results.html", first_city_offers=first_city_offers, second_city_offers=second_city_offers)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
