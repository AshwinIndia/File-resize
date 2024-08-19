import sqlite3
from tkinter import *

def show_database():
    conn = sqlite3.connect('file_resizer.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, password FROM users')
    records = cursor.fetchall()
    conn.close()

    db_window = Tk()
    db_window.title("Database Records")

    Label(db_window, text="Username", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=10)
    Label(db_window, text="Password (Hashed)", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=10, pady=10)

    for i, record in enumerate(records, start=1):
        Label(db_window, text=record[0], font=("Arial", 10)).grid(row=i, column=0, padx=10, pady=5)
        hidden_password = "********"  
        Label(db_window, text=hidden_password, font=("Arial", 10)).grid(row=i, column=1, padx=10, pady=5)

    db_window.mainloop()

if __name__ == "__main__":
    show_database()
