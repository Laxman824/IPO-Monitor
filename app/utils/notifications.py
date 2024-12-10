# # utils/notifications.py
# from twilio.rest import Client
# from config.config import Config

# class NotificationManager:
#     def __init__(self):
#         self.client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)

#     def send_whatsapp_alert(self, phone, ipo_details):
#         message = f"""🚨 IPO Alert!

# IPO: {ipo_details['name']}
# Gain: {ipo_details['gain']}%
# Price: ₹{ipo_details['price']}
# GMP: ₹{ipo_details['gmp']}
# Date: {ipo_details['date']}
# Type: {ipo_details['type']}"""

#         try:
#             self.client.messages.create(
#                 body=message,
#                 from_=f'whatsapp:{Config.TWILIO_PHONE_NUMBER}',
#                 to=f'whatsapp:{phone}'
#             )
#             return True
#         except Exception as e:
#             print(f"Error sending WhatsApp alert: {str(e)}")
#             return False
# utils/notifications.py
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os
from config.config import Config

class NotificationManager:
    def __init__(self):
        self.client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
        self.from_number = Config.TWILIO_PHONE_NUMBER

    def send_whatsapp_message(self, to_number, message):
        """Send a WhatsApp message using Twilio"""
        try:
            # Format the 'from' number if needed
            if not self.from_number.startswith('whatsapp:'):
                from_number = f'whatsapp:{self.from_number}'
            else:
                from_number = self.from_number

            # Format the 'to' number if needed
            if not to_number.startswith('whatsapp:'):
                to_number = f'whatsapp:{to_number}'

            # Print debug information
            print(f"Sending WhatsApp message:")
            print(f"From: {from_number}")
            print(f"To: {to_number}")
            print(f"Message: {message[:100]}...")  # First 100 chars of message

            # Send the message
            message = self.client.messages.create(
                from_=from_number,
                body=message,
                to=to_number
            )

            # Print success information
            print(f"Message sent successfully! SID: {message.sid}")
            return True

        except TwilioRestException as e:
            print(f"Twilio error: {str(e)}")
            if e.code == 21614:
                print("Recipient has not opted in to your WhatsApp sandbox")
            elif e.code == 20003:
                print("Authentication error. Check your Twilio credentials")
            elif e.code == 21211:
                print("Invalid 'To' phone number format")
            return False
        except Exception as e:
            print(f"Error sending WhatsApp message: {str(e)}")
            return False

    def send_ipo_alert(self, to_number, ipo_details):
        """Send an IPO alert message"""
        message = f"""🚨 IPO Alert!

IPO: {ipo_details['name']}
Gain: {ipo_details['gain']}%
Price: ₹{ipo_details['price']}
GMP: ₹{ipo_details['gmp']}
Type: {ipo_details['type']}

Stay tuned for more updates!"""

        return self.send_whatsapp_message(to_number, message)

    def test_connection(self):
        """Test Twilio connection and credentials"""
        try:
            # Try to fetch account details
            account = self.client.api.accounts(Config.TWILIO_ACCOUNT_SID).fetch()
            print(f"Successfully connected to Twilio account: {account.friendly_name}")
            return True
        except Exception as e:
            print(f"Failed to connect to Twilio: {str(e)}")
            return False