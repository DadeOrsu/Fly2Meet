from flask import Flask, render_template, request
from swiplserver import PrologMQI
from utils.helpers import *
from utils.prolog_parser import FlightParser
import time

app = Flask(__name__, static_folder='static', template_folder='templates')


@app.route('/search_flights', methods=['POST'])
def search_flights():
    # Collect the data from index.html template
    departure_city_1 = request.form.get('departure_city_1')
    departure_city_2 = request.form.get('departure_city_2')
    departure_date = request.form.get('departure_date')
    return_date = request.form.get('return_date') if request.form.get('return_date') != '' else None
    max_base_price = request.form.get('max_base_price') if request.form.get('max_base_price') != '' else None
    max_duration = request.form.get('max_duration') if request.form.get('max_duration') != '' else None
    max_wait_time = int(request.form.get('max_wait_time')) * 60 if request.form.get('max_wait_time') != '' else None
    target_cities = request.form.get('target_cities') if request.form.get('target_cities') != '' else None
    target_countries = request.form.get('target_countries') if request.form.get('target_countries') != '' else None
    same_airport = False if request.form.get('same_airport') is None else True
    new_city = False if request.form.get('new_city') is None else True
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
        f"new_city: {new_city}\n"
    )

    # Get the iata code for the first city
    iata_departure_city_1 = get_iata_code(departure_city_1)
    if iata_departure_city_1 is None:
        return render_template('display_results.html', error_msg="First departure city not found.")
    time.sleep(1)
    # Get the iata code for the second city
    iata_departure_city_2 = get_iata_code(departure_city_2)
    if iata_departure_city_2 is None:
        return render_template('display_results.html', error_msg="Second departure city not found.")
    time.sleep(1)
    # Arrays of the flight offers from the two departure cities
    first_city_offers = []
    second_city_offers = []
    # set of the iata codes of the airports
    iata_codes = set()
    # the destination city and destination country are not specified, the system chooses the destination
    if target_cities is None and target_countries is None:
        # API call to get the flight inspirations for the first city
        flight_inspirations = get_flight_inspirations(iata_departure_city_1, departure_date, max_base_price)
        if flight_inspirations is None:
            return render_template('display_results.html', error_msg="No flight inspirations found.")
        # Set of all destinations for the flights of the first departure city
        first_city_destinations = set()
        for flight in flight_inspirations:
            time.sleep(1)
            # API call to get all the flight offers using the information of the flight inspiration search
            fo = get_flight_offers_and_update_iata_codes(iata_departure_city_1, flight['destination'], departure_date,
                                                         return_date, max_base_price, iata_codes)
            if fo is not None:
                first_city_offers.extend(fo)
            # if there are flights for that destination, add it to the destination set
            if len(fo) > 0:
                first_city_destinations.add(flight['destination'])
        time.sleep(1)
        if not new_city:
            # Add the flight offers for the first city with the second city as destination
            fo = get_flight_offers_and_update_iata_codes(iata_departure_city_1, iata_departure_city_2, departure_date,
                                                         return_date, max_base_price, iata_codes)
            if fo is not None:
                first_city_offers.extend(fo)

        for target_cities in first_city_destinations:
            time.sleep(1)
            # API call to get the flight offers of the second departure city
            fo = get_flight_offers_and_update_iata_codes(iata_departure_city_2, target_cities, departure_date,
                                                         return_date, max_base_price, iata_codes)
            if fo is not None:
                second_city_offers.extend(fo)
        time.sleep(1)
        if not new_city:
            # Add the flight offers for the second city with the first city as destination
            fo = get_flight_offers_and_update_iata_codes(iata_departure_city_2, iata_departure_city_1, departure_date,
                                                         return_date, max_base_price, iata_codes)
            if fo is not None:
                second_city_offers.extend(fo)
    else:
        # if the destination city is specified
        if target_cities is not None:
            destinations = target_cities.split(", ")

            for dest in destinations:
                time.sleep(1)
                iata_destination = get_iata_code(dest)
                # if no iata found for the destination, continue with the next destination
                if iata_destination is None:
                    continue
                time.sleep(1)
                response = get_flight_offers_and_update_iata_codes(iata_departure_city_1, iata_destination,
                                                                   departure_date, return_date, max_base_price,
                                                                   iata_codes)
                if response is not None:
                    first_city_offers.extend(response)
                time.sleep(1)
                response = get_flight_offers_and_update_iata_codes(iata_departure_city_2, iata_destination,
                                                                   departure_date, return_date, max_base_price,
                                                                   iata_codes)
                if response is not None:
                    second_city_offers.extend(response)

        # if the destination country is specified
        if target_countries is not None:
            countries = target_countries.split(", ")
            for dest in countries:
                # get the iata codes of the airports in the country
                target_country_airports_iata = get_airports_from_country_name(dest)
                for iata in target_country_airports_iata:
                    time.sleep(1)
                    # get the flight offers for those airports from the first departure city
                    response = get_flight_offers_and_update_iata_codes(iata_departure_city_1, iata, departure_date,
                                                                       return_date, max_base_price, iata_codes)
                    if response is not None:
                        first_city_offers.extend(response)
                    time.sleep(1)
                    # get the flight offers for those airports from the second departure city
                    response = get_flight_offers_and_update_iata_codes(iata_departure_city_2, iata, departure_date,
                                                                       return_date, max_base_price, iata_codes)
                    if response is not None:
                        second_city_offers.extend(response)

    # filter the flight offers based on the max duration
    if max_duration is not None:
        first_city_offers = filter_flight_offers_by_duration(first_city_offers, int(max_duration))
        second_city_offers = filter_flight_offers_by_duration(second_city_offers, int(max_duration))

    # convert the flight offers to prolog facts
    flight_parser = FlightParser()
    airport_facts = flight_parser.prolog_airport_parser(iata_codes)
    all_flight_offers = first_city_offers + second_city_offers
    for i, item in enumerate(all_flight_offers):
        item['id'] = i
    prolog_facts = flight_parser.prolog_flight_parser(all_flight_offers)
    # write the prolog facts on a file
    prolog_file = open('prologFacts/prolog_facts.pl', 'w')
    prolog_file.write('\n'.join(airport_facts + prolog_facts))
    prolog_file.close()
    # collect the iata codes of the first city
    first_city_iata_codes = set()
    for tmp in first_city_offers:
        first_city_iata_codes.add(tmp['itineraries'][0]['segments'][0]['departure']['iataCode'].lower())

    # collect the iata codes of the second city
    second_city_iata_codes = set()
    for tmp in second_city_offers:
        second_city_iata_codes.add(tmp['itineraries'][0]['segments'][0]['departure']['iataCode'].lower())
    # array for the results of the query
    results = []
    # flag to check if return flights are included
    if return_date is not None:
        include_return = True
    else:
        include_return = False
    # Query the prolog file
    return_flag = 'yes' if include_return else 'no'
    same_airport_flag = 'yes' if same_airport else 'no'
    new_city_flag = 'yes' if new_city else 'no'
    waiting_time = max_wait_time if max_wait_time is not None else 'inf'
    # create the prolog server
    with PrologMQI() as mqi:
        with mqi.create_thread() as prolog_thread:
            # Query the file
            prolog_thread.query('consult(prologFacts/prolog_facts)')
            prolog_thread.query('consult(fly2meet)')
            for iata_code1 in first_city_iata_codes:
                for iata_code2 in second_city_iata_codes:
                    query = (f'fly2meet({iata_code1},{iata_code2}, bestsolution,{return_flag},{waiting_time},'
                             f'{same_airport_flag},{new_city_flag},Flights).')
                    result = prolog_thread.query(query)
                    if result:
                        results.extend(result[0]['Flights'])

    # sort the results by ranking
    def sort_key(x):
        return x['args'][3]

    results.sort(key=sort_key)
    return render_template("display_results.html", prolog_results=results, include_return=include_return)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
