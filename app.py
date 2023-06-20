from flask import Flask, render_template, request

app = Flask(__name__)


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

    # Ottieni access token

    # Elaborazione delle informazioni raccolte
    # ...
    print(departure_airport, departure_date, return_date, max_base_price, max_duration, max_wait_time, destination,
          same_airport, one_way)
    return "Risultati della ricerca dei voli"


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
