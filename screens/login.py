from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from peer.client import PeerClient
import screens.navigation as nav
import requests
import threading
import os

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title('Login')
        self.root.geometry('925x500+300+200')
        self.root.configure(bg="#fff")
        self.root.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):
        img = ImageTk.PhotoImage(Image.open("assets/images/auth.png").resize((450, 400)))
        self.img = img
        
        Label(self.root, image=self.img, bg="white").place(x=50, y=50)

        frame = Frame(self.root, width=350, height=350, bg="white")
        frame.place(x=520, y=70)

        heading = Label(frame, text='Login', fg='#57a1f8', bg='white', font=('', 23, 'bold'))
        heading.place(x=100, y=5)

        self.username = Entry(frame, width=25, fg='black', border=0, bg='white', font=('', 11))
        self.username.place(x=30, y=80)
        self.username.insert(0, 'Username')
        self.username.bind('<FocusIn>', self.on_focus_in)
        self.username.bind('<FocusOut>', self.on_focus_out)

        Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

        self.password = Entry(frame, width=25, fg='black', border=0, bg='white', font=('', 11))
        self.password.place(x=30, y=150)
        self.password.insert(0, 'Password')
        self.password.bind('<FocusIn>', self.on_focus_in)
        self.password.bind('<FocusOut>', self.on_focus_out)

        Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

        signin_btn = Button(frame, width=39, pady=7, text='Sign in', bg='#57a1f8', fg='white', border=0, cursor='hand2', command=self.signin)
        signin_btn.place(x=35, y=204)

        label = Label(frame, text="Don't have an account?", fg='black', bg='white', font=('', 9))
        label.place(x=75, y=270)
        signupNav_btn = Button(frame, width=6, text='Sign up', border=0, bg='white', cursor='hand2', fg='#57a1f8', command=self.signup_nav)
        signupNav_btn.place(x=215, y=270)

    def on_focus_in(self, event):
        widget = event.widget
        if widget.get() in ['Username', 'Password']:
            widget.delete(0, END)
            if widget == self.password:
                widget.config(show='*')

    def on_focus_out(self, event):
        widget = event.widget
        if widget.get() == '':
            if widget == self.username:
                widget.insert(0, 'Username')
            elif widget == self.password:
                widget.insert(0, 'Password')
                widget.config(show='')

    def signin(self):
        username = self.username.get()
        password = self.password.get()

        url = "http://localhost:5000/login"
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            response_data = response.json()
            shared_file_path = response_data["shared_file_path"]

            shared_files = []
            if os.path.isdir(shared_file_path):
                shared_files = os.listdir(shared_file_path)

            client = PeerClient(peer_name=username, shared_files_path=shared_file_path)
            client.port = client.find_available_port()
            client.shared_files = shared_files

            if client.register_with_tracker():
                threading.Thread(target=client.start_peer, daemon=True).start()
                self.root.destroy()
                nav.start_download_screen(client)
        else:
            messagebox.showerror('Invalid', "Invalid username or password")

    def signup_nav(self):
        self.root.destroy()
        nav.start_register_screen()

if __name__ == "__main__":
    login_root = Tk()
    Login(login_root)
    login_root.mainloop()
