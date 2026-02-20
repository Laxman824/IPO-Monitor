
# # config/config.py
# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     # Twilio settings
#     TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
#     TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
#     TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
#     OWNER_WHATSAPP_NUMBER = os.getenv('OWNER_WHATSAPP_NUMBER')
    
#     # Database settings
#     DATABASE_PATH = 'ipo_monitor.db'
    
#     # IPO settings
#     IPO_URL = "https://ipowatch.in/ipo-grey-market-premium-latest-ipo-gmp/"
#     REFRESH_INTERVAL = 60  # seconds
    
#     # Alert settings
#     DEFAULT_GAIN_THRESHOLD = 50
#     MAX_DAILY_ALERTS = 10


# config/config.py
import os
from dataclasses import dataclass, field
from typing import List


@dataclass
class Config:
    """Centralized application configuration"""

    # ── Scraper ──────────────────────────────────────────────────
    IPO_URL: str = "https://ipowatch.in/ipo-grey-market-premium-latest-ipo-gmp/"
    FALLBACK_URLS: List[str] = field(default_factory=lambda: [
        "https://ipowatch.in/ipo-grey-market-premium-latest-ipo-gmp/",
        "https://www.investorgain.com/report/live-ipo-gmp/331/",
    ])

    REQUEST_TIMEOUT: int = 5  # Reduced timeout for faster failure
    MAX_RETRIES: int = 3
    RETRY_DELAY: float = 2.0  # seconds (doubles each retry)

    USER_AGENTS: List[str] = field(default_factory=lambda: [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
        "(KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    ])

    # ── Database ─────────────────────────────────────────────────
    DB_PATH: str = "ipo_monitor.db"

    # ── Notifications ────────────────────────────────────────────
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_WHATSAPP_FROM: str = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")

    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASS: str = os.getenv("SMTP_PASS", "")

    # ── App ──────────────────────────────────────────────────────
    APP_NAME: str = "IPO GMP Monitor"
    APP_VERSION: str = "2.0.0"
    CACHE_TTL: int = 300  # 5 minutes
    DEFAULT_GAIN_THRESHOLD: int = 50

    @classmethod
    def get(cls):
        """Return a singleton config instance"""
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance