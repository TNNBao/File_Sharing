# main.py
import asyncio
import threading
from tracker.server import TrackerServer
from peer.client import PeerClient
from peer.gui import TorrentGUI
import tkinter as tk

def start_asyncio_loop(loop):
    """Chạy asyncio event loop trong một luồng riêng."""
    asyncio.set_event_loop(loop)
    loop.run_forever()

def main():
    # Tạo một event loop mới cho asyncio
    loop = asyncio.new_event_loop()
    asyncio_thread = threading.Thread(target=start_asyncio_loop, args=(loop,), daemon=True)
    asyncio_thread.start()

    # Khởi tạo Tracker và Peer
    tracker = TrackerServer()
    peer = PeerClient()

    # Đăng ký Tracker chạy trên event loop
    asyncio.run_coroutine_threadsafe(tracker.run(), loop)

    # Khởi tạo GUI
    root = tk.Tk()
    app = TorrentGUI(root, peer, loop)
    root.mainloop()

if __name__ == "__main__":
    main()
