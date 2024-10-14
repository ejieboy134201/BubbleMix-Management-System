import tkinter as tk
from tkinter import messagebox

class PaymentPage:
    def __init__(self, master, total_amount, db_manager):
        self.master = master
        self.master.title("Payment Page")

        self.db_manager = db_manager
        self.total_amount = total_amount
        self.customer_payment = tk.DoubleVar()

        tk.Label(self.master, text="Total Amount:").pack()
        tk.Label(self.master, text=f"${self.total_amount}").pack()

        tk.Label(self.master, text="Enter Payment Amount:").pack()
        tk.Entry(self.master, textvariable=self.customer_payment).pack()

        tk.Button(self.master, text="Proceed to Checkout", command=self.checkout).pack()
        tk.Button(self.master, text="Cancel Order", command=self.cancel_order).pack()

    def checkout(self):
        amount_received = self.customer_payment.get()
        if amount_received < self.total_amount:
            messagebox.showwarning("Insufficient Payment", "Please enter a sufficient amount.")
            return

        # Proceed to deduct from inventory and record sale
        for product_name, price in self.order_items:
            self.db_manager.update_item_quantity(product_name, 1)  # Deduct quantity here (assumed 1 for simplicity)
            self.db_manager.record_sale(product_name, 1, price, self.total_amount)

        messagebox.showinfo("Transaction Successful", "Thank you for your order!")
        self.master.destroy()

    def cancel_order(self):
        if messagebox.askyesno("Cancel Order", "Are you sure you want to cancel the order?"):
            self.master.destroy()
