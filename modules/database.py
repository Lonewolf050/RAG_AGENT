import sqlite3
from datetime import datetime
from typing import Dict, Optional


class Database:
    def __init__(self, db_path="./data/summaries.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._init_tables()
        print(f"[Database] Connected")
    
    def _init_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                summary TEXT NOT NULL,
                query TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                whatsapp_sent BOOLEAN DEFAULT FALSE,
                sms_sent BOOLEAN DEFAULT FALSE,
                email_sent BOOLEAN DEFAULT FALSE
            )
        """)
        self.conn.commit()
    
    def save_summary(self, summary: str, query: str = None) -> int:
        cursor = self.conn.execute(
            "INSERT INTO summaries (summary, query) VALUES (?, ?)",
            (summary, query)
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def get_summary(self, summary_id: int) -> Optional[Dict]:
        cursor = self.conn.execute(
            "SELECT * FROM summaries WHERE id = ?", (summary_id,)
        )
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "summary": row[1],
                "query": row[2],
                "created_at": row[3],
                "whatsapp_sent": row[4],
                "sms_sent": row[5],
                "email_sent": row[6]
            }
        return None
    
    def update_notification_status(self, summary_id: int, channel: str, status: bool):
        self.conn.execute(
            f"UPDATE summaries SET {channel}_sent = ? WHERE id = ?",
            (status, summary_id)
        )
        self.conn.commit()


_db = None

def get_database():
    global _db
    if _db is None:
        _db = Database()
    return _db
