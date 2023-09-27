import requests
import os
from flight_data import FlightData

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
FLIGHT_SEARCH_API = os.environ["FLIGHT_SEARCH_API"]


# This class is responsible for talking to the Flight Search API.
class FlightSearch:

    def iata_code(self, city_name):
        location = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {"apikey": FLIGHT_SEARCH_API}
        query = {"term": city_name, "location_types": "city"}
        response = requests.get(url=location, headers=headers, params=query)
        result = response.json()["locations"]
        code = result[0]["code"]
        return code

    def check_flights(self, city_code, destination_city_code, from_time, to_time):
        headers = {"apikey": FLIGHT_SEARCH_API}
        query = {
            "fly_from": city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "EUR"
        }

        response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", headers=headers, params=query)
        try:
            data = response.json()["data"][0]
        except IndexError:
            query["max_stopovers"] = 1
            response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", headers=headers, params=query)
            data = response.json()["data"][0]

            flight_data = FlightData(
                price=data["price"],
                city=data["route"][0]["cityFrom"],
                airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                departure_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0],
                stop_overs=1,
                via_city=data["route"][0]["cityTo"]
            )
            return flight_data
        else:
            flight_data = FlightData(
                price=data["price"],
                city=data["route"][0]["cityFrom"],
                airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                departure_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )
            print(f"{flight_data.destination_city}: {flight_data.price}")
            return flight_data
