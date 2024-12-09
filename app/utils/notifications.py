# utils/notifications.py
from twilio.rest import Client
from config.config import Config

class NotificationManager:
    def __init__(self):
        self.client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)

    def send_whatsapp_alert(self, phone, ipo_details):
        message = f"""🚨 IPO Alert!

IPO: {ipo_details['name']}
Gain: {ipo_details['gain']}%
Price: ₹{ipo_details['price']}
GMP: ₹{ipo_details['gmp']}
Date: {ipo_details['date']}
Type: {ipo_details['type']}"""

        try:
            self.client.messages.create(
                body=message,
                from_=f'whatsapp:{Config.TWILIO_PHONE_NUMBER}',
                to=f'whatsapp:{phone}'
            )
            return True
        except Exception as e:
            print(f"Error sending WhatsApp alert: {str(e)}")
            return False
