import pytest
from app import app

# Put the application in testing mode
app.testing = True


# Create a test client


# Define a test for the / endpoint
def test_index():
    with app.test_client() as client:
        # Use the client to make requests
        response = client.get('/')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data


# post request with valid data
def test_search_flights():
    with app.test_client() as client:
        response = client.post('/search_flights', data={
            'departure_city_1': 'Paris',
            'departure_city_2': 'London',
            'departure_date': '2023-08-10',
            'return_date': '2023-08-20',
            'max_base_price': '500',
            'max_duration': '6',
            'max_wait_time': '3',
            'target_cities': 'Madrid, Barcelona',
            'target_countries': 'Italy, France',
            'same_airport': 'on',
        })

        # check that the request was successful
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data


# simple post request with no optional parameters
def test_search_flights_simple():
    with app.test_client() as client:
        response = client.post('/search_flights', data={
            'departure_city_1': 'Paris',
            'departure_city_2': 'London',
            'departure_date': '2023-08-10',
            'return_date': '',
            'max_base_price': '',
            'max_duration': '',
            'max_wait_time': '',
            'target_cities': '',
            'target_countries': '',
        })

        # check that the request was successful
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data


# post request where first city is invalid
def test_search_flights_invalid_city_1():
    with app.test_client() as client:
        response = client.post('/search_flights', data={
            'departure_city_1': 'NonExistingCity1',
            'departure_city_2': 'London',
            'departure_date': '2023-08-10',
            'return_date': '2023-08-20',
            'max_base_price': '500',
            'max_duration': '6',
            'max_wait_time': '3',
            'target_cities': 'Madrid, Barcelona',
            'target_countries': 'Italy, France',
            'same_airport': 'on',
        })

        # check that the request was successful
        assert response.status_code == 200
        assert b'First departure city not found.' in response.data


# post request where second city is invalid
def test_search_flights_invalid_city_2():
    with app.test_client() as client:
        response = client.post('/search_flights', data={
            'departure_city_1': 'London',
            'departure_city_2': 'NonExistingCity2',
            'departure_date': '2023-08-10',
            'return_date': '2023-08-20',
            'max_base_price': '500',
            'max_duration': '6',
            'max_wait_time': '3',
            'target_cities': 'Madrid, Barcelona',
            'target_countries': 'Italy, France',
            'same_airport': 'on',
        })

        # check that the request was successful
        assert response.status_code == 200
        assert b'Second departure city not found.' in response.data
