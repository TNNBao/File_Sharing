import socket
import os
import requests
from tkinter import messagebox
from crypto.crypto import Crypto

class PeerClient:
    def __init__(self, peer_name, shared_files_path):
        self.peer_name = peer_name
        self.shared_files_path = shared_files_path
        self.peer_id = None
        self.ip = None
        self.virtual_ip = None
        self.port = self.find_available_port()
        self.crypto = Crypto()
        if os.path.isdir(shared_files_path):
            self.shared_files = os.listdir(shared_files_path)
        else:
            self.shared_files = []

    def find_available_port(self):
        """Finds an available port to avoid conflicts with other peers."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as temp_socket:
            temp_socket.bind(('', 0))  # Bind to a free port
            return temp_socket.getsockname()[1]

    def register_with_tracker(self):
        url = 'http://127.0.0.1:5000/register'
        data = {
            'peer_name': self.peer_name,
            'shared_files': self.shared_files,
            'port': self.port
        }

        response = requests.post(url, json=data)

        print("Response from tracker:", response.json())

        if response.status_code == 200:
            if 'peer_id' in response.json():
                self.peer_id = response.json()['peer_id']
                self.ip = response.json()['ip']
                self.virtual_ip = response.json()['virtual_ip']
                messagebox.showinfo("Success", f"Registered with IP: {self.virtual_ip}")
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
                    # Encrypt content
                    aes_key = os.urandom(32)
                    encrypted_content = self.crypto.encrypt(content, aes_key)
                    print(encrypted_content)

                    # Receive public key of requested peer
                    public_key_pem = client_socket.recv(1024)
                    peer_public_key = self.crypto.load_public_key(public_key_pem)

                    # Encrypt AES key using public key
                    encrypted_aes_key = self.crypto.encrypt_aes_key(aes_key, peer_public_key)

                    client_socket.sendall(encrypted_aes_key + encrypted_content)
                    print(f"Sending {filename} with {len(content)} bytes.")
                else:
                    print("File is empty, sending empty response.")
                    client_socket.sendall(b"File is empty") 
            else:
                client_socket.sendall(b"File not found")
                print(f"File '{filename}' not found")

    def get_peers_with_file(self, filename):
        url = f"http://localhost:5000/find_file?filename={filename}"
        response = requests.get(url)
        if response.status_code == 200:
            peers = response.json()
            print(f"Peers with file '{filename}': {peers}")
            # remove self and return the rest
            return [peer for peer in peers if peer['ip'] != self.ip or peer['port'] != self.port]
        else:
            raise Exception("Error fetching peers with file")
        
    def get_ip_through_virtual_ip(self, virtual_ip):
        url = f"http://localhost:5000/get_peer_through_virtual_ip?virtual_ip={virtual_ip}"
        response = requests.get(url)
        if response.status_code == 200:
            peer = response.json()
            return peer['ip']
        else:
            raise Exception("Error fetching peer")

    def get_peers_from_tracker(self):
        url = 'http://127.0.0.1:5000/get_all_peers'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            messagebox.showerror("Error", "Failed to get peers from tracker")
            return []

    def download_file(self, ip, virtual_ip, port, filename):
        """Connects to another peer and requests a file download."""
        try:
            with socket.create_connection((ip, int(port)), timeout=10) as client_socket:
                client_socket.sendall(f"DOWNLOAD {filename}".encode())

                # Send public key
                client_socket.sendall(self.crypto.get_public_key_pem())

                # Receive data
                encrypted_data = b""
                while True:
                    chunk = client_socket.recv(4096)
                    if not chunk:
                        break
                    encrypted_data += chunk
                
                # Decrypt
                encrypted_aes_key = encrypted_data[:256]  # RSA 2048 bit = 256 bytes
                encrypted_content = encrypted_data[256:]

                aes_key = self.crypto.decrypt_aes_key(encrypted_aes_key)
                content = self.crypto.decrypt(encrypted_content, aes_key)

                file_path = os.path.join(self.shared_files_path, filename)
                with open(file_path, 'wb') as f:
                    f.write(content)

            print(f"File '{filename}' downloaded to {file_path}")
            messagebox.showinfo("Success", f"Downloaded {filename} from {virtual_ip}:{port}")

        except socket.timeout:
            messagebox.showerror("Error", f"Connection timeout while downloading {filename} from {virtual_ip}:{port}")
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
            response_data = response.json()
            self.peer_id = response_data.get('user_id')
            self.shared_files_path = response_data.get('shared_file_path')

            if os.path.isdir(self.shared_files_path):
                self.shared_files = os.listdir(self.shared_files_path)
            else:
                self.shared_files = []

            return response_data
        else:
            messagebox.showerror("Error", "Login failed")
            return None
    
    def logout(self):
        url = "http://localhost:5000/unregister"
        try:
            response = requests.post(url, json={"port": self.port})
            if response.status_code == 200:
                print("Successfully unregistered peer")
            else:
                print(f"Failed to unregister peer: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Exception occurred during logout: {str(e)}")

