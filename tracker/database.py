import sqlite3

def initialize_db():
    conn = sqlite3.connect('tracker.db')
    cursor = conn.cursor()

    # Tạo bảng peer
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS peer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT NOT NULL,
        port INTEGER NOT NULL,
        shared_files TEXT
    )
    ''')

    conn.commit()
    conn.close()

def add_peer(ip, port, shared_files):
    conn = sqlite3.connect('tracker.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO peer (ip, port, shared_files) VALUES (?, ?, ?)', (ip, port, shared_files))
    conn.commit()
    conn.close()

def get_all_peers():
    conn = sqlite3.connect('tracker.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM peer')
    peers = cursor.fetchall()
    conn.close()
    return peers

def remove_peer(ip):
    conn = sqlite3.connect('tracker.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM peer WHERE ip = ?', (ip,))
    conn.commit()
    conn.close()
