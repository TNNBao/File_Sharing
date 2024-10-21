import asyncio
from tracker.database import initialize_db, add_peer, get_all_peers, remove_peer

class TrackerServer:
    def __init__(self):
        self.peers = {}
        initialize_db()

    async def handle_peer(self, reader, writer):
        data = await reader.read(100)
        message = data.decode()
        ip = writer.get_extra_info('peername')[0]

        if message.startswith('REGISTER'):
            port, shared_files = message.split()[1:3]
            self.peers[ip] = (port, shared_files)
            add_peer(ip, port, shared_files)
            writer.write(f"Registered with IP {ip}".encode())
        elif message.startswith('UNREGISTER'):
            remove_peer(ip)
            if ip in self.peers:
                del self.peers[ip]
            writer.write(f"Unregistered IP {ip}".encode())
        elif message.startswith('GET_PEERS'):
            peers = get_all_peers()
            writer.write(str(peers).encode())
        
        await writer.drain()
        writer.close()

    async def run(self):
        server = await asyncio.start_server(self.handle_peer, '0.0.0.0', 6881)
        async with server:
            await server.serve_forever()

if __name__ == '__main__':
    tracker = TrackerServer()
    asyncio.run(tracker.run())
