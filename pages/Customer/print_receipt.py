import tkinter as tk

class PrintReceipt:
    def __init__(self, master, order_details):
        self.master = master
        self.master.title("Receipt")

        tk.Label(self.master, text="Receipt", font=("Arial", 16)).pack()

        for detail in order_details:
            tk.Label(self.master, text=detail).pack()

        tk.Button(self.master, text="Print", command=self.print_receipt).pack()

    def print_receipt(self):
        # Placeholder for printing logic
        print("Receipt printed!")  # Replace with actual printing logic
