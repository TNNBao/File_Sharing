from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from screens.login import Login
import requests

class Register:
    def __init__(self, root):
        self.root = root
        self.root.title('Register')
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

        heading = Label(frame, text='Sign up', fg='#57a1f8', bg='white', font=('', 23, 'bold'))
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

        self.shared_files_path = Entry(frame, width=25, fg='black', border=0, bg='white', font=('', 11))
        self.shared_files_path.place(x=30, y=220)
        self.shared_files_path.insert(0, 'Shared Files Path')
        self.shared_files_path.bind('<FocusIn>', self.on_focus_in)
        self.shared_files_path.bind('<FocusOut>', self.on_focus_out)

        Frame(frame, width=295, height=2, bg='black').place(x=25, y=247)

        signup_btn = Button(frame, width=39, pady=7, text='Sign up', bg='#57a1f8', fg='white', border=0, cursor='hand2', command=self.signup)
        signup_btn.place(x=35, y=280)

        label = Label(frame, text="I have an account", fg='black', bg='white', font=('', 9))
        label.place(x=90, y=340)
        signinNav_btn = Button(frame, width=6, text='Sign in', border=0, bg='white', cursor='hand2', fg='#57a1f8', command=self.signin_nav)
        signinNav_btn.place(x=200, y=340)

    def on_focus_in(self, event):
        widget = event.widget
        if widget.get() in ['Username', 'Password', 'Shared Files Path']:
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
            elif widget == self.shared_files_path:
                widget.insert(0, 'Shared Files Path')

    def signup(self):
        username = self.username.get()
        password = self.password.get()
        shared_files_path = self.shared_files_path.get()

        url = 'http://127.0.0.1:5000/register_account'
        data = {
            'username': username,
            'password': password,
            'shared_file_path': shared_files_path
        }
        response = requests.post(url, json=data)
        if response.status_code == 201:
            messagebox.showinfo('Success', 'User registered successfully')
            self.root.destroy()
            Login(Tk())
        else:
            messagebox.showerror('Error', response.json()['message'])

    def signin_nav(self):
        self.root.destroy()
        login_root = Tk()
        Login(login_root)
        login_root.mainloop()

if __name__ == "__main__":
    pass
