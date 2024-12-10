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
#  
# utils/notifications.py
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import telegram
import discord_webhook
import requests
from config.config import Config
import asyncio
import aiohttp

class NotificationManager:
    def __init__(self):
        # Twilio setup
        self.twilio_client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
        self.twilio_number = Config.TWILIO_PHONE_NUMBER
        
        # Telegram setup
        self.telegram_bot = telegram.Bot(token=Config.TELEGRAM_BOT_TOKEN)
        
        # Discord setup
        self.discord_webhook_url = Config.DISCORD_WEBHOOK_URL
        
        # Pushbullet setup
        self.pushbullet_api_key = Config.PUSHBULLET_API_KEY

    async def send_telegram_message(self, chat_id, message):
        """Send message via Telegram"""
        try:
            await self.telegram_bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')
            return True
        except Exception as e:
            print(f"Telegram error: {str(e)}")
            return False

    def send_discord_message(self, message):
        """Send message via Discord webhook"""
        try:
            webhook = discord_webhook.DiscordWebhook(url=self.discord_webhook_url, content=message)
            webhook.execute()
            return True
        except Exception as e:
            print(f"Discord error: {str(e)}")
            return False

    def send_pushbullet_notification(self, title, message):
        """Send notification via Pushbullet"""
        try:
            headers = {
                'Access-Token': self.pushbullet_api_key,
                'Content-Type': 'application/json'
            }
            data = {
                'type': 'note',
                'title': title,
                'body': message
            }
            response = requests.post(
                'https://api.pushbullet.com/v2/pushes',
                headers=headers,
                json=data
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Pushbullet error: {str(e)}")
            return False

    def send_whatsapp_message(self, to_number, message):
        """Send a WhatsApp message using Twilio"""
        try:
            from_number = f'whatsapp:{self.twilio_number}' if not self.twilio_number.startswith('whatsapp:') else self.twilio_number
            to_number = f'whatsapp:{to_number}' if not to_number.startswith('whatsapp:') else to_number

            message = self.twilio_client.messages.create(
                from_=from_number,
                body=message,
                to=to_number
            )
            return True
        except Exception as e:
            print(f"WhatsApp error: {str(e)}")
            return False

    async def send_notification(self, message, notification_methods, user_info):
        """Send notification through multiple channels"""
        results = []
        
        if 'whatsapp' in notification_methods and user_info.get('phone'):
            results.append(('WhatsApp', self.send_whatsapp_message(user_info['phone'], message)))
            
        if 'telegram' in notification_methods and user_info.get('telegram_chat_id'):
            results.append(('Telegram', await self.send_telegram_message(user_info['telegram_chat_id'], message)))
            
        if 'discord' in notification_methods and user_info.get('discord_webhook'):
            results.append(('Discord', self.send_discord_message(message)))
            
        if 'pushbullet' in notification_methods and user_info.get('pushbullet_email'):
            results.append(('Pushbullet', self.send_pushbullet_notification("IPO Alert", message)))
            
        return results

    def test_connections(self):
        """Test all notification connections"""
        results = {
            'whatsapp': False,
            'telegram': False,
            'discord': False,
            'pushbullet': False
        }
        
        try:
            # Test Twilio
            account = self.twilio_client.api.accounts(Config.TWILIO_ACCOUNT_SID).fetch()
            results['whatsapp'] = True
        except:
            pass

        try:
            # Test Telegram
            asyncio.run(self.telegram_bot.get_me())
            results['telegram'] = True
        except:
            pass

        try:
            # Test Discord
            webhook = discord_webhook.DiscordWebhook(url=self.discord_webhook_url, content="Test")
            webhook.execute()
            results['discord'] = True
        except:
            pass

        try:
            # Test Pushbullet
            headers = {'Access-Token': self.pushbullet_api_key}
            response = requests.get('https://api.pushbullet.com/v2/users/me', headers=headers)
            results['pushbullet'] = response.status_code == 200
        except:
            pass

        return results