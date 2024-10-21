# tracker/server.py
import asyncio
import json
from tracker.database import Database

class TrackerServer:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.db = Database()

    async def handle_client(self, reader, writer):
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
            if action == 'register':
                filename = data.get('filename')
                peer = data.get('peer')
                self.db.add_peer(filename, peer)
                return {'status': 'success'}
            elif action == 'search':
                filename = data.get('filename')
                peers = self.db.get_peers(filename)
                return {'peers': peers}
            else:
                return {'status': 'invalid_action'}
        except json.JSONDecodeError:
            return {'status': 'invalid_json'}

    async def run(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        addr = server.sockets[0].getsockname()
        print(f'Tracker server running on {addr}')

        async with server:
            await server.serve_forever()
