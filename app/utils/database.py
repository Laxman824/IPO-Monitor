
# utils/database.py
import sqlite3
import pandas as pd
import json
from datetime import datetime
import logging

class Database:
    def __init__(self):
        self.db_path = 'ipo_monitor.db'
        self._setup_database()
        
    def _setup_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS subscribers
                    (phone TEXT PRIMARY KEY,
                     name TEXT NOT NULL,
                     gain_threshold INTEGER DEFAULT 50,
                     preferences TEXT,
                     active BOOLEAN DEFAULT 1,
                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
                     
        conn.commit()
        conn.close()
        
    def add_subscriber(self, phone, name, threshold=50, preferences=None):
        """Add a new subscriber"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            preferences_json = json.dumps(preferences) if preferences else '{}'
            
            c.execute('''INSERT OR REPLACE INTO subscribers 
                        (phone, name, gain_threshold, preferences, active, updated_at)
                        VALUES (?, ?, ?, ?, 1, ?)''',
                     (phone, name, threshold, preferences_json, datetime.now()))
            
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"Failed to add subscriber: {str(e)}")
            return False
        finally:
            conn.close()
            
    def get_subscribers(self, active_only=True):
        """Get list of subscribers"""
        conn = sqlite3.connect(self.db_path)
        query = "SELECT * FROM subscribers"
        if active_only:
            query += " WHERE active = 1"
            
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty and 'preferences' in df.columns:
            df['preferences'] = df['preferences'].apply(
                lambda x: json.loads(x) if x else {})
        return df
        
    def deactivate_subscriber(self, phone):
        """Deactivate a subscriber"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            c.execute('''UPDATE subscribers 
                        SET active = 0, 
                            updated_at = ? 
                        WHERE phone = ?''', 
                     (datetime.now(), phone))
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"Failed to deactivate subscriber: {str(e)}")
            return False
        finally:
            conn.close()