
from flight_search import FlightSearch
from datetime import datetime, timedelta
from data_manager import DataManager
from notification_manager import NotificationManager
data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

sheet_data = data_manager.get_destination_data()

ORIGIN_CITY_IATA = "DUB"

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.iata_code(row["city"])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_data()

tomorrow = datetime.now() + timedelta(days=1)
in_six_months = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    flight = flight_search.check_flights(ORIGIN_CITY_IATA, destination["iataCode"], from_time=tomorrow, to_time=in_six_months)
    if flight.price < destination["lowestPrice"]:
        message = f"Low price alert! Only €{flight.price} to fly from {flight.city} to {flight.destination_city}, from{flight.departure_date} to {flight.return_date}"
        if flight.stop_overs > 0:
            message = f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."

        notification_manager.send_text(message)
        print(message)
