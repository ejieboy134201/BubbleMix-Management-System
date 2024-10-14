import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
from pages.admin.admin_panel import AdminPortal  # Ensure this path is correct

# Ensure the database folder exists
if not os.path.exists('database'):
    os.makedirs('database')

# Create database and table if not exists, and insert dummy accounts
def setup_database():
    conn = sqlite3.connect('manage_accounts.db')  # Make sure to use the correct path
    cursor = conn.cursor()
    
    # Create a table called 'users' if it does not exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        account_type TEXT NOT NULL
    )''')

    # Insert dummy users if they do not exist
    cursor.execute("INSERT OR IGNORE INTO users (first_name, last_name, username, password, account_type) VALUES (?, ?, ?, ?, ?)",
                   ('Maria', 'Labo', 'maria', 'koko', 'admin'))
    cursor.execute("INSERT OR IGNORE INTO users (first_name, last_name, username, password, account_type) VALUES (?, ?, ?, ?, ?)",
                   ('John', 'Doe', 'john', '1234', 'admin'))

    conn.commit()
    conn.close()

# Call to create or setup the database with dummy data
setup_database()

# Login Page Class
class LoginPage:
    def __init__(self, master):
        self.master = master
        self.master.title("Login Page")
        self.master.geometry("400x300")
        
        # Create login form
        self.create_widgets()
    
    def create_widgets(self):
        # Username Label and Entry
        tk.Label(self.master, text="Username:", font=('Arial', 14)).pack(pady=10)
        self.username_entry = tk.Entry(self.master, font=('Arial', 14))
        self.username_entry.pack(pady=5)

        # Password Label and Entry
        tk.Label(self.master, text="Password:", font=('Arial', 14)).pack(pady=10)
        self.password_entry = tk.Entry(self.master, font=('Arial', 14), show='*')
        self.password_entry.pack(pady=5)

        # Login Button
        tk.Button(self.master, text="Login", font=('Arial', 14), command=self.validate_login).pack(pady=20)
    
    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Connect to the database
        conn = sqlite3.connect('manage_accounts.db')  # Make sure to use the correct path
        cursor = conn.cursor()

        # Query the database for the entered username and password
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        conn.close()

        def get_user_role(self, username):
            """Fetch the account type of the user based on their username."""
            cursor = self.conn.cursor()
            cursor.execute("SELECT account_type FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            if result:
                return result[0]  # This returns the account_type (e.g., 'admin' or 'employee')
            else:
                return None


        if user:
            if user[5] in ['admin']:
                messagebox.showinfo("Login Successful", f"Welcome, {user[1]} {user[2]}! You are logged in as {user[5]}.")
                self.master.withdraw()  # Hide login window
                admin_window = tk.Toplevel(self.master)  # Open new window for user panel
                AdminPortal(admin_window, account_type= 'admin')  # Call the UserPortal class, passing user details
                
            elif user[5] in ['employee']:
                messagebox.showinfo("Login Successful", f"Welcome, {user[1]} {user[2]}! You are logged in as {user[5]}.")
                self.master.withdraw()  # Hide login window
                admin_window = tk.Toplevel(self.master)  # Open new window for user panel
                AdminPortal(admin_window, account_type= 'employee')  # Call the UserPortal class, passing user details
                
        else:
            messagebox.showwarning("Login Failed", "Invalid username or password. Please try again.")


# Create the Tkinter application window and run the login page
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginPage(root)
    root.mainloop()
