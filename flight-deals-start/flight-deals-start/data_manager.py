import requests
import os

SHEETY_GET_ENDPOINT = os.environ["SHEETY_GET_ENDPOINT"]


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        # 2. Use the Sheety API to GET all the data in that sheet and print it out.
        response = requests.get(url=SHEETY_GET_ENDPOINT)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data


    def update_destination_data(self):
    # make a PUT request and use the row id from sheet_data to update the Google Sheet with the IATA codes
        for city in self.destination_data:
            updated_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{SHEETY_GET_ENDPOINT}/{city['id']}", json=updated_data)




