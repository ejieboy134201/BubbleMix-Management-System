import tkinter as tk
from tkinter import messagebox
from pages.Customer.payment_page import PaymentPage

def show_confirmation_popup(master, total_amount, order_items, db_manager):
    popup = tk.Toplevel(master)
    popup.title("Order Confirmation")
    
    tk.Label(popup, text="Confirm Your Order:").pack()

    for product_name, price in order_items:
        tk.Label(popup, text=f"{product_name} - ${price}").pack()

    tk.Label(popup, text=f"Total Amount: ${total_amount}").pack()

    tk.Button(popup, text="Proceed", command=lambda: proceed_to_payment(popup, total_amount, db_manager)).pack()
    tk.Button(popup, text="Cancel", command=popup.destroy).pack()

def proceed_to_payment(popup, total_amount, db_manager):
    popup.destroy()
    
    payment_window = tk.Toplevel()
    PaymentPage(payment_window, total_amount, db_manager)
