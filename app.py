import requests
from flask import Flask, render_template, request

from helpers import get_access_token

app = Flask(__name__)

access_token = get_access_token('kMotx0vA8lrM8jQ0P3xZA8mAwgYMQXDS', '2JatjYoMT1mSeL0i')


def get_data(departure_airport, _access_token):
    url = "https://test.api.amadeus.com/v1/reference-data/locations"
    headers = {
        "Authorization": f"Bearer {_access_token}"
    }
    params = {
        "subType": "AIRPORT",
        "keyword": departure_airport
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()


@app.route('/search_flights', methods=['POST'])
def search_flights():
    # dati presi dal form
    departure_airport = request.form.get('departure_airport')
    departure_date = request.form.get('departure_date')
    return_date = request.form.get('return_date')
    max_base_price = request.form.get('max_base_price')
    max_duration = request.form.get('max_duration')
    max_wait_time = request.form.get('max_wait_time')
    destination = request.form.get('destination')
    same_airport = request.form.get('same_airport')
    one_way = request.form.get('one_way')

    print(departure_airport, departure_date, return_date, max_base_price, max_duration, max_wait_time, destination,
          same_airport, one_way)
    return "Risultati della ricerca dei voli"


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
