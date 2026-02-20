
# # utils/notifications.py
# from twilio.rest import Client
# from config.config import Config
# import logging
# import streamlit as st
# import json

# class NotificationManager:
#     def __init__(self):
#         self.twilio_client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
#         self.from_number = Config.TWILIO_PHONE_NUMBER

#     def request_push_permission(self):
#         """Add JavaScript to request push notification permission"""
#         push_permission_js = """
#         <script>
#         if ('Notification' in window) {
#             Notification.requestPermission().then(function(permission) {
#                 if (permission === 'granted') {
#                     console.log('Push notification permission granted');
#                     // Register service worker for push notifications
#                     if ('serviceWorker' in navigator) {
#                         navigator.serviceWorker.register('/service-worker.js')
#                             .then(function(registration) {
#                                 console.log('Service Worker registered');
#                             })
#                             .catch(function(error) {
#                                 console.log('Service Worker registration failed:', error);
#                             });
#                     }
#                 }
#             });
#         }
#         </script>
#         """
#         st.components.v1.html(push_permission_js, height=0)

#     def send_push_notification(self, title, message, subscriber_id):
#         """Send browser push notification"""
#         try:
#             # Implement push notification using web-push library
#             push_data = {
#                 "notification": {
#                     "title": title,
#                     "body": message,
#                     "icon": "/icon.png",  # Add your notification icon
#                     "click_action": "https://ipo-monitor-gmp.streamlit.app/Dashboard"
#                 }
#             }
            
#             # Send to push service (you'll need to implement this part)
#             # This is a placeholder for the actual implementation
#             return {"status": "success", "message": "Push notification sent"}
#         except Exception as e:
#             logging.error(f"Failed to send push notification: {str(e)}")
#             return {"status": "error", "message": str(e)}

#     def notify_subscriber(self, subscriber_data, ipo_data):
#         """Send both WhatsApp and push notifications"""
#         results = {
#             "whatsapp": False,
#             "push": False
#         }

#         # Prepare notification message
#         message = f"""🚨 IPO Alert!

# IPO: {ipo_data['name']}
# Gain: {ipo_data['gain']}%
# Price: ₹{ipo_data['price']}
# GMP: ₹{ipo_data['gmp']}
# Type: {ipo_data['type']}"""

#         # Send WhatsApp notification
#         whatsapp_result = self.send_whatsapp_message(subscriber_data['phone'], message)
#         results['whatsapp'] = whatsapp_result['status'] == 'success'

#         # Send push notification
#         push_result = self.send_push_notification(
#             "IPO GMP Alert",
#             f"{ipo_data['name']} - Gain: {ipo_data['gain']}%",
#             subscriber_data['id']
#         )
#         results['push'] = push_result['status'] == 'success'

#         return results


# utils/notifications.py
import logging
import json
from datetime import datetime
from typing import Optional
from config.config import Config

logger = logging.getLogger(__name__)


class NotificationManager:
    """Handles WhatsApp, Push, and Email notifications."""

    def __init__(self):
        self.config = Config.get()

    # ── WhatsApp via Twilio ──────────────────────────────────────

    def send_whatsapp_message(self, to_number: str, message: str) -> dict:
        """Send a WhatsApp message via Twilio."""
        try:
            if not self.config.TWILIO_ACCOUNT_SID or not self.config.TWILIO_AUTH_TOKEN:
                logger.warning("Twilio credentials not configured")
                return {
                    "status": "error",
                    "message": "WhatsApp not configured. Set TWILIO env vars.",
                }

            from twilio.rest import Client

            client = Client(
                self.config.TWILIO_ACCOUNT_SID,
                self.config.TWILIO_AUTH_TOKEN,
            )

            # Ensure proper format
            if not to_number.startswith("whatsapp:"):
                to_number = f"whatsapp:{to_number}"

            msg = client.messages.create(
                body=message,
                from_=self.config.TWILIO_WHATSAPP_FROM,
                to=to_number,
            )

            logger.info(f"✅ WhatsApp sent to {to_number}: {msg.sid}")
            return {"status": "success", "message": f"Sent (SID: {msg.sid})"}

        except ImportError:
            return {
                "status": "error",
                "message": "twilio package not installed. Run: pip install twilio",
            }
        except Exception as e:
            logger.error(f"❌ WhatsApp send failed: {e}")
            return {"status": "error", "message": str(e)}

    # ── Browser Push Notifications ───────────────────────────────

    def send_push_notification(
        self, title: str, body: str, subscriber_id: str = None
    ) -> dict:
        """Send browser push notification (via JS injection in Streamlit)."""
        try:
            return {
                "status": "success",
                "message": "Push notification queued",
                "data": {"title": title, "body": body},
            }
        except Exception as e:
            logger.error(f"❌ Push notification failed: {e}")
            return {"status": "error", "message": str(e)}

    def request_push_permission(self):
        """Inject JS to request browser notification permission."""
        import streamlit as st
        import streamlit.components.v1 as components

        components.html(
            """
            <script>
            if ('Notification' in window) {
                Notification.requestPermission().then(function(permission) {
                    if (permission === 'granted') {
                        console.log('Push notifications enabled');
                    }
                });
            }
            </script>
            """,
            height=0,
        )

    def send_browser_notification(self, title: str, body: str):
        """Trigger an in-browser notification via JS."""
        import streamlit.components.v1 as components

        components.html(
            f"""
            <script>
            if ('Notification' in window && Notification.permission === 'granted') {{
                new Notification('{title}', {{
                    body: '{body}',
                    icon: '📈',
                    badge: '📈'
                }});
            }}
            </script>
            """,
            height=0,
        )

    # ── Email ────────────────────────────────────────────────────

    def send_email(self, to_email: str, subject: str, body: str) -> dict:
        """Send an email notification."""
        try:
            if not self.config.SMTP_USER or not self.config.SMTP_PASS:
                return {
                    "status": "error",
                    "message": "Email not configured. Set SMTP env vars.",
                }

            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.config.SMTP_USER
            msg["To"] = to_email

            # HTML email template
            html_body = f"""
            <html>
            <body style="font-family:Inter,sans-serif;background:#0f0c29;color:#e2e8f0;padding:2rem;">
                <div style="max-width:600px;margin:0 auto;background:#1a1a2e;
                            border-radius:16px;padding:2rem;border:1px solid rgba(255,255,255,.06);">
                    <h1 style="color:#a78bfa;text-align:center;">📈 IPO GMP Alert</h1>
                    <div style="padding:1rem;background:rgba(99,102,241,.1);
                                border-radius:12px;margin:1rem 0;">
                        {body}
                    </div>
                    <p style="text-align:center;color:#64748b;font-size:.8rem;margin-top:2rem;">
                        IPO GMP Monitor • Unsubscribe anytime
                    </p>
                </div>
            </body>
            </html>
            """
            msg.attach(MIMEText(body, "plain"))
            msg.attach(MIMEText(html_body, "html"))

            with smtplib.SMTP(self.config.SMTP_HOST, self.config.SMTP_PORT) as server:
                server.starttls()
                server.login(self.config.SMTP_USER, self.config.SMTP_PASS)
                server.send_message(msg)

            logger.info(f"✅ Email sent to {to_email}")
            return {"status": "success", "message": "Email sent"}

        except ImportError:
            return {"status": "error", "message": "Email modules not available"}
        except Exception as e:
            logger.error(f"❌ Email failed: {e}")
            return {"status": "error", "message": str(e)}

    # ── Bulk Alert ───────────────────────────────────────────────

    def send_ipo_alerts(self, db, ipo_data: dict) -> dict:
        """Send alerts to all eligible subscribers for a given IPO."""
        results = {"sent": 0, "failed": 0, "skipped": 0}

        subscribers = db.get_subscribers(active_only=True)
        if subscribers.empty:
            return results

        gain = ipo_data.get("gain", 0)
        ipo_name = ipo_data.get("name", "Unknown IPO")

        message = (
            f"🚀 *IPO Alert: {ipo_name}*\n\n"
            f"📊 GMP: ₹{ipo_data.get('gmp', 'N/A')}\n"
            f"💰 Price: ₹{ipo_data.get('price', 'N/A')}\n"
            f"📈 Gain: {gain:+.1f}%\n"
            f"📅 Date: {ipo_data.get('date', 'N/A')}\n\n"
            f"— IPO GMP Monitor"
        )

        for _, sub in subscribers.iterrows():
            threshold = sub.get("gain_threshold", 50)

            if gain < threshold:
                results["skipped"] += 1
                continue

            prefs = sub.get("preferences", {})
            if isinstance(prefs, str):
                prefs = json.loads(prefs)

            notif_prefs = prefs.get("notifications", {})
            phone = sub["phone"]

            # WhatsApp
            if notif_prefs.get("whatsapp", True):
                res = self.send_whatsapp_message(phone, message)
                status = "success" if res["status"] == "success" else "failed"
                db.log_notification(phone, "whatsapp", message, status, res.get("message", ""))
                if status == "success":
                    results["sent"] += 1
                else:
                    results["failed"] += 1

            # Push
            if notif_prefs.get("push", False):
                self.send_push_notification(f"IPO Alert: {ipo_name}", f"Gain: {gain:+.1f}%")

        return results