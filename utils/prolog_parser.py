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
    def _convert_to_prolog_duration(iso_duration):
        duration = parse_duration(iso_duration)
        duration_in_seconds = duration.total_seconds()
        return int(duration_in_seconds)

    # method to get the timezone name from the IANA code
    @staticmethod
    def _get_timezone_name_from_iana(iana_code):
        try:
            timezone = pytz.timezone(iana_code)
            now = datetime.now(pytz.utc)
            timezone_name = now.astimezone(timezone).tzname()
            return "'" + timezone_name + "'"
        except pytz.UnknownTimeZoneError:
            return None

    # method to get the date in prolog format
    def _get_date(self, date_string, airport_code):
        date = datetime.fromisoformat(date_string)
        airport_info = self.airports.airport_iata(airport_code)
        timezone_name = self._get_timezone_name_from_iana(airport_info.tzdb)
        offset = int(float(airport_info.tz) * 3600)
        dst = 'true' if airport_info.dst == 'E' else 'false'
        return f"date({date.year}, {date.month}, {date.day}, {date.hour}, {date.minute}, {date.second}, {offset}, " \
               f"{timezone_name.lower()}, {dst})"

    def _get_segment_data(self, segment):
        origin = segment['departure']['iataCode']
        destination = segment['arrival']['iataCode']
        carrier_code = "'" + segment['carrierCode'].lower() + "'"
        flight_number = segment['number']
        departure_date = self._get_date(segment['departure']['at'], origin)
        arrival_date = self._get_date(segment['arrival']['at'], destination)
        duration = self._convert_to_prolog_duration(segment['duration'])
        return origin, destination, carrier_code, flight_number, departure_date, arrival_date, duration

    # method to parse the flight offers in prolog facts
    def prolog_flight_parser(self, all_flight_offers):
        prolog_facts = []
        for flight in all_flight_offers:
            itineraries = flight['itineraries']
            if len(itineraries) == 1:
                segment = itineraries[0]['segments'][0]
                origin, destination, carrier_code, flight_number, departure_date, arrival_date, duration = (
                    self._get_segment_data(segment)
                )
                price = flight['price']['total']
                # add the flight offer as a prolog fact
                prolog_facts.append(
                    f"flight({origin.lower()}, {destination.lower()}, {carrier_code}, {flight_number}, "
                    f"{departure_date}, {arrival_date}, {duration}, {price})."
                )
            else:
                # data of first segment
                segment1 = itineraries[0]['segments'][0]
                origin1, destination1, carrier_code1, flight_number1, departure_date1, arrival_date1, duration1 = (
                    self._get_segment_data(segment1)
                )
                # data of second segment
                segment2 = itineraries[1]['segments'][0]
                origin2, destination2, carrier_code2, flight_number2, departure_date2, arrival_date2, duration2 = (
                    self._get_segment_data(segment2)
                )
                # total price
                price = flight['price']['total']
                prolog_facts.append(
                    f"itinerary({origin1.lower()}, {destination1.lower()},"
                    f" f({carrier_code1}, {flight_number1}, {departure_date1}, {arrival_date1}, {duration1}),"
                    f" f({carrier_code2}, {flight_number2}, {departure_date2}, {arrival_date2}, {duration2}),"
                    f" {price})."
                )

        return prolog_facts

    # method to parse the airport information in prolog facts
    def prolog_airport_parser(self, all_airports):
        prolog_facts = []
        for airport in all_airports:
            data = self.airports.airport_iata(airport)
            country = pycountry.countries.get(name=data.country).alpha_2
            iata_code = str(data.iata).lower()
            city_name = data.city
            country_code = country.lower()
            prolog_facts.append("airport(" + iata_code + ", '" + city_name + "', " + country_code + ").")
        return prolog_facts
