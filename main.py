from pages.Customer.db_setup import setup_database
from pages.Customer.customer_order import CustomerOrder
from pages.admin.admin_panel import AdminPortal
from pages.admin.login import LoginPage
import tkinter as tk

if __name__ == "__main__":
    setup_database()
    
    root = tk.Tk()
    app = LoginPage(root)
    root.mainloop()
