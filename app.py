from datetime import datetime
from flask import Flask, render_template, request
from utils.helpers import *
from utils.prolog_parser import prolog_flight_parser
import time
import re

app = Flask(__name__)


# Filtro per formattare il prezzo
def format_price(value):
    return f"{value} €"


app.jinja_env.filters['format_price'] = format_price


# Filtro per formattare la durata
def format_duration(value):
    hours_match = re.search(r'(\d+)H', value)
    minutes_match = re.search(r'(\d+)M', value)

    hours = int(hours_match.group(1)) if hours_match else 0
    minutes = int(minutes_match.group(1)) if minutes_match else 0

    return f"{hours}h {minutes}m"


app.jinja_env.filters['format_duration'] = format_duration


# Filtro per formattare la data
def format_datetime(value):
    date_obj = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
    formatted_date = date_obj.strftime("%d/%m/%Y")
    formatted_time = date_obj.strftime("%H:%M")
    return f"{formatted_date} alle {formatted_time}"


app.jinja_env.filters['format_datetime'] = format_datetime


@app.route('/search_flights', methods=['POST'])
def search_flights():
    # dati presi dal form
    departure_city_1 = request.form.get('departure_city_1')
    departure_city_2 = request.form.get('departure_city_2')
    departure_date = request.form.get('departure_date')
    return_date = request.form.get('return_date')
    if return_date == '':
        return_date = None
    max_base_price = request.form.get('max_base_price')
    max_duration = int(request.form.get('max_duration'))
    max_wait_time = request.form.get('max_wait_time')
    destination = request.form.get('destination')
    destination_country = request.form.get('destination_country')
    same_airport = request.form.get('same_airport')
    # scrittura dei dati
    print(
        f"departure_city_1: {departure_city_1}\n"
        f"departure_city_2: {departure_city_2}\n"
        f"departure_date: {departure_date}\n"
        f"return_date: {return_date}\n"
        f"max_base_price: {max_base_price}\n"
        f"max_duration: {max_duration}\n"
        f"max_wait_time: {max_wait_time}\n"
        f"destination: {destination}\n"
        f"destination_country: {destination_country}\n"
        f"same_airport: {same_airport}\n"
    )
    iata_departure_city_1 = get_iata_code(departure_city_1)
    time.sleep(2)
    iata_departure_city_2 = get_iata_code(departure_city_2)
    time.sleep(2)
    first_city_offers = []
    second_city_offers = []
    if destination == "None" and destination_country == "None":
        print("Destinazione e destinazione country sono None")
        # richiesta delle flight inspirations per la prima città di partenza
        flights = get_flight_inspirations(iata_departure_city_1)
        # richiesta delle flight offers per la prima città di partenza
        first_city_offers = []
        first_city_destinations = set()
        for flight in flights:
            time.sleep(2)
            fo = get_flight_offers(iata_departure_city_1, flight['destination'], departure_date, return_date,
                                   max_base_price)
            print(fo)
            # aggiungo la destinazione all'insieme delle destinazioni della prima città di partenza
            if flight['destination'] not in first_city_destinations and len(fo['data']) > 0:
                print("Aggiungo la destinazione")
                first_city_destinations.add(flight['destination'])
            first_city_offers.extend(fo['data'])
        # scrivi all_flight_offers in un file json
        with open('flight_offers_paris.json', 'w') as file:
            json.dump(first_city_offers, file, indent=4)

        # richiesta delle flight offers per la seconda città di partenza
        second_city_offers = []
        for destination in first_city_destinations:
            time.sleep(2)
            fo = get_flight_offers(iata_departure_city_2, destination, departure_date, return_date, max_base_price)
            print(fo)
            second_city_offers.extend(fo['data'])

    else:
        if destination != 'None':
            print("Destinazione non è None")
            iata_destination = get_iata_code(destination)
            time.sleep(2)
            response = get_flight_offers(iata_departure_city_1, iata_destination, departure_date, return_date,
                                         max_base_price)
            first_city_offers.extend(response['data'])
            time.sleep(2)
            response = get_flight_offers(iata_departure_city_2, iata_destination, departure_date, return_date,
                                         max_base_price)
            second_city_offers.extend(response['data'])

        if destination_country != 'None':
            print("Destinazione country non è None")
            lat, lon = get_country_center_coordinates(destination_country)
            time.sleep(2)
            print(lat, lon)
            time.sleep(2)
            target_country_airports = get_airports_from_country_center_coordinates(lat, lon)
            print(target_country_airports)
            target_country_airports_iata = [airport['iataCode'] for airport in target_country_airports]

            for iata in target_country_airports_iata:
                time.sleep(2)
                response = get_flight_offers(iata_departure_city_1, iata, departure_date, return_date, max_base_price)
                first_city_offers.extend(response['data'])
                time.sleep(2)
                response = get_flight_offers(iata_departure_city_2, iata, departure_date, return_date, max_base_price)
                second_city_offers.extend(response['data'])

    # filtro le offerte di volo in base alla durata immessa
    first_city_offers = filter_flight_offers_by_duration(first_city_offers, max_duration)
    second_city_offers = filter_flight_offers_by_duration(second_city_offers, max_duration)

    # scrittura dei voli su file json
    write_flights_to_json(first_city_offers, 'jsonDumps/'+departure_city_1+departure_date+'.json')
    write_flights_to_json(second_city_offers, 'jsonDumps/'+departure_city_2+departure_date+'.json')
    # scrittura dei fatti prolog su file
    prolog_facts = prolog_flight_parser(first_city_offers)
    prolog_file = open('prolog_facts.pl', 'w')
    prolog_file.write('\n'.join(prolog_facts))
    prolog_file.close()
    return render_template("results.html", first_city_offers=first_city_offers, second_city_offers=second_city_offers)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
