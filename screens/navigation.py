import tkinter as tk
from screens.download import DownloadScreen
from screens.login import Login
from screens.register import Register

def start_download_screen(client):
    download_root = tk.Tk()
    app = DownloadScreen(download_root, client)
    download_root.mainloop()

def start_login_screen():
    login_root = tk.Tk()
    Login(login_root)
    login_root.mainloop()

def start_register_screen():
    register_root = tk.Tk()
    Register(register_root)
    register_root.mainloop()