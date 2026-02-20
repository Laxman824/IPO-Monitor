
# # utils/database.py
# import sqlite3
# import pandas as pd
# import json
# from datetime import datetime
# import logging

# class Database:
#     def __init__(self):
#         self.db_path = 'ipo_monitor.db'
#         self._setup_database()
        
#     def _setup_database(self):
#         """Initialize database tables"""
#         conn = sqlite3.connect(self.db_path)
#         c = conn.cursor()
        
#         c.execute('''CREATE TABLE IF NOT EXISTS subscribers
#                     (phone TEXT PRIMARY KEY,
#                      name TEXT NOT NULL,
#                      gain_threshold INTEGER DEFAULT 50,
#                      preferences TEXT,
#                      active BOOLEAN DEFAULT 1,
#                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
                     
#         conn.commit()
#         conn.close()
        
#     def add_subscriber(self, phone, name, threshold=50, preferences=None):
#         """Add a new subscriber"""
#         conn = sqlite3.connect(self.db_path)
#         c = conn.cursor()
#         try:
#             preferences_json = json.dumps(preferences) if preferences else '{}'
            
#             c.execute('''INSERT OR REPLACE INTO subscribers 
#                         (phone, name, gain_threshold, preferences, active, updated_at)
#                         VALUES (?, ?, ?, ?, 1, ?)''',
#                      (phone, name, threshold, preferences_json, datetime.now()))
            
#             conn.commit()
#             return True
#         except Exception as e:
#             logging.error(f"Failed to add subscriber: {str(e)}")
#             return False
#         finally:
#             conn.close()
            
#     def get_subscribers(self, active_only=True):
#         """Get list of subscribers"""
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
        
#     def deactivate_subscriber(self, phone):
#         """Deactivate a subscriber"""
#         conn = sqlite3.connect(self.db_path)
#         c = conn.cursor()
#         try:
#             c.execute('''UPDATE subscribers 
#                         SET active = 0, 
#                             updated_at = ? 
#                         WHERE phone = ?''', 
#                      (datetime.now(), phone))
#             conn.commit()
#             return True
#         except Exception as e:
#             logging.error(f"Failed to deactivate subscriber: {str(e)}")
#             return False
#         finally:
#             conn.close()

# utils/database.py
import sqlite3
import pandas as pd
import json
from datetime import datetime
from contextlib import contextmanager
import logging
from config.config import Config

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or Config.get().DB_PATH
        self._setup_database()

    @contextmanager
    def _get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _setup_database(self):
        """Initialize all database tables."""
        with self._get_connection() as conn:
            c = conn.cursor()

            # Subscribers table
            c.execute("""
                CREATE TABLE IF NOT EXISTS subscribers (
                    phone TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT DEFAULT '',
                    gain_threshold INTEGER DEFAULT 50,
                    preferences TEXT DEFAULT '{}',
                    active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # IPO history for tracking over time
            c.execute("""
                CREATE TABLE IF NOT EXISTS ipo_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ipo_name TEXT NOT NULL,
                    gmp REAL DEFAULT 0,
                    price REAL DEFAULT 0,
                    gain REAL DEFAULT 0,
                    ipo_type TEXT DEFAULT 'Mainline',
                    date_range TEXT DEFAULT '',
                    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Notification log
            c.execute("""
                CREATE TABLE IF NOT EXISTS notification_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone TEXT,
                    channel TEXT DEFAULT 'whatsapp',
                    message TEXT,
                    status TEXT DEFAULT 'pending',
                    error_message TEXT DEFAULT '',
                    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (phone) REFERENCES subscribers(phone)
                )
            """)

            # App settings
            c.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            logger.info("✅ Database tables initialized")

    # ── Subscribers ──────────────────────────────────────────────

    def add_subscriber(self, phone, name, threshold=50, preferences=None, email=""):
        """Add or update a subscriber."""
        with self._get_connection() as conn:
            try:
                prefs_json = json.dumps(preferences) if preferences else "{}"
                conn.execute(
                    """INSERT OR REPLACE INTO subscribers
                       (phone, name, email, gain_threshold, preferences, active, updated_at)
                       VALUES (?, ?, ?, ?, ?, 1, ?)""",
                    (phone, name, email, threshold, prefs_json, datetime.now()),
                )
                logger.info(f"✅ Subscriber added/updated: {phone}")
                return True
            except Exception as e:
                logger.error(f"❌ Failed to add subscriber: {e}")
                return False

    def get_subscribers(self, active_only=True) -> pd.DataFrame:
        """Get subscribers as DataFrame."""
        with self._get_connection() as conn:
            query = "SELECT * FROM subscribers"
            if active_only:
                query += " WHERE active = 1"
            query += " ORDER BY created_at DESC"

            df = pd.read_sql_query(query, conn)

        if not df.empty and "preferences" in df.columns:
            df["preferences"] = df["preferences"].apply(
                lambda x: json.loads(x) if x else {}
            )
        return df

    def get_subscriber(self, phone) -> dict:
        """Get a single subscriber by phone."""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM subscribers WHERE phone = ?", (phone,)
            ).fetchone()
            if row:
                d = dict(row)
                d["preferences"] = json.loads(d.get("preferences", "{}"))
                return d
        return {}

    def update_subscriber(self, phone, **kwargs):
        """Update subscriber fields."""
        allowed = {"name", "email", "gain_threshold", "preferences", "active"}
        updates = {k: v for k, v in kwargs.items() if k in allowed}

        if not updates:
            return False

        if "preferences" in updates and isinstance(updates["preferences"], dict):
            updates["preferences"] = json.dumps(updates["preferences"])

        updates["updated_at"] = datetime.now()
        set_clause = ", ".join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [phone]

        with self._get_connection() as conn:
            try:
                conn.execute(
                    f"UPDATE subscribers SET {set_clause} WHERE phone = ?", values
                )
                return True
            except Exception as e:
                logger.error(f"❌ Update failed: {e}")
                return False

    def deactivate_subscriber(self, phone):
        """Deactivate a subscriber (soft delete)."""
        return self.update_subscriber(phone, active=0)

    def activate_subscriber(self, phone):
        """Re-activate a subscriber."""
        return self.update_subscriber(phone, active=1)

    def delete_subscriber(self, phone):
        """Hard delete a subscriber."""
        with self._get_connection() as conn:
            try:
                conn.execute("DELETE FROM subscribers WHERE phone = ?", (phone,))
                return True
            except Exception as e:
                logger.error(f"❌ Delete failed: {e}")
                return False

    def get_subscriber_count(self) -> dict:
        """Get subscriber statistics."""
        with self._get_connection() as conn:
            total = conn.execute("SELECT COUNT(*) FROM subscribers").fetchone()[0]
            active = conn.execute(
                "SELECT COUNT(*) FROM subscribers WHERE active = 1"
            ).fetchone()[0]
        return {"total": total, "active": active, "inactive": total - active}

    # ── IPO History ──────────────────────────────────────────────

    def save_ipo_snapshot(self, df: pd.DataFrame):
        """Save current IPO data as a historical snapshot."""
        if df is None or df.empty:
            return False

        with self._get_connection() as conn:
            now = datetime.now()
            for _, row in df.iterrows():
                conn.execute(
                    """INSERT INTO ipo_history
                       (ipo_name, gmp, price, gain, ipo_type, date_range, scraped_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (
                        row.get("Current IPOs", ""),
                        row.get("IPO GMP", 0),
                        row.get("IPO Price", 0),
                        row.get("Gain", 0),
                        row.get("Type", "Mainline"),
                        row.get("Date", ""),
                        now,
                    ),
                )
            logger.info(f"✅ Saved snapshot: {len(df)} IPOs")
            return True

    def get_ipo_history(self, ipo_name: str = None, days: int = 30) -> pd.DataFrame:
        """Get IPO history, optionally filtered."""
        with self._get_connection() as conn:
            if ipo_name:
                df = pd.read_sql_query(
                    """SELECT * FROM ipo_history
                       WHERE ipo_name = ?
                       AND scraped_at >= datetime('now', ?)
                       ORDER BY scraped_at DESC""",
                    conn,
                    params=(ipo_name, f"-{days} days"),
                )
            else:
                df = pd.read_sql_query(
                    """SELECT * FROM ipo_history
                       WHERE scraped_at >= datetime('now', ?)
                       ORDER BY scraped_at DESC""",
                    conn,
                    params=(f"-{days} days",),
                )
        return df

    # ── Notification Log ─────────────────────────────────────────

    def log_notification(self, phone, channel, message, status, error=""):
        """Log a sent notification."""
        with self._get_connection() as conn:
            conn.execute(
                """INSERT INTO notification_log
                   (phone, channel, message, status, error_message)
                   VALUES (?, ?, ?, ?, ?)""",
                (phone, channel, message, status, error),
            )

    def get_notification_log(self, limit=100) -> pd.DataFrame:
        """Retrieve recent notification logs."""
        with self._get_connection() as conn:
            return pd.read_sql_query(
                "SELECT * FROM notification_log ORDER BY sent_at DESC LIMIT ?",
                conn,
                params=(limit,),
            )

    # ── Settings ─────────────────────────────────────────────────

    def get_setting(self, key, default=None):
        """Get a setting value."""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT value FROM settings WHERE key = ?", (key,)
            ).fetchone()
            return row[0] if row else default

    def set_setting(self, key, value):
        """Set a setting value."""
        with self._get_connection() as conn:
            conn.execute(
                """INSERT OR REPLACE INTO settings (key, value, updated_at)
                   VALUES (?, ?, ?)""",
                (key, str(value), datetime.now()),
            )

    def get_all_settings(self) -> dict:
        """Get all settings as a dictionary."""
        with self._get_connection() as conn:
            rows = conn.execute("SELECT key, value FROM settings").fetchall()
        return {r[0]: r[1] for r in rows}