import threading
import tkinter as tk
from tkinter import messagebox
from peer.client import PeerClient

class DownloadScreen:
    def __init__(self, root, client):
        self.client = client
        self.root = root
        self.root.title("P2P File Sharing - Download")
        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        self.search_label = tk.Label(self.frame, text="Enter filename to search:")
        self.search_label.grid(row=0, column=0, sticky='w')

        self.search_entry = tk.Entry(self.frame)
        self.search_entry.grid(row=0, column=1, pady=5)

        self.search_button = tk.Button(self.frame, text="Search", command=self.search_file)
        self.search_button.grid(row=1, columnspan=2, pady=10)

        self.files_listbox = tk.Listbox(self.frame, width=50)
        self.files_listbox.grid(row=2, columnspan=2, pady=10)

        self.download_button = tk.Button(self.frame, text="Download", command=self.download_file)
        self.download_button.grid(row=3, columnspan=2, pady=10)

    def search_file(self):
        filename = self.search_entry.get()
        if not filename:
            self.show_error("Please enter a filename")
            return
        self.update_file_list(filename)

    def update_file_list(self, filename):
        try:
            peers = self.client.get_peers_from_tracker()
            self.files_listbox.delete(0, tk.END)
            for peer in peers:
                self.files_listbox.insert(tk.END, f"{peer['ip']}:{peer['port']} - {filename}")
        except Exception as e:
            self.show_error(f"Error fetching peers: {str(e)}")

    def download_file(self):
        selected = self.files_listbox.curselection()
        if not selected:
            self.show_error("Please select a file to download")
            return

        peer_info = self.files_listbox.get(selected[0]).split(" - ")[0]
        ip, port = peer_info.split(":")
        filename = self.search_entry.get()

        threading.Thread(target=self.run_download, args=(ip, port, filename)).start()

    def run_download(self, ip, port, filename):
        self.client.download_file(ip, int(port), filename)

    def show_error(self, message):
        messagebox.showerror("Error", message)


class RegistrationScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("P2P File Sharing - Registration")
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=20)

        tk.Label(frame, text="Peer Name:").grid(row=0, column=0, sticky='w')
        self.peer_name_entry = tk.Entry(frame)
        self.peer_name_entry.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Shared Files Path:").grid(row=1, column=0, sticky='w')
        self.shared_files_entry = tk.Entry(frame)
        self.shared_files_entry.grid(row=1, column=1, pady=5)

        register_button = tk.Button(frame, text="Register and Start", command=self.register_peer)
        register_button.grid(row=2, columnspan=2, pady=10)

    def register_peer(self):
        peer_name = self.peer_name_entry.get()
        shared_files_path = self.shared_files_entry.get()
        
        if not peer_name or not shared_files_path:
            messagebox.showerror("Error", "Please enter all fields")
            return

        client = PeerClient(peer_name, shared_files_path)
        client.port = client.find_available_port()  # Use random port

        if client.register_with_tracker():
            threading.Thread(target=client.start_peer, daemon=True).start()
            self.root.destroy()
            self.start_download_screen(client)

    def start_download_screen(self, client):
        download_root = tk.Tk()
        app = DownloadScreen(download_root, client)
        download_root.mainloop()

def setup_ui():
    root = tk.Tk()
    app = RegistrationScreen(root)
    root.mainloop()

if __name__ == "__main__":
    setup_ui()
