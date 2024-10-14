import tkinter as tk
from tkinter import messagebox
from db_manager import add_product

def add_product_page():
    def save_product():
        name = name_entry.get()
        description = desc_entry.get()
        price = float(price_entry.get())
        quantity = int(quantity_entry.get())
        add_product(name, description, price, quantity)
        messagebox.showinfo("Success", "Product added successfully!")

    root = tk.Tk()
    root.title("Add Product")

    name_label = tk.Label(root, text="Product Name:")
    name_label.pack(pady=5)
    name_entry = tk.Entry(root)
    name_entry.pack(pady=5)

    desc_label = tk.Label(root, text="Product Description:")
    desc_label.pack(pady=5)
    desc_entry = tk.Entry(root)
    desc_entry.pack(pady=5)

    price_label = tk.Label(root, text="Product Price:")
    price_label.pack(pady=5)
    price_entry = tk.Entry(root)
    price_entry.pack(pady=5)

    quantity_label = tk.Label(root, text="Product Quantity:")
    quantity_label.pack(pady=5)
    quantity_entry = tk.Entry(root)
    quantity_entry.pack(pady=5)

    save_button = tk.Button(root, text="Save", command=save_product)
    save_button.pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    add_product_page()
