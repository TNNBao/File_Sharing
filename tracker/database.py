import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Khởi tạo cơ sở dữ liệu và các bảng
def initialize_db():
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS peers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT NOT NULL,
            port INTEGER NOT NULL,
            shared_files TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            shared_file_path TEXT
        )
    """)
    conn.commit()
    conn.close()

# Thao tác với bảng peers
def add_peer(ip, port, shared_files):
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO peers (ip, port, shared_files) VALUES (?, ?, ?)", (ip, port, shared_files))
    conn.commit()
    conn.close()

def remove_peer(peer_id):
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM peers WHERE id = ?", (peer_id,))
    conn.commit()
    conn.close()

def remove_all_peers():
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM peers")
    conn.commit()
    conn.close()

def get_all_peers():
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM peers")
    peers = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "ip": row[1], "port": row[2], "shared_files": row[3]} for row in peers]

def get_next_peer_id():
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM peers")
    result = cursor.fetchone()[0]
    conn.close()
    return (result or 0) + 1

# Find peers that have a specific file
def find_peers_with_file(filename):
    conn = sqlite3.connect('tracker.db')
    cursor = conn.cursor()
    cursor.execute('SELECT ip, port FROM peers WHERE shared_files LIKE ?', (f'%{filename}%',))
    peers = cursor.fetchall()
    conn.close()
    return [{'ip': peer[0], 'port': peer[1]} for peer in peers]

# Thao tác với bảng accounts
def add_account(username, password, shared_file_path):
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO accounts (username, password, shared_file_path) VALUES (?, ?, ?)", (username, hashed_password, shared_file_path))
    conn.commit()
    conn.close()

def get_account(username):
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts WHERE username = ?", (username,))
    account = cursor.fetchone()
    conn.close()
    if account:
        return {"id": account[0], "username": account[1], "password": account[2], "shared_file_path": account[3]}
    return None

def authenticate_account(username, password):
    account = get_account(username)
    if account and check_password_hash(account['password'], password):
        return True
    return False
