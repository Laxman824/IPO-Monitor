# utils/database.py
import sqlite3
import pandas as pd
from config.config import Config

class Database:
    def __init__(self):
        self.db_path = Config.DATABASE_PATH

    def setup_database(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS subscribers
                    (phone TEXT PRIMARY KEY,
                     name TEXT,
                     gain_threshold INTEGER DEFAULT 50,
                     active BOOLEAN DEFAULT 1)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS sent_alerts
                    (ipo_name TEXT,
                     phone TEXT,
                     date TEXT,
                     PRIMARY KEY (ipo_name, phone, date))''')
        
        conn.commit()
        conn.close()

    def add_subscriber(self, phone, name, threshold=50):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO subscribers VALUES (?, ?, ?, 1)',
                 (phone, name, threshold))
        conn.commit()
        conn.close()

    def get_subscribers(self):
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM subscribers WHERE active = 1", conn)
        conn.close()
        return df

    def deactivate_subscriber(self, phone):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('UPDATE subscribers SET active = 0 WHERE phone = ?', (phone,))
        conn.commit()
        conn.close()
