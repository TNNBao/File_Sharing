from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

class Register:
    def __init__(self, root):
        self.root = root
        self.root.title('Register')
        self.root.geometry('925x500+300+200')
        self.root.configure(bg="#fff")
        self.root.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):
        # Load and resize the image
        img = ImageTk.PhotoImage(Image.open("assets/images/auth.png").resize((450, 400)))
        Label(self.root, image=img, bg="white").place(x=50, y=50)
        
        # Keep a reference to the image to prevent it from being garbage collected
        self.img = img

        frame = Frame(self.root, width=350, height=400, bg="white")
        frame.place(x=520, y=70)

        # Header
        heading = Label(frame, text='Register', fg='#57a1f8', bg='white', font=('', 23, 'bold'))
        heading.place(x=100, y=5)

        # Username
        def on_focus_in(e):
            if self.username.get() == 'Username':
                self.username.delete(0, END) 

        def on_focus_out(e):
            if self.username.get() == '':
                self.username.insert(0, 'Username')

        self.username = Entry(frame, width=25, fg='black', border=0, bg='white', font=('', 11))
        self.username.place(x=30, y=80)
        self.username.insert(0, 'Username')
        self.username.bind('<FocusIn>', on_focus_in)
        self.username.bind('<FocusOut>', on_focus_out)

        Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

        # Email
        def on_focus_in(e):
            if self.email.get() == 'Email':
                self.email.delete(0, END) 

        def on_focus_out(e):
            if self.email.get() == '':
                self.email.insert(0, 'Email')

        self.email = Entry(frame, width=25, fg='black', border=0, bg='white', font=('', 11))
        self.email.place(x=30, y=130)
        self.email.insert(0, 'Email')
        self.email.bind('<FocusIn>', on_focus_in)
        self.email.bind('<FocusOut>', on_focus_out)

        Frame(frame, width=295, height=2, bg='black').place(x=25, y=157)

        # Password
        def on_focus_in(e):
            if self.password.get() == 'Password':
                self.password.delete(0, END)
                self.password.config(show='*')

        def on_focus_out(e):
            if self.password.get() == '':
                self.password.insert(0, 'Password')
                self.password.config(show='')

        self.password = Entry(frame, width=25, fg='black', border=0, bg='white', font=('', 11))
        self.password.place(x=30, y=180)
        self.password.insert(0, 'Password')
        self.password.bind('<FocusIn>', on_focus_in)
        self.password.bind('<FocusOut>', on_focus_out)

        Frame(frame, width=295, height=2, bg='black').place(x=25, y=207)

        # Password Confirm
        def on_focus_in(e):
            if self.password_confirm.get() == 'Confirm Password':
                self.password_confirm.delete(0, END)
                self.password_confirm.config(show='*')

        def on_focus_out(e):
            if self.password_confirm.get() == '':
                self.password_confirm.insert(0, 'Confirm Password')
                self.password_confirm.config(show='')

        self.password_confirm = Entry(frame, width=25, fg='black', border=0, bg='white', font=('', 11))
        self.password_confirm.place(x=30, y=230)
        self.password_confirm.insert(0, 'Confirm Password')
        self.password_confirm.bind('<FocusIn>', on_focus_in)
        self.password_confirm.bind('<FocusOut>', on_focus_out)

        Frame(frame, width=295, height=2, bg='black').place(x=25, y=257)

        # Sign in button
        signup_btn = Button(frame, width=39, pady=7, text='Sign up', bg='#57a1f8', fg='white', border=0, cursor='hand2', command=self.signup)
        signup_btn.place(x=35, y=284)

        # Sign up recommend line
        label = Label(frame, text="Already have an account?", fg='black', bg='white', font=('', 9))
        label.place(x=75, y=330)
        signinNav_btn = Button(frame, width=6, text='Sign in', border=0, bg='white', cursor='hand2', fg='#57a1f8')
        signinNav_btn.place(x=218, y=330)

    
    def signup(self):
        email = self.email.get()
        password = self.password.get()

        if email == 'admin' and password == '1234':
            screen = Toplevel(self.root)
            screen.title("App")
            screen.geometry("920x500+300+200")
            screen.config(bg='white')

            Label(screen, text="Hello", bg='#fff').pack(expand=True)

            screen.mainloop()
        else:
            messagebox.showerror('Invalid', "invalid email or password")

    def signin_nav(self):
        pass

if __name__ == "__main__":
    root = Tk()
    app = Register(root)
    root.mainloop()
