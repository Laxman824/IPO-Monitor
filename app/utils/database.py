# # utils/database.py
# import sqlite3
# import pandas as pd
# import json
# from datetime import datetime
# from config.config import Config

# class Database:
#     def __init__(self):
#         self.db_path = Config.DATABASE_PATH
#         self.setup_database()

#     def setup_database(self):
#         """Initialize database tables"""
#         conn = sqlite3.connect(self.db_path)
#         c = conn.cursor()
        
#         # Subscribers table with enhanced fields
#         c.execute('''CREATE TABLE IF NOT EXISTS subscribers (
#             phone TEXT PRIMARY KEY,
#             name TEXT NOT NULL,
#             gain_threshold INTEGER DEFAULT 50,
#             preferences TEXT,
#             active BOOLEAN DEFAULT 1,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             last_notified TIMESTAMP,
#             notification_count INTEGER DEFAULT 0
#         )''')
        
#         # Sent alerts history
#         c.execute('''CREATE TABLE IF NOT EXISTS sent_alerts (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             ipo_name TEXT NOT NULL,
#             phone TEXT NOT NULL,
#             alert_type TEXT NOT NULL,
#             alert_message TEXT,
#             gain_percentage REAL,
#             sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             status TEXT,
#             FOREIGN KEY (phone) REFERENCES subscribers(phone)
#         )''')
        
#         # IPO tracking table
#         c.execute('''CREATE TABLE IF NOT EXISTS ipo_tracking (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             ipo_name TEXT NOT NULL,
#             current_gmp INTEGER,
#             previous_gmp INTEGER,
#             gain_percentage REAL,
#             last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             status TEXT DEFAULT 'active'
#         )''')
        
#         # System logs
#         c.execute('''CREATE TABLE IF NOT EXISTS system_logs (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             log_type TEXT NOT NULL,
#             message TEXT NOT NULL,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         )''')
        
#         conn.commit()
#         conn.close()

#     def add_subscriber(self, phone, name, threshold=50, preferences=None):
#         """Add or update a subscriber"""
#         conn = sqlite3.connect(self.db_path)
#         c = conn.cursor()
#         try:
#             preferences_json = json.dumps(preferences) if preferences else '{}'
            
#             c.execute('''INSERT OR REPLACE INTO subscribers 
#                         (phone, name, gain_threshold, preferences, active, updated_at)
#                         VALUES (?, ?, ?, ?, 1, ?)''',
#                      (phone, name, threshold, preferences_json, datetime.now()))
            
#             self.log_activity('INFO', f'Added/Updated subscriber: {name} ({phone})')
#             conn.commit()
#             return True
#         except Exception as e:
#             self.log_activity('ERROR', f'Failed to add subscriber: {str(e)}')
#             return False
#         finally:
#             conn.close()

#     def get_subscribers(self, active_only=True):
#         """Get subscriber list with optional filtering"""
#         conn = sqlite3.connect(self.db_path)
#         query = "SELECT * FROM subscribers"
#         if active_only:
#             query += " WHERE active = 1"
#         df = pd.read_sql_query(query, conn)
#         conn.close()
        
#         if not df.empty and 'preferences' in df.columns:
#             df['preferences'] = df['preferences'].apply(
#                 lambda x: json.loads(x) if x else {})
#         return df

#     def update_subscriber_status(self, phone, active=True):
#         """Activate or deactivate a subscriber"""
#         conn = sqlite3.connect(self.db_path)
#         c = conn.cursor()
#         try:
#             c.execute('''UPDATE subscribers 
#                         SET active = ?, updated_at = ? 
#                         WHERE phone = ?''', 
#                      (active, datetime.now(), phone))
            
#             status = "activated" if active else "deactivated"
#             self.log_activity('INFO', f'Subscriber {phone} {status}')
#             conn.commit()
#             return True
#         except Exception as e:
#             self.log_activity('ERROR', f'Failed to update subscriber status: {str(e)}')
#             return False
#         finally:
#             conn.close()

#     def record_alert(self, ipo_name, phone, alert_type, message, gain_percentage):
#         """Record a sent alert"""
#         conn = sqlite3.connect(self.db_path)
#         c = conn.cursor()
#         try:
#             c.execute('''INSERT INTO sent_alerts 
#                         (ipo_name, phone, alert_type, alert_message, gain_percentage, status)
#                         VALUES (?, ?, ?, ?, ?, ?)''',
#                      (ipo_name, phone, alert_type, message, gain_percentage, 'sent'))
            
#             # Update subscriber's notification count and last_notified
#             c.execute('''UPDATE subscribers 
#                         SET notification_count = notification_count + 1,
#                             last_notified = ?
#                         WHERE phone = ?''',
#                      (datetime.now(), phone))
            
#             conn.commit()
#             return True
#         except Exception as e:
#             self.log_activity('ERROR', f'Failed to record alert: {str(e)}')
#             return False
#         finally:
#             conn.close()

#     def update_ipo_tracking(self, ipo_data):
#         """Update IPO tracking information"""
#         conn = sqlite3.connect(self.db_path)
#         c = conn.cursor()
#         try:
#             for ipo in ipo_data:
#                 # Get previous GMP
#                 c.execute('''SELECT current_gmp 
#                            FROM ipo_tracking 
#                            WHERE ipo_name = ? 
#                            ORDER BY last_updated DESC LIMIT 1''',
#                         (ipo['name'],))
#                 result = c.fetchone()
#                 previous_gmp = result[0] if result else None

#                 # Insert new tracking record
#                 c.execute('''INSERT INTO ipo_tracking 
#                            (ipo_name, current_gmp, previous_gmp, gain_percentage)
#                            VALUES (?, ?, ?, ?)''',
#                         (ipo['name'], ipo['gmp'], previous_gmp, ipo['gain']))
            
#             conn.commit()
#             return True
#         except Exception as e:
#             self.log_activity('ERROR', f'Failed to update IPO tracking: {str(e)}')
#             return False
#         finally:
#             conn.close()

#     def get_alert_history(self, days=7):
#         """Get alert history for the last n days"""
#         conn = sqlite3.connect(self.db_path)
#         query = f'''
#             SELECT * FROM sent_alerts 
#             WHERE sent_at >= date('now', '-{days} days')
#             ORDER BY sent_at DESC
#         '''
#         df = pd.read_sql_query(query, conn)
#         conn.close()
#         return df

#     def get_ipo_trends(self, ipo_name=None):
#         """Get IPO GMP trends"""
#         conn = sqlite3.connect(self.db_path)
#         query = '''SELECT * FROM ipo_tracking'''
#         if ipo_name:
#             query += f" WHERE ipo_name = '{ipo_name}'"
#         query += " ORDER BY last_updated DESC"
        
#         df = pd.read_sql_query(query, conn)
#         conn.close()
#         return df

#     def log_activity(self, log_type, message):
#         """Log system activity"""
#         conn = sqlite3.connect(self.db_path)
#         c = conn.cursor()
#         try:
#             c.execute('''INSERT INTO system_logs (log_type, message)
#                         VALUES (?, ?)''', (log_type, message))
#             conn.commit()
#         except Exception as e:
#             print(f"Failed to log activity: {str(e)}")
#         finally:
#             conn.close()

#     def get_system_logs(self, limit=100):
#         """Get recent system logs"""
#         conn = sqlite3.connect(self.db_path)
#         query = f'''SELECT * FROM system_logs 
#                    ORDER BY created_at DESC 
#                    LIMIT {limit}'''
#         df = pd.read_sql_query(query, conn)
#         conn.close()
#         return df

#     def get_subscriber_stats(self):
#         """Get subscriber statistics"""
#         conn = sqlite3.connect(self.db_path)
#         stats = {}
        
#         c = conn.cursor()
#         c.execute("SELECT COUNT(*) FROM subscribers WHERE active = 1")
#         stats['active_subscribers'] = c.fetchone()[0]
        
#         c.execute("SELECT COUNT(*) FROM subscribers WHERE active = 0")
#         stats['inactive_subscribers'] = c.fetchone()[0]
        
#         c.execute("SELECT COUNT(*) FROM sent_alerts WHERE date(sent_at) = date('now')")
#         stats['alerts_today'] = c.fetchone()[0]
        
#         conn.close()
#         return stats
# # utils/database.py (add these methods)

# class Database:
#     def add_pending_subscriber(self, phone, name, preferences):
#         """Add subscriber in pending state"""
#         conn = sqlite3.connect(self.db_path)
#         c = conn.cursor()
#         try:
#             c.execute('''INSERT INTO subscribers 
#                         (phone, name, gain_threshold, preferences, status)
#                         VALUES (?, ?, ?, ?, 'pending')''',
#                      (phone, name, preferences['gain_threshold'], 
#                       json.dumps(preferences)))
#             conn.commit()
#             return True
#         except Exception as e:
#             print(f"Error adding pending subscriber: {str(e)}")
#             return False
#         finally:
#             conn.close()

#     def approve_subscriber(self, phone):
#         """Approve a pending subscriber"""
#         conn = sqlite3.connect(self.db_path)
#         c = conn.cursor()
#         try:
#             c.execute('''UPDATE subscribers 
#                         SET status = 'active', 
#                             approved_at = CURRENT_TIMESTAMP
#                         WHERE phone = ?''', (phone,))
#             conn.commit()
#             return True
#         except Exception as e:
#             print(f"Error approving subscriber: {str(e)}")
#             return False
#         finally:
#             conn.close()





# utils/database.py
import sqlite3
import pandas as pd
import json
from datetime import datetime
from config.config import Config

class Database:
    def __init__(self):
        self.db_path = Config.DATABASE_PATH
        self._setup_database()  # Call setup during initialization

    def _setup_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Create subscribers table
        c.execute('''CREATE TABLE IF NOT EXISTS subscribers
                    (phone TEXT PRIMARY KEY,
                     name TEXT NOT NULL,
                     gain_threshold INTEGER DEFAULT 50,
                     preferences TEXT,
                     status TEXT DEFAULT 'pending',
                     active BOOLEAN DEFAULT 1,
                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     approved_at TIMESTAMP,
                     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     last_notified TIMESTAMP,
                     notification_count INTEGER DEFAULT 0)''')
        
        # Create sent_alerts table
        c.execute('''CREATE TABLE IF NOT EXISTS sent_alerts
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     ipo_name TEXT NOT NULL,
                     phone TEXT NOT NULL,
                     alert_type TEXT NOT NULL,
                     alert_message TEXT,
                     gain_percentage REAL,
                     sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     status TEXT,
                     FOREIGN KEY (phone) REFERENCES subscribers(phone))''')
        
        # Create IPO tracking table
        c.execute('''CREATE TABLE IF NOT EXISTS ipo_tracking
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     ipo_name TEXT NOT NULL,
                     current_gmp INTEGER,
                     previous_gmp INTEGER,
                     gain_percentage REAL,
                     last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     status TEXT DEFAULT 'active')''')
        
        # Create system logs table
        c.execute('''CREATE TABLE IF NOT EXISTS system_logs
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     log_type TEXT NOT NULL,
                     message TEXT NOT NULL,
                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        
        conn.commit()
        conn.close()

    def add_subscriber(self, phone, name, threshold=50, preferences=None):
        """Add or update a subscriber"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            preferences_json = json.dumps(preferences) if preferences else '{}'
            
            c.execute('''INSERT OR REPLACE INTO subscribers 
                        (phone, name, gain_threshold, preferences, status, active, updated_at)
                        VALUES (?, ?, ?, ?, 'pending', 1, ?)''',
                     (phone, name, threshold, preferences_json, datetime.now()))
            
            self.log_activity('INFO', f'Added/Updated subscriber: {name} ({phone})')
            conn.commit()
            return True
        except Exception as e:
            self.log_activity('ERROR', f'Failed to add subscriber: {str(e)}')
            return False
        finally:
            conn.close()

    def get_subscribers(self, status=None, active_only=True):
        """Get subscriber list with optional filtering"""
        conn = sqlite3.connect(self.db_path)
        query = "SELECT * FROM subscribers WHERE 1=1"
        if active_only:
            query += " AND active = 1"
        if status:
            query += f" AND status = '{status}'"
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty and 'preferences' in df.columns:
            df['preferences'] = df['preferences'].apply(
                lambda x: json.loads(x) if x else {})
        return df

    def approve_subscriber(self, phone):
        """Approve a pending subscriber"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            c.execute('''UPDATE subscribers 
                        SET status = 'active',
                            approved_at = ?,
                            updated_at = ?
                        WHERE phone = ?''',
                     (datetime.now(), datetime.now(), phone))
            
            self.log_activity('INFO', f'Subscriber approved: {phone}')
            conn.commit()
            return True
        except Exception as e:
            self.log_activity('ERROR', f'Failed to approve subscriber: {str(e)}')
            return False
        finally:
            conn.close()

    def log_activity(self, log_type, message):
        """Log system activity"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            c.execute('''INSERT INTO system_logs (log_type, message)
                        VALUES (?, ?)''', (log_type, message))
            conn.commit()
        except Exception as e:
            print(f"Failed to log activity: {str(e)}")
        finally:
            conn.close()

    def get_system_logs(self, limit=100):
        """Get recent system logs"""
        conn = sqlite3.connect(self.db_path)
        query = f'''SELECT * FROM system_logs 
                   ORDER BY created_at DESC 
                   LIMIT {limit}'''
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df