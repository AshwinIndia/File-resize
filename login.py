import sqlite3
import bcrypt
from tkinter import *
from tkinter import messagebox
from resizer import launch_resizer_gui

# Database setup
def setup_db():
    conn = sqlite3.connect('file_resizer.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       username TEXT NOT NULL UNIQUE, 
                       password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Register User
def register_user(username, password):
    conn = sqlite3.connect('file_resizer.db')
    cursor = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                       (username, hashed_password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

# Validate Login
def validate_login(username, password):
    conn = sqlite3.connect('file_resizer.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return bcrypt.checkpw(password.encode('utf-8'), result[0])
    return False

# GUI Setup
def login_register_gui():
    root = Tk()
    root.title("Login/Register")
    root.geometry("300x250")

    def login():
        username = username_entry.get()
        password = password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        if validate_login(username, password):
            messagebox.showinfo("Login", "Login Successful!")
            root.destroy()
            launch_resizer_gui()
        else:
            messagebox.showerror("Login", "Invalid Username or Password")

    def register():
        username = username_entry.get()
        password = password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        if register_user(username, password):
            messagebox.showinfo("Register", "Registration Successful!")
        else:
            messagebox.showerror("Register", "Username already exists!")

    Label(root, text="Username").pack()
    username_entry = Entry(root)
    username_entry.pack()

    Label(root, text="Password").pack()
    password_entry = Entry(root, show='*')
    password_entry.pack()

    Button(root, text="Login", command=login).pack()
    Button(root, text="Register", command=register).pack()

    root.mainloop()

setup_db()
login_register_gui()
