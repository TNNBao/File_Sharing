import socket
import os
import requests
from tkinter import messagebox

class PeerClient:
    def __init__(self, peer_name, shared_files_path):
        self.peer_name = peer_name
        self.shared_files_path = shared_files_path
        self.peer_id = None
        self.ip = None
        self.port = self.find_available_port()

    def find_available_port(self):
        """Finds an available port to avoid conflicts with other peers."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as temp_socket:
            temp_socket.bind(('', 0))  # Bind to a free port
            return temp_socket.getsockname()[1]

    def register_with_tracker(self):
        url = 'http://127.0.0.1:5000/register'
        data = {
            'peer_name': self.peer_name,
            'shared_files': self.shared_files_path,
            'port': self.port
        }

        response = requests.post(url, json=data)

        # In ra phản hồi từ server để kiểm tra
        print("Response from tracker:", response.json())

        if response.status_code == 200:
            # Kiểm tra xem 'peer_id' có tồn tại trong phản hồi hay không
            if 'peer_id' in response.json():
                self.peer_id = response.json()['peer_id']
                self.ip = response.json()['ip']
                messagebox.showinfo("Success", f"Registered with IP: {self.ip}")
                return True
            else:
                messagebox.showerror("Error", "peer_id not found in response")
                return False
        else:
            messagebox.showerror("Error", "Failed to register with tracker")
            return False

    def start_peer(self):
        """Starts listening for incoming file download requests from other peers."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(('0.0.0.0', self.port))
            server_socket.listen()
            print(f"Listening on port {self.port}...")
            while True:
                client_socket, _ = server_socket.accept()
                with client_socket:
                    self.handle_peer(client_socket)

    def handle_peer(self, client_socket):
        """Handles an incoming request for a file download."""
        data = client_socket.recv(1024).decode()
        if data.startswith('DOWNLOAD'):
            filename = data.split()[1]
            filepath = os.path.join(self.shared_files_path, filename)
            if os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    content = f.read()
                if content:
                    print(f"Sending {filename} with {len(content)} bytes.")
                    client_socket.sendall(content)
                else:
                    print("File is empty, sending empty response.")
                    client_socket.sendall(b"File is empty")  # Kiểm tra file rỗng
            else:
                client_socket.sendall(b"File not found")
                print(f"File '{filename}' not found")

    def get_peers_from_tracker(self):
        url = 'http://127.0.0.1:5000/get_all_peers'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            messagebox.showerror("Error", "Failed to get peers from tracker")
            return []

    def download_file(self, ip, port, filename):
        """Connects to another peer and requests a file download."""
        try:
            with socket.create_connection((ip, int(port)), timeout=10) as client_socket:
                client_socket.sendall(f"DOWNLOAD {filename}".encode())

                file_path = os.path.join(self.shared_files_path, filename)
                with open(file_path, 'wb') as f:
                    while True:
                        data = client_socket.recv(1024)
                        if not data:
                            break
                        f.write(data)
                        print(f"Receiving data chunk for {filename}")

            print(f"File '{filename}' downloaded to {file_path}")
            messagebox.showinfo("Success", f"Downloaded {filename} from {ip}:{port}")

        except socket.timeout:
            messagebox.showerror("Error", f"Connection timeout while downloading {filename} from {ip}:{port}")
        except Exception as e:
            messagebox.showerror("Error", f"Error downloading file: {str(e)}")

    def login(self, username, password):
        url = "http://localhost:5000/login"
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            self.peer_id = response.json()['user_id']
            self.shared_files_path = response.json()['shared_file_path']
        return response.json()
