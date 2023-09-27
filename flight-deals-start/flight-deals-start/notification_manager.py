from twilio.rest import Client
import os

TWILIO_SID = os.environ["TWILIO_SID"]
TWILIO_AUTH = os.environ["TWILIO_AUTH"]
TWILIO_NUMBER = os.environ["TWILIO_NUMBER"]
OWN_NUMBER = os.environ["OWN_NUMBER"]


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH)

    def send_text(self, message):
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_NUMBER,
            to=OWN_NUMBER
        )
        print(message.sid)

