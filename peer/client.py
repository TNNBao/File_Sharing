# peer/client.py
import asyncio
import json
import os

class PeerClient:
    def __init__(self, tracker_host='localhost', tracker_port=8000, peer_host='localhost', peer_port=9000):
        self.tracker_host = tracker_host
        self.tracker_port = tracker_port
        self.peer_host = peer_host
        self.peer_port = peer_port
        self.shared_files = []
        self.downloaded_files = {}

    async def register_file(self, filename):
        reader, writer = await asyncio.open_connection(self.tracker_host, self.tracker_port)
        data = {'action': 'register', 'filename': filename, 'peer': f"{self.peer_host}:{self.peer_port}"}
        writer.write(json.dumps(data).encode('utf-8'))
        await writer.drain()
        response = await reader.read(4096)
        print(f"Registered {filename}: {response.decode('utf-8')}")
        writer.close()
        await writer.wait_closed()

    async def search_file(self, filename):
        reader, writer = await asyncio.open_connection(self.tracker_host, self.tracker_port)
        data = {'action': 'search', 'filename': filename}
        writer.write(json.dumps(data).encode('utf-8'))
        await writer.drain()
        response = await reader.read(4096)
        writer.close()
        await writer.wait_closed()
        peers = json.loads(response.decode('utf-8')).get('peers', [])
        return peers

    async def handle_peer_connection(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"Connected by {addr}")
        try:
            while True:
                data = await reader.read(4096)
                if not data:
                    break
                message = data.decode('utf-8')
                print(f"Received from {addr}: {message}")
                response = self.process_message(message)
                writer.write(json.dumps(response).encode('utf-8'))
                await writer.drain()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            writer.close()
            await writer.wait_closed()
            print(f"Connection closed: {addr}")

    def process_message(self, message):
        try:
            data = json.loads(message)
            action = data.get('action')
            if action == 'download':
                filename = data.get('filename')
                if filename in self.shared_files:
                    with open(filename, 'rb') as f:
                        content = f.read()
                    return {'status': 'success', 'data': content.hex()}
                else:
                    return {'status': 'file_not_found'}
            else:
                return {'status': 'invalid_action'}
        except json.JSONDecodeError:
            return {'status': 'invalid_json'}

    async def start_server(self):
        server = await asyncio.start_server(self.handle_peer_connection, self.peer_host, self.peer_port)
        addr = server.sockets[0].getsockname()
        print(f"Peer client running on {addr}")

        async with server:
            await server.serve_forever()

    async def download_file(self, filename):
        peers = await self.search_file(filename)
        if not peers:
            print("File not found on any peer.")
            return
        # Kết nối đến peer đầu tiên để tải file
        peer = peers[0]
        peer_host, peer_port = peer.split(':')
        reader, writer = await asyncio.open_connection(peer_host, int(peer_port))
        data = {'action': 'download', 'filename': filename}
        writer.write(json.dumps(data).encode('utf-8'))
        await writer.drain()
        response = await reader.read(4096)
        response_data = json.loads(response.decode('utf-8'))
        if response_data.get('status') == 'success':
            file_content = bytes.fromhex(response_data.get('data'))
            os.makedirs('downloads', exist_ok=True)
            with open(os.path.join('downloads', filename), 'wb') as f:
                f.write(file_content)
            print(f"Downloaded {filename} successfully.")
        else:
            print("Failed to download file.")
        writer.close()
        await writer.wait_closed()

    async def run(self):
        # Chạy server peer trong một task riêng biệt
        asyncio.create_task(self.start_server())
