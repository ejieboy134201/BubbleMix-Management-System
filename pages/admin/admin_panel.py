import tkinter as tk
from ttkbootstrap import Style
from tkinter import ttk, messagebox
from pages.admin.manage_items import ManageItems
import sqlite3

class AdminPortal:
    def __init__(self, master, account_type):
        self.master = master
        self.master.title("Admin Access Portal")
        
        # Set the window size to 1024x768
        self.master.geometry("1366x768")
        
        # Create the side navigation panel
        self.side_nav = tk.Frame(self.master, bg="white", width=200)
        self.side_nav.pack(side=tk.LEFT, fill=tk.Y)

        # Title for the portal
        self.title_label = tk.Label(self.master, text="Admin Access Panel", font=('Arial', 24), bg="#2c3e50", fg="white")
        self.title_label.pack(pady=20)

        # Tab buttons for the side panel
        self.create_side_nav_buttons()

        # Change the style of the buttons
        style = ttk.Style()
        style.configure("TButton", background="#2c3e50", foreground="white")
        style.map("TButton", background=[("active", "#3498db")])

        # Main content frame where pages will be shown
        self.main_content = tk.Frame(self.master, bg="white")
        self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Default page to load
        self.show_inventory_page()

        # Setup database connection
        self.conn = sqlite3.connect('manage_accounts.db')
        self.create_users_table()

        # Save the account type (admin or employee)
        self.account_type = account_type  # Set the account type from the constructor

    def create_users_table(self):
        """Creates the users table in the database if it doesn't exist.""" 
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                account_type TEXT NOT NULL
            )''')
        self.conn.commit()

    def create_side_nav_buttons(self):
        """Creates buttons for the side navigation panel.""" 
        self.inventory_button = tk.Button(self.side_nav, text="Inventory", font=('Arial', 14), bg="#2c3e50", fg="white", 
                                           relief=tk.FLAT, activebackground="yellow", command=self.show_inventory_page)
        self.inventory_button.pack(fill=tk.X, pady=5)

        self.sales_report_button = tk.Button(self.side_nav, text="Sales Report", font=('Arial', 14), bg="#2c3e50", fg="white", 
                                             relief=tk.FLAT, activebackground="yellow", command=self.show_sales_report_page)
        self.sales_report_button.pack(fill=tk.X, pady=5)

        self.manage_item_button = tk.Button(self.side_nav, text="Manage Item", font=('Arial', 14), bg="#2c3e50", fg="white", 
                                            relief=tk.FLAT, activebackground="yellow", command=self.show_manage_item_page)
        self.manage_item_button.pack(fill=tk.X, pady=5)

        self.manage_users_button = tk.Button(self.side_nav, text="Manage Users", font=('Arial', 14), bg="#2c3e50", fg="white", 
                                              relief=tk.FLAT, activebackground="yellow", command=self.show_manage_users_page)
        self.manage_users_button.pack(fill=tk.X, pady=5)

        self.logout_button = tk.Button(self.side_nav, text="Logout", font=('Arial', 14), bg="#2c3e50", fg="white", 
                                       relief=tk.FLAT, activebackground="yellow", command=self.logout)
        self.logout_button.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

    def clear_main_content(self):
        """Clears the main content frame.""" 
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def show_inventory_page(self):
        """Displays the inventory page.""" 
        self.clear_main_content()
        tk.Label(self.main_content, text="Inventory Page", font=('Arial', 18), bg="white").pack(pady=20)

    def show_sales_report_page(self):
        """Displays the sales report page.""" 
        self.clear_main_content()
        tk.Label(self.main_content, text="Sales Report Page", font=('Arial', 18), bg="white").pack(pady=20)

    def show_manage_item_page(self):
        # Clear the current frame
        print("Showing manage item page")
        print(f"Main content: {self.main_content}")
        self.clear_main_content()
        tk.Label(self.main_content, text="Sales Report Page", font=('Arial', 18), bg="white").pack(pady=20)
        if not hasattr(self, 'manage_item_page'):
            self.manage_item_page = ManageItems(self.main_content)
            self.manage_item_page.pack(fill="both", expand=True)
        else:
            self.manage_item_page.pack_forget()
            self.manage_item_page = ManageItems(self.main_content)
            self.manage_item_page.pack(fill="both", expand=True)

    def show_manage_users_page(self):
        """Displays the manage users page."""
        if self.account_type == 'employee':
            messagebox.showerror("Access Denied", "Only admin accounts can access this page.")
            return

        # If the user is an admin, show the management options
        if self.account_type == 'admin':
            self.clear_main_content()
            tk.Label(self.main_content, text="User Management", font=('Arial', 18), bg="white").pack(pady=20)

            # User list in table format
            self.user_table = ttk.Treeview(self.main_content, columns=("id", "first_name", "last_name", "username", "password", "account_type"), show="headings")
            self.user_table.pack(pady=10)
            self.user_table.heading("id", text="ID")
            self.user_table.heading("first_name", text="First Name")
            self.user_table.heading("last_name", text="Last Name")
            self.user_table.heading("username", text="Username")
            self.user_table.heading("password", text="Password")
            self.user_table.heading("account_type", text="Access Type")

            self.load_users_from_db()  # Load the users from the database

            # Buttons for user management
            self.add_user_button = tk.Button(self.main_content, text="Add User", command=self.add_user)
            self.add_user_button.pack(pady=5)

            self.update_user_button = tk.Button(self.main_content, text="Update User", command=self.update_user)
            self.update_user_button.pack(pady=5)

            self.delete_user_button = tk.Button(self.main_content, text="Delete User", command=self.delete_user)
            self.delete_user_button.pack(pady=5)

    def load_users_from_db(self):
        """Loads users from the database and populates the table.""" 
        for i in self.user_table.get_children():
            self.user_table.delete(i)  # Clear previous entries

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        
        for row in users:
            self.user_table.insert("", tk.END, values=row)

    def add_user(self):
        """Prompts for user details and adds a new user to the database.""" 
        details_window = tk.Toplevel(self.master)
        details_window.title("Add User")

        tk.Label(details_window, text="First Name:").pack()
        first_name_entry = tk.Entry(details_window)
        first_name_entry.pack()

        tk.Label(details_window, text="Last Name:").pack()
        last_name_entry = tk.Entry(details_window)
        last_name_entry.pack()

        tk.Label(details_window, text="Username:").pack()
        username_entry = tk.Entry(details_window)
        username_entry.pack()

        tk.Label(details_window, text="Password:").pack()
        password_entry = tk.Entry(details_window, show="*")
        password_entry.pack()

        tk.Label(details_window, text="Account Type:").pack()
        account_type_combo = ttk.Combobox(details_window, values=["employee", "admin"])
        account_type_combo.pack()

        def save_user():
            """Saves the new user to the database.""" 
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            username = username_entry.get()
            password = password_entry.get()
            account_type = account_type_combo.get()

            cursor = self.conn.cursor()
            try:
                cursor.execute("INSERT INTO users (first_name, last_name, username, password, account_type) VALUES (?, ?, ?, ?, ?)",
                               (first_name, last_name, username, password, account_type))
                self.conn.commit()
                messagebox.showinfo("Success", "User added successfully!")
                details_window.destroy()
                self.load_users_from_db()  # Refresh the user list
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists.")

        tk.Button(details_window, text="Save User", command=save_user).pack()

    def update_user(self):
        """Prompts for user details and updates the selected user in the database.""" 
        selected_item = self.user_table.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Select a user to update.")
            return

        user_data = self.user_table.item(selected_item)["values"]

        details_window = tk.Toplevel(self.master)
        details_window.title("Update User")

        tk.Label(details_window, text="First Name:").pack()
        first_name_entry = tk.Entry(details_window)
        first_name_entry.insert(0, user_data[1])
        first_name_entry.pack()

        tk.Label(details_window, text="Last Name:").pack()
        last_name_entry = tk.Entry(details_window)
        last_name_entry.insert(0, user_data[2])
        last_name_entry.pack()

        tk.Label(details_window, text="Username:").pack()
        username_entry = tk.Entry(details_window)
        username_entry.insert(0, user_data[3])
        username_entry.config(state='readonly')
        username_entry.pack()

        tk.Label(details_window, text="Password:").pack()
        password_entry = tk.Entry(details_window, show="*")
        password_entry.insert(0, user_data[4])
        password_entry.pack()

        tk.Label(details_window, text="Account Type:").pack()
        account_type_combo = ttk.Combobox(details_window, values=["employee", "admin"])
        account_type_combo.set(user_data[5])
        account_type_combo.pack()

        def save_updated_user():
            """Saves the updated user details to the database.""" 
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            password = password_entry.get()
            account_type = account_type_combo.get()

            cursor = self.conn.cursor()
            cursor.execute("UPDATE users SET first_name=?, last_name=?, password=?, account_type=? WHERE username=?",
                           (first_name, last_name, password, account_type, user_data[3]))
            self.conn.commit()
            messagebox.showinfo("Success", "User updated successfully!")
            details_window.destroy()
            self.load_users_from_db()

        tk.Button(details_window, text="Save Changes", command=save_updated_user).pack()

    def delete_user(self):
        """Deletes the selected user from the database.""" 
        selected_item = self.user_table.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Select a user to delete.")
            return

        user_data = self.user_table.item(selected_item)["values"]
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete {user_data[1]} {user_data[2]}?")
        if confirm:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM users WHERE id=?", (user_data[0],))
            self.conn.commit()
            self.load_users_from_db()

    def logout(self):
        """Logs out the user and returns to the login screen."""
        self.master.destroy()  # Close the current window (AdminPortal)  
        from pages.admin.login import LoginPage  # Import here to avoid circular import
        # Create a new instance of LoginPage or show it
        root = tk.Tk()
        LoginPage(root)  # Pass the root or master window to LoginPage
        root.mainloop()  # Start the Tkinter event loop for the new window   # Call the function to show the login window

# Example of initializing the AdminPortal with the account type
if __name__ == "__main__":
    root = tk.Tk()
    # Pass 'admin' or 'employee' based on the user's account type
    admin_portal = AdminPortal(root, account_type='admin')
    root.mainloop()

