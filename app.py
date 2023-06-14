# file: app.py
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/process_form', methods=['POST'])
def process_form():
    name = request.form['name']
    email = request.form['email']

    # Esegui l'elaborazione dei dati come desiderato

    return f"Name: {name}, Email: {email}"


if __name__ == '__main__':
    app.run()
