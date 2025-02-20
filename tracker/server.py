from flask import Flask, request, jsonify
import tracker.database as db
from dhcp.dhcp_server import DHCPServer
import sqlite3

app = Flask(__name__)
dhcp_server = DHCPServer("192.168.1.0", "192.168.1.255")

# Initialize the SQLite database to store peer information
db.initialize_db()

@app.route('/register', methods=['POST'])
def register_peer_route():
    data = request.json
    ip = request.remote_addr
    port = data['port']
    shared_files = data['shared_files']

    # hash peer_id
    peer_id = str((ip +":"+ str(port)))
    virtual_ip = dhcp_server.allocate_ip(peer_id)

    db.add_peer(ip, port, virtual_ip, shared_files)

    return jsonify({
        "peer_id": peer_id, 
        "ip": ip,
        "virtual_ip": virtual_ip, 
        "port": port, 
        "message": "Peer registered successfully"
    })

@app.route('/unregister', methods=['POST'])
def unregister_peer_route():
    data = request.json
    ip = request.remote_addr
    port = data['port']

    peer_id = str((ip +":"+ str(port)))
    dhcp_server.release_ip(peer_id)

    db.remove_peer(ip, port)
    return jsonify({"message": "Peer unregistered successfully"})

@app.route('/get_all_peers', methods=['GET'])
def get_all_peers_route():
    peers = db.get_all_peers()
    return jsonify(peers)

@app.route('/get_peer_through_virtual_ip', methods=['GET'])
def get_peer_through_virtual_ip():
    virtual_ip = request.args.get('virtual_ip')
    if not virtual_ip:
        return jsonify({"error": "Virtual_ip is required"}), 400
    
    peer = db.get_peer_through_virtual_ip(virtual_ip)
    return jsonify(peer)

@app.route('/find_file', methods=['GET'])
def find_file_route():
    filename = request.args.get('filename')
    if not filename:
        return jsonify({"error": "Filename is required"}), 400

    peers = db.find_peers_with_file(filename)
    print(f"API find_file_route called for filename: {filename}")
    print(f"Peers found: {peers}") 
    return jsonify(peers)

# Routes for account management
@app.route('/register_account', methods=['POST'])
def register_account_route():
    data = request.json
    username = data['username']
    password = data['password']
    shared_file_path = data['shared_file_path']
    try:
        db.add_account(username, password, shared_file_path)
        return jsonify({"message": "User registered successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"message": "Username already exists"}), 400

@app.route('/login', methods=['POST'])
def login_route():
    data = request.json
    username = data['username']
    password = data['password']
    if db.authenticate_account(username, password):
        account = db.get_account(username)
        return jsonify({
            "message": "Login successful",
            "user_id": account['id'],
            "shared_file_path": account['shared_file_path']
        }), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
