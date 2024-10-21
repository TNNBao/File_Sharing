# tracker/database.py
import sqlite3

class Database:
    def __init__(self, db_name='tracker.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS peers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                peer_address TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_peer(self, filename, peer_address):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO peers (filename, peer_address) VALUES (?, ?)', (filename, peer_address))
        self.conn.commit()

    def get_peers(self, filename):
        cursor = self.conn.cursor()
        cursor.execute('SELECT peer_address FROM peers WHERE filename = ?', (filename,))
        return [row[0] for row in cursor.fetchall()]

    def close(self):
        self.conn.close()
