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

# # version2 qworking
# # utils/notifications.py
# from twilio.rest import Client
# from twilio.base.exceptions import TwilioRestException
# import os
# from config.config import Config

# class NotificationManager:
#     def __init__(self):
#         self.client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
#         self.from_number = Config.TWILIO_PHONE_NUMBER

#     def send_whatsapp_message(self, to_number, message):
#         """Send a WhatsApp message using Twilio"""
#         try:
#             # Format the 'from' number if needed
#             if not self.from_number.startswith('whatsapp:'):
#                 from_number = f'whatsapp:{self.from_number}'
#             else:
#                 from_number = self.from_number

#             # Format the 'to' number if needed
#             if not to_number.startswith('whatsapp:'):
#                 to_number = f'whatsapp:{to_number}'

#             # Print debug information
#             print(f"Sending WhatsApp message:")
#             print(f"From: {from_number}")
#             print(f"To: {to_number}")
#             print(f"Message: {message[:100]}...")  # First 100 chars of message

#             # Send the message
#             message = self.client.messages.create(
#                 from_=from_number,
#                 body=message,
#                 to=to_number
#             )

#             # Print success information
#             print(f"Message sent successfully! SID: {message.sid}")
#             return True

#         except TwilioRestException as e:
#             print(f"Twilio error: {str(e)}")
#             if e.code == 21614:
#                 print("Recipient has not opted in to your WhatsApp sandbox")
#             elif e.code == 20003:
#                 print("Authentication error. Check your Twilio credentials")
#             elif e.code == 21211:
#                 print("Invalid 'To' phone number format")
#             return False
#         except Exception as e:
#             print(f"Error sending WhatsApp message: {str(e)}")
#             return False

#     def send_ipo_alert(self, to_number, ipo_details):
#         """Send an IPO alert message"""
#         message = f"""🚨 IPO Alert!

# IPO: {ipo_details['name']}
# Gain: {ipo_details['gain']}%
# Price: ₹{ipo_details['price']}
# GMP: ₹{ipo_details['gmp']}
# Type: {ipo_details['type']}

# Stay tuned for more updates!"""

#         return self.send_whatsapp_message(to_number, message)

#     def test_connection(self):
#         """Test Twilio connection and credentials"""
#         try:
#             # Try to fetch account details
#             account = self.client.api.accounts(Config.TWILIO_ACCOUNT_SID).fetch()
#             print(f"Successfully connected to Twilio account: {account.friendly_name}")
#             return True
#         except Exception as e:
#             print(f"Failed to connect to Twilio: {str(e)}")
#             return False
# utils/notifications.py

# from twilio.rest import Client
# from config.config import Config
# import logging

# class NotificationManager:
#     def __init__(self):
#         try:
#             self.client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
#             self.from_number = Config.TWILIO_PHONE_NUMBER
#             logging.info("Twilio client initialized successfully")
#         except Exception as e:
#             logging.error(f"Failed to initialize Twilio client: {str(e)}")
#             raise

#     def send_whatsapp_message(self, to_number, message):
#         """Send a WhatsApp message"""
#         try:
#             # Format phone numbers
#             if not self.from_number.startswith('whatsapp:'):
#                 from_number = f'whatsapp:{self.from_number}'
#             else:
#                 from_number = self.from_number

#             if not to_number.startswith('whatsapp:'):
#                 to_number = f'whatsapp:{to_number}'

#             # Send message
#             message = self.client.messages.create(
#                 from_=from_number,
#                 body=message,
#                 to=to_number
#             )
            
#             logging.info(f"Message sent successfully. SID: {message.sid}")
#             return True
            
#         except Exception as e:
#             logging.error(f"Failed to send WhatsApp message: {str(e)}")
#             return False

#     def send_ipo_alert(self, to_number, ipo_details):
#         """Send IPO alert message"""
#         try:
#             message = f"""🚨 IPO Alert!

# IPO: {ipo_details['name']}
# Gain: {ipo_details['gain']}%
# Price: ₹{ipo_details['price']}
# GMP: ₹{ipo_details['gmp']}
# Type: {ipo_details['type']}

# Stay tuned for more updates!"""

#             return self.send_whatsapp_message(to_number, message)
            
#         except Exception as e:
#             logging.error(f"Failed to send IPO alert: {str(e)}")
#             return False

#     def test_connection(self):
#         """Test Twilio connection"""
#         try:
#             account = self.client.api.accounts(Config.TWILIO_ACCOUNT_SID).fetch()
#             logging.info(f"Connected to Twilio account: {account.friendly_name}")
#             return True
#         except Exception as e:
#             logging.error(f"Failed to connect to Twilio: {str(e)}")
#             return False
# utils/notifications.py
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from config.config import Config
import logging

class NotificationManager:
    def __init__(self):
        # Verify credentials exist
        if not all([Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN, Config.TWILIO_PHONE_NUMBER]):
            raise ValueError("Missing Twilio credentials. Check your .env file.")
            
        self.client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
        self.from_number = Config.TWILIO_PHONE_NUMBER

    def verify_credentials(self):
        """Test Twilio credentials"""
        try:
            # Try to fetch account info
            account = self.client.api.accounts(Config.TWILIO_ACCOUNT_SID).fetch()
            return {
                "status": "success",
                "message": f"Connected to Twilio account: {account.friendly_name}",
                "account_status": account.status
            }
        except TwilioRestException as e:
            error_message = ""
            if e.code == 20003:
                error_message = "Invalid Twilio credentials. Check your Account SID and Auth Token."
            elif e.code == 20001:
                error_message = "Missing or incorrect Twilio credentials."
            else:
                error_message = f"Twilio error: {str(e)}"
            return {
                "status": "error",
                "message": error_message,
                "code": e.code
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Unknown error: {str(e)}"
            }

    def send_whatsapp_message(self, to_number, message):
        """Send a WhatsApp message"""
        try:
            # Verify credentials first
            verification = self.verify_credentials()
            if verification["status"] == "error":
                raise ValueError(verification["message"])

            # Format numbers
            if not self.from_number.startswith('whatsapp:'):
                from_number = f'whatsapp:{self.from_number}'
            else:
                from_number = self.from_number

            if not to_number.startswith('whatsapp:'):
                to_number = f'whatsapp:{to_number}'

            # Print debug info
            print(f"Sending from: {from_number}")
            print(f"Sending to: {to_number}")

            # Send message
            message = self.client.messages.create(
                from_=from_number,
                body=message,
                to=to_number
            )

            return {
                "status": "success",
                "message_sid": message.sid
            }

        except TwilioRestException as e:
            error_message = ""
            if e.code == 21211:
                error_message = "Invalid 'To' phone number format"
            elif e.code == 21608:
                error_message = "User has not joined your WhatsApp sandbox"
            elif e.code == 21614:
                error_message = "Invalid 'From' phone number"
            else:
                error_message = f"Twilio error: {str(e)}"
            
            logging.error(error_message)
            return {
                "status": "error",
                "message": error_message,
                "code": e.code
            }
        except Exception as e:
            error_message = f"Failed to send message: {str(e)}"
            logging.error(error_message)
            return {
                "status": "error",
                "message": error_message
            }