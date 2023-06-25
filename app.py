from datetime import datetime
from flask import Flask, render_template, request
import time
import re


from helpers import *

app = Flask(__name__)

access_token = get_access_token('kMotx0vA8lrM8jQ0P3xZA8mAwgYMQXDS', '2JatjYoMT1mSeL0i')


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
    max_base_price = request.form.get('max_base_price')
    max_duration = request.form.get('max_duration')
    max_wait_time = request.form.get('max_wait_time')
    destination = request.form.get('destination')
    same_airport = request.form.get('same_airport')
    one_way = request.form.get('one_way')
    # scrittura dei dati
    print(departure_city_1, departure_city_2, departure_date, return_date, max_base_price, max_duration,
          max_wait_time, destination, same_airport, one_way)
    # richiesta delle flight inspirations per la prima città di partenza
    flights = get_flight_inspirations(departure_city_1, access_token)
    # richiesta delle flight offers per la prima città di partenza
    all_flight_offers = []
    first_city_destinations = set()
    for flight in flights:
        time.sleep(2)
        fo = get_flight_offers(departure_city_1, flight['destination'], departure_date, access_token)
        # aggiungo la destinazione all'insieme delle destinazioni della prima città di partenza
        if flight['destination'] not in first_city_destinations:
            first_city_destinations.add(flight['destination'])
        all_flight_offers.extend(fo['data'])
    print(json.dumps(all_flight_offers, indent=4))

    # richiesta delle flight offers per la seconda città di partenza
    second_city_offers = []
    for destination in first_city_destinations:
        time.sleep(2)
        fo = get_flight_offers(departure_city_2, destination, departure_date, access_token)
        second_city_offers.extend(fo['data'])
    # scrivi all_flight_offers in un file json
    with open('flight_offers_paris.json', 'w') as file:
        json.dump(all_flight_offers, file, indent=4)
    return render_template("results.html", all_flight_offers=all_flight_offers, second_city_offers=second_city_offers)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
