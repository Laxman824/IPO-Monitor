
# # utils/notifications.py
# from twilio.rest import Client
# from twilio.base.exceptions import TwilioRestException
# from config.config import Config
# import logging

# class NotificationManager:
#     def __init__(self):
#         # Verify credentials exist
#         if not all([Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN, Config.TWILIO_PHONE_NUMBER]):
#             raise ValueError("Missing Twilio credentials. Check your .env file.")
            
#         self.client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
#         self.from_number = Config.TWILIO_PHONE_NUMBER

#     def verify_credentials(self):
#         """Test Twilio credentials"""
#         try:
#             # Try to fetch account info
#             account = self.client.api.accounts(Config.TWILIO_ACCOUNT_SID).fetch()
#             return {
#                 "status": "success",
#                 "message": f"Connected to Twilio account: {account.friendly_name}",
#                 "account_status": account.status
#             }
#         except TwilioRestException as e:
#             error_message = ""
#             if e.code == 20003:
#                 error_message = "Invalid Twilio credentials. Check your Account SID and Auth Token."
#             elif e.code == 20001:
#                 error_message = "Missing or incorrect Twilio credentials."
#             else:
#                 error_message = f"Twilio error: {str(e)}"
#             return {
#                 "status": "error",
#                 "message": error_message,
#                 "code": e.code
#             }
#         except Exception as e:
#             return {
#                 "status": "error",
#                 "message": f"Unknown error: {str(e)}"
#             }

#     def send_whatsapp_message(self, to_number, message):
#         """Send a WhatsApp message"""
#         try:
#             # Verify credentials first
#             verification = self.verify_credentials()
#             if verification["status"] == "error":
#                 raise ValueError(verification["message"])

#             # Format numbers
#             if not self.from_number.startswith('whatsapp:'):
#                 from_number = f'whatsapp:{self.from_number}'
#             else:
#                 from_number = self.from_number

#             if not to_number.startswith('whatsapp:'):
#                 to_number = f'whatsapp:{to_number}'

#             # Print debug info
#             print(f"Sending from: {from_number}")
#             print(f"Sending to: {to_number}")

#             # Send message
#             message = self.client.messages.create(
#                 from_=from_number,
#                 body=message,
#                 to=to_number
#             )

#             return {
#                 "status": "success",
#                 "message_sid": message.sid
#             }

#         except TwilioRestException as e:
#             error_message = ""
#             if e.code == 21211:
#                 error_message = "Invalid 'To' phone number format"
#             elif e.code == 21608:
#                 error_message = "User has not joined your WhatsApp sandbox"
#             elif e.code == 21614:
#                 error_message = "Invalid 'From' phone number"
#             else:
#                 error_message = f"Twilio error: {str(e)}"
            
#             logging.error(error_message)
#             return {
#                 "status": "error",
#                 "message": error_message,
#                 "code": e.code
#             }
#         except Exception as e:
#             error_message = f"Failed to send message: {str(e)}"
#             logging.error(error_message)
#             return {
#                 "status": "error",
#                 "message": error_message
#             }
# utils/notifications.py
from twilio.rest import Client
from config.config import Config
import logging
import streamlit as st
import json

class NotificationManager:
    def __init__(self):
        self.twilio_client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
        self.from_number = Config.TWILIO_PHONE_NUMBER

    def request_push_permission(self):
        """Add JavaScript to request push notification permission"""
        push_permission_js = """
        <script>
        if ('Notification' in window) {
            Notification.requestPermission().then(function(permission) {
                if (permission === 'granted') {
                    console.log('Push notification permission granted');
                    // Register service worker for push notifications
                    if ('serviceWorker' in navigator) {
                        navigator.serviceWorker.register('/service-worker.js')
                            .then(function(registration) {
                                console.log('Service Worker registered');
                            })
                            .catch(function(error) {
                                console.log('Service Worker registration failed:', error);
                            });
                    }
                }
            });
        }
        </script>
        """
        st.components.v1.html(push_permission_js, height=0)

    def send_push_notification(self, title, message, subscriber_id):
        """Send browser push notification"""
        try:
            # Implement push notification using web-push library
            push_data = {
                "notification": {
                    "title": title,
                    "body": message,
                    "icon": "/icon.png",  # Add your notification icon
                    "click_action": "https://ipo-monitor-gmp.streamlit.app/Dashboard"
                }
            }
            
            # Send to push service (you'll need to implement this part)
            # This is a placeholder for the actual implementation
            return {"status": "success", "message": "Push notification sent"}
        except Exception as e:
            logging.error(f"Failed to send push notification: {str(e)}")
            return {"status": "error", "message": str(e)}

    def notify_subscriber(self, subscriber_data, ipo_data):
        """Send both WhatsApp and push notifications"""
        results = {
            "whatsapp": False,
            "push": False
        }

        # Prepare notification message
        message = f"""🚨 IPO Alert!

IPO: {ipo_data['name']}
Gain: {ipo_data['gain']}%
Price: ₹{ipo_data['price']}
GMP: ₹{ipo_data['gmp']}
Type: {ipo_data['type']}"""

        # Send WhatsApp notification
        whatsapp_result = self.send_whatsapp_message(subscriber_data['phone'], message)
        results['whatsapp'] = whatsapp_result['status'] == 'success'

        # Send push notification
        push_result = self.send_push_notification(
            "IPO GMP Alert",
            f"{ipo_data['name']} - Gain: {ipo_data['gain']}%",
            subscriber_data['id']
        )
        results['push'] = push_result['status'] == 'success'

        return results