from twilio.rest import Client
import os

class NotificationManager:

    def __init__(self):
        self.client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])

    def send_whatsapp_message(self, message_body):
        message = self.client.messages.create(
            from_='whatsapp:+14155238886',
            body=message_body,
            to=os.environ["TWILIO_WHATSAPP_TO"],
        )
        print(message.sid)
