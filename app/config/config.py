import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
    DATABASE_PATH = 'ipo_monitor.db'
    IPO_URL = "https://ipowatch.in/ipo-grey-market-premium-latest-ipo-gmp/"
    REFRESH_INTERVAL = 60  # seconds