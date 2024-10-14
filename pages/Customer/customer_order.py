import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from pages.Customer.db_manager import DatabaseManager
from pages.Customer.popup_confirmation import show_confirmation_popup


class CustomerOrder:
    def __init__(self, master):
        self.master = master
        self.master.title("Milk Tea Ordering System")
       
        # Set the window size to 1024x768
        self.master.geometry("1024x768")


        # Center the window on the screen
        self.center_window()


        # Initialize the database manager
        self.db_manager = DatabaseManager('database/Ordering_system.db')
       
        self.order_items = []


        self.dine_in_var = tk.IntVar()
        self.dine_out_var = tk.IntVar()


        self.create_widgets()


    def center_window(self):
        # Get the width and height of the screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
       
        # Calculate the x and y coordinates to center the window
        x = (screen_width // 2) - (1024 // 2)
        y = (screen_height // 2) - (768 // 2)
       
        # Set the position of the window
        self.master.geometry(f"1024x768+{x}+{y}")


    def create_widgets(self):
        tk.Label(self.master, text="Select Order Type:", font=('Arial', 16)).pack(pady=20)
       
        tk.Radiobutton(self.master, text="Dine In", variable=self.dine_in_var, value=1, font=('Arial', 14)).pack(anchor=tk.W)
        tk.Radiobutton(self.master, text="Dine Out", variable=self.dine_out_var, value=2, font=('Arial', 14)).pack(anchor=tk.W)


        tk.Label(self.master, text="Menu:", font=('Arial', 16)).pack(pady=20)


        # Create the item_table for displaying menu items
        self.item_table = ttk.Treeview(self.master, columns=('Type', 'Name', 'Description', 'Price'), show='headings')
        self.item_table.heading('Type', text='Type')
        self.item_table.heading('Name', text='Name')
        self.item_table.heading('Description', text='Description')
        self.item_table.heading('Price', text='Price')


        # Add demo items to the item_table
        demo_items = [
            ("Beverages", "Classic Milk Tea", "Classic Milk Tea", 300.00),
            ("Beverages", "Passion Fruit Tea", "Passion Fruit Tea", 500.00),
            ("Food", "Beef doughnut", "Smoked Beef Doughnut", 513.00)
        ]


        for item in demo_items:
            self.item_table.insert('', tk.END, values=item)


        self.item_table.pack(pady=10)


        # Button to add the selected item to the order
        tk.Button(self.master, text="Add to Order", command=self.add_to_order, font=('Arial', 14)).pack(pady=10)


        # Create the final_order_table for displaying orders
        tk.Label(self.master, text="Final Orders:", font=('Arial', 16)).pack(pady=20)
       
        self.final_order_table = ttk.Treeview(self.master, columns=('Name', 'Quantity', 'Total Price'), show='headings')
        self.final_order_table.heading('Name', text='Name')
        self.final_order_table.heading('Quantity', text='Quantity')
        self.final_order_table.heading('Total Price', text='Total Price')


        self.final_order_table.pack(pady=10)


        tk.Button(self.master, text="Proceed to Payment", command=self.proceed_to_payment, font=('Arial', 14)).pack(pady=20)


    def add_to_order(self):
        # Get the selected item from the item_table
        selected_item = self.item_table.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an item from the menu.")
            return


        # Get item details
        item_details = self.item_table.item(selected_item)['values']
        item_name = item_details[1]
        item_price = item_details[3]


        # Prompt the user for quantity
        quantity = simpledialog.askinteger("Quantity", f"Enter the quantity for {item_name}:", minvalue=1)
        if quantity is None:
            return  # User cancelled the dialog


        # Calculate total price
        total_price = item_price * quantity


        # Add to final orders table
        self.final_order_table.insert('', tk.END, values=(item_name, quantity, total_price))
        self.order_items.append((item_name, quantity, total_price))


        messagebox.showinfo("Order Added", f"{quantity} x {item_name} added to order.")


    def proceed_to_payment(self):
        if not self.order_items:
            messagebox.showwarning("No Items", "Please add items to your order.")
            return


        total_amount = sum(price for _, _, price in self.order_items)
        show_confirmation_popup(self.master, total_amount, self.order_items, self.db_manager)


    def close_app(self):
        self.master.destroy()  # Close the application


    def minimize_app(self):
        self.master.iconify()  # Minimize the application


if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerOrder(root)
    root.mainloop()
