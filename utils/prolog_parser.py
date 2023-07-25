from datetime import datetime
import pytz
import pycountry
from isodate import parse_duration
from pyairports.airports import Airports


class FlightParser:
    def __init__(self):
        self.airports = Airports()

    # method to convert the duration from ISO 8601 format to seconds
    @staticmethod
    def convert_to_prolog_duration(iso_duration):
        duration = parse_duration(iso_duration)
        duration_in_seconds = duration.total_seconds()
        return int(duration_in_seconds)

    # method to get the timezone name from the IANA code
    @staticmethod
    def get_timezone_name_from_iana(iana_code):
        try:
            timezone = pytz.timezone(iana_code)
            now = datetime.now(pytz.utc)
            timezone_name = now.astimezone(timezone).tzname()
            return "'" + timezone_name + "'"
        except pytz.UnknownTimeZoneError:
            return None

    # method to get the date in prolog format
    def get_date(self, date_string, airport_code):
        date = datetime.fromisoformat(date_string)
        airport_info = self.airports.airport_iata(airport_code)
        timezone_name = self.get_timezone_name_from_iana(airport_info.tzdb)
        offset = int(float(airport_info.tz) * 3600)
        dst = 'true' if airport_info.dst == 'E' else 'false'
        return f"date({date.year}, {date.month}, {date.day}, {date.hour}, {date.minute}, {date.second}, {offset}, " \
               f"{timezone_name.lower()}, {dst})"

    # method to parse the flight offers in prolog facts
    def prolog_flight_parser(self, all_flight_offers):
        prolog_facts = []
        for flight in all_flight_offers:
            itineraries = flight['itineraries']
            for itinerary in itineraries:
                segments = itinerary['segments']
                for segment in segments:
                    origin = segment['departure']['iataCode']
                    destination = segment['arrival']['iataCode']
                    carrier_code = "'" + segment['carrierCode'].lower() + "'"
                    flight_number = segment['number']
                    departure_date = self.get_date(segment['departure']['at'], origin)
                    arrival_date = self.get_date(segment['arrival']['at'], destination)
                    duration = self.convert_to_prolog_duration(segment['duration'])
                    price = flight['price']['total']
                    # add the flight offer as a prolog fact
                    prolog_facts.append(
                        f"flight({origin.lower()}, {destination.lower()}, {carrier_code}, {flight_number}, "
                        f"{departure_date}, {arrival_date}, {duration}, {price})."
                    )
        return prolog_facts

    # method to parse the airport information in prolog facts
    def prolog_airport_parser(self, all_airports):
        prolog_facts = []
        for airport in all_airports:
            data = self.airports.airport_iata(airport)
            country = pycountry.countries.get(name=data.country).alpha_2
            prolog_facts.append("airport(" + str(data.iata).lower() + ").")
            prolog_facts.append("\tin(" + str(data.iata).lower() + ", " + country.lower() + ").")
            prolog_facts.append("\tcity(" + str(data.iata.lower()) + ", " + data.city.lower().replace(' ', '_') + ").")
        return prolog_facts
