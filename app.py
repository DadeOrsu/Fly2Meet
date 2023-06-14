from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search_flights', methods=['POST'])
def search_flights():
    # Recupera i dati dal form di richiesta
    departure_airport = request.form.get('departure_airport')
    departure_date = request.form.get('departure_date')
    arrival_date = request.form.get('arrival_date')
    max_base_price = request.form.get('max_base_price')
    max_duration = request.form.get('max_duration')
    max_wait_time = request.form.get('max_wait_time')
    destination = request.form.get('destination')

    # Esegui l'elaborazione dei dati come desiderato

    return f"Departure Airport: {departure_airport}, Departure Date: {departure_date}, Arrival Date: {arrival_date}, Max Base Price: {max_base_price}, Max Duration: {max_duration}, Max Wait Time: {max_wait_time}, Destination: {destination}"


if __name__ == '__main__':
    app.run()
