import sqlite3
import os

class Database:
    def __init__(self, db_path="config/enms.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.cursor().execute("""
                CREATE TABLE IF NOT EXISTS infrastructure (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hostname TEXT NOT NULL,
                    ip_address TEXT NOT NULL UNIQUE,
                    role TEXT NOT NULL,
                    status TEXT DEFAULT 'Inconnu',
                    last_seen TEXT DEFAULT 'Jamais'
                )
            """)
            conn.commit()

    def add_node(self, hostname, ip, role):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.cursor().execute(
                    "INSERT INTO infrastructure (hostname, ip_address, role) VALUES (?, ?, ?)",
                    (hostname, ip, role)
                )
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def fetch_nodes(self):
        with sqlite3.connect(self.db_path) as conn:
            return conn.cursor().execute("SELECT * FROM infrastructure").fetchall()

    def update_node_status(self, ip, status, timestamp):
        with sqlite3.connect(self.db_path) as conn:
            conn.cursor().execute(
                "UPDATE infrastructure SET status = ?, last_seen = ? WHERE ip_address = ?",
                (status, timestamp, ip)
            )
            conn.commit()

    def delete_node(self, node_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.cursor().execute("DELETE FROM infrastructure WHERE id = ?", (node_id,))
            conn.commit()