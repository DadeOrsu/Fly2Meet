from datetime import datetime
import pytz
from pyairports.airports import Airports
from isodate import parse_duration


# converte la durata iso in un timestamp in secondi
def convert_to_prolog_duration(durata_iso):
    durata = parse_duration(durata_iso)
    durata_in_secondi = durata.total_seconds()
    return int(durata_in_secondi)


def get_timezone_name_from_iana(_iana_code):
    try:
        _timezone = pytz.timezone(_iana_code)
        now = pytz.utc.localize(datetime.utcnow())
        _timezone_name = now.astimezone(_timezone).tzname()
        return _timezone_name
    except pytz.UnknownTimeZoneError:
        return None


# Funzione per ottenere la data in formato prolog date(Y,M,D,H,Mn,S,Off,TZ,DST)
def get_date(date_string, airport_code):
    date = datetime.fromisoformat(date_string)
    airports = Airports()
    airport_info = airports.airport_iata(airport_code)
    timezone_name = get_timezone_name_from_iana(airport_info.tzdb)
    # offset = get_timezone_offset(airport_info.tzdb)
    offset = int(float(airport_info.tz) * 3600)
    dst = 'true' if airport_info.dst == 'E' else 'false'
    return f"date({date.year}, {date.month}, {date.day}, {date.hour}, {date.minute}, {date.second}, {offset}," \
           f" '{timezone_name}', {dst})"


# Funzione per formattare l'offset in formato UTC
def format_offset_to_utc(offset):
    hours, minutes = offset.split(':')
    formatted_offset = f"{hours}{minutes}"
    return formatted_offset


def prolog_flight_parser(all_flight_offers):
    # Array di fatti prolog
    prolog_facts = []
    for flight in all_flight_offers:
        # flight(Origin, Destination, CarrierNo, FlightNo, DepDate, ArrDate, Duration, Price)
        origin = flight['itineraries'][0]['segments'][0]['departure']['iataCode']
        destination = flight['itineraries'][0]['segments'][0]['arrival']['iataCode']
        carrier_code = flight['itineraries'][0]['segments'][0]['carrierCode'].lower()
        flight_number = flight['itineraries'][0]['segments'][0]['number']
        departure_date = get_date(flight['itineraries'][0]['segments'][0]['departure']['at'], origin)
        arrival_date = get_date(flight['itineraries'][0]['segments'][0]['arrival']['at'], destination)
        duration = convert_to_prolog_duration(flight['itineraries'][0]['segments'][0]['duration'])
        price = flight['price']['total']
        prolog_facts.append(
            f"flight({origin.lower()},"  # origin
            f" {destination.lower()},"  # destination
            f" {carrier_code},"  # carrier code
            f" {flight_number},"  # flight number 
            f" {departure_date},"  # departure date
            f" {arrival_date},"  # arrival date
            f" {duration},"  # duration
            f" {price}).")  # price
    return prolog_facts
