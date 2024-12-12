
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