from flask import Flask, request, jsonify
import tracker.database as db
import sqlite3

app = Flask(__name__)

# Initialize the SQLite database to store peer information
db.initialize_db()

@app.route('/register', methods=['POST'])
def register_peer_route():
    data = request.json
    ip = request.remote_addr
    port = data['port']
    shared_files = data['shared_files']

    # Giả sử bạn có một hàm để tạo peer_id, ví dụ:
    peer_id = str(hash(ip + str(port)))

    db.add_peer(ip, port, shared_files)

    # Trả về peer_id trong phản hồi
    return jsonify({
        "peer_id": peer_id, 
        "ip": ip, 
        "port": port, 
        "message": "Peer registered successfully"
    })


@app.route('/unregister', methods=['POST'])
def unregister_peer_route():
    data = request.json
    ip = request.remote_addr
    port = data['port']

    db.remove_peer(ip, port)
    return jsonify({"message": "Peer unregistered successfully"})

@app.route('/get_all_peers', methods=['GET'])
def get_all_peers_route():
    peers = db.get_all_peers()
    return jsonify(peers)

@app.route('/find_file', methods=['GET'])
def find_file_route():
    filename = request.args.get('filename')
    if not filename:
        return jsonify({"error": "Filename is required"}), 400

    peers = db.find_peers_with_file(filename)
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
