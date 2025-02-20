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
            virtual_ip TEXT,
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
def add_peer(ip, port, virtual_ip, shared_files):
    shared_files_str = ",".join(shared_files) if shared_files else ""
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO peers (ip, port, virtual_ip, shared_files) VALUES (?, ?, ?, ?)", (ip, port, virtual_ip, shared_files_str))
    conn.commit()
    conn.close()

def remove_peer(ip, port):
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM peers WHERE ip = ? AND port = ?", (ip, port))
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
    return [{"id": row[0], "ip": row[1], "port": row[2], "virtual_ip": row[3], "shared_files": row[4]} for row in peers]

def get_peer_through_virtual_ip(virtual_ip):
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM peers WHERE virtual_ip = ?", (virtual_ip,))
    peer = cursor.fetchone()
    conn.close()
    return {"id": peer[0], "ip": peer[1], "port": peer[2], "virtual_ip": peer[3], "shared_files": peer[4]}

def get_next_peer_id():
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM peers")
    result = cursor.fetchone()[0]
    conn.close()
    return (result or 0) + 1

def find_peers_with_file(filename):
    conn = sqlite3.connect('tracker.db')
    cursor = conn.cursor()
    cursor.execute('SELECT ip, virtual_ip, port FROM peers WHERE shared_files LIKE ?', (f'%{filename}%',))
    peers = cursor.fetchall()
    conn.close()
    print(f"Peers containing '{filename}': {peers}")  
    return [{'ip': peer[0], 'virtual_ip':peer[1], 'port': peer[2]} for peer in peers]

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
