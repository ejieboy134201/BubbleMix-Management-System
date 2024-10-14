import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import Frame
import sqlite3
from PIL import Image, ImageTk
import io

class ManageItems(Frame):
    def __init__(self, parent):
        super().__init__(parent)  # Call to parent class initializer
        self.parent = parent
        self.frame = Frame(self)  # Initialize the frame
        self.frame.pack(fill=tk.BOTH, expand=True)  # Pack the frame
        self.image_refs = {}
        self.image_data = None  # To store uploaded image data
        self.create_widgets()
    
    def delete_item(self):
            """Deletes the selected item from the database."""
            selected_item = self.item_table.selection()
            if not selected_item:
                messagebox.showerror("Error", "No item selected!")
                return
            
            item_id = self.item_table.item(selected_item)['values'][0]  # Get the selected item's ID

            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this item?"):
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM items WHERE id=?", (item_id,))
                self.conn.commit()
                messagebox.showinfo("Success", "Item deleted successfully!")
                self.load_items_from_db()  # Refresh item list

    def create_widgets(self):
        # Add borders to the table
        style = ttk.Style()
        style.configure("Treeview", bordercolor="black", borderwidth=4)

        # Change the color of the buttons
        style.configure("TButton", background="#2c3e50", foreground="white")
        style.map("TButton", background=[("active", "#3498db")])

        # Add buttons for item management
        self.add_item_button = tk.Button(self.frame, text="Add Item", command=self.add_item)
        self.add_item_button.pack(pady=5)

        # Create the item table with an additional column for images and quantity
        self.item_table = ttk.Treeview(self.frame, columns=("id", "product_name", "product_type", "variety", "description", "image", "quantity", "price"), show="headings")
        self.item_table.pack(pady=10)

        # Define table headings
        self.item_table.heading("id", text="ID")
        self.item_table.heading("product_name", text="Product Name")
        self.item_table.heading("product_type", text="Product Type")
        self.item_table.heading("variety", text="Variety")
        self.item_table.heading("description", text="Description")
        self.item_table.heading("image", text="Image")  # New column for images
        self.item_table.heading("quantity", text="Quantity")  # New quantity column
        self.item_table.heading("price", text="Price")

        # Set column widths and add a style for borders
        self.item_table.column("id", width=50)
        self.item_table.column("product_name", width=150)
        self.item_table.column("product_type", width=100)
        self.item_table.column("variety", width=100)
        self.item_table.column("description", width=200)
        self.item_table.column("image", width=50)  # Width for the image column
        self.item_table.column("quantity", width=80)  # Width for the quantity column
        self.item_table.column("price", width=80)

        # Add borders to the table
        style = ttk.Style()
        style.configure("Treeview", bordercolor="black", borderwidth=1)
        self.item_table["show"] = "headings"  # Show only headings
        self.item_table["selectmode"] = "browse"  # Allow single selection

        # Add buttons for item management
        self.add_item_button = tk.Button(self.frame, text="Add Item", command=self.add_item)
        self.add_item_button.pack(pady=5)

        self.update_item_button = tk.Button(self.frame, text="Update Item", command=self.update_item)
        self.update_item_button.pack(pady=5)

        self.delete_item_button = tk.Button(self.frame, text="Delete Item", command=self.delete_item)
        self.delete_item_button.pack(pady=5)

        # Setup database connection
        self.conn = sqlite3.connect('manage_items.db')
        self.create_items_table()

        # Load items from database
        self.load_items_from_db()

    def create_items_table(self):
        """Creates the items table in the database if it doesn't exist."""
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                product_type TEXT NOT NULL,
                variety TEXT NOT NULL,
                description TEXT NOT NULL,
                quantity INTEGER NOT NULL, 
                price REAL NOT NULL,
                image BLOB  -- For storing images as binary
            )''')
        self.conn.commit()

    def load_items_from_db(self):
        """Loads items from the database and populates the table."""
        for i in self.item_table.get_children():
            self.item_table.delete(i)  # Clear previous entries

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()

        for row in items:
            # Ensure that the row has the correct number of elements
            if len(row) < 8:
                print(f"Row has insufficient data: {row}")
                continue  # Skip this row if it doesn't have enough data

            # Convert BLOB to Image for display
            image = None
            if row[7]:  # If there's an image stored
                image = Image.open(io.BytesIO(row[7]))  # Convert BLOB to Image
                image.thumbnail((50, 50))  # Resize image to fit in the table
                image = ImageTk.PhotoImage(image)

                # Keep a reference to the image
                self.image_refs[row[0]] = image  # row[0] is the item ID

            # Insert values into the table
            self.item_table.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4], '', row[5], row[6]))  # Add '' for the image cell

            # Update the image in the table after inserting the row
            self.item_table.item(self.item_table.get_children()[-1], image=image if image else '')



    def add_item(self):
        """Prompts for item details and adds a new item to the database."""
        details_window = tk.Toplevel(self.parent)
        details_window.title("Add Item")

        # Input fields for item details
        tk.Label(details_window, text="Product Name:").pack()
        product_name_entry = tk.Entry(details_window)
        product_name_entry.pack()

        tk.Label(details_window, text="Product Type:").pack()
        product_type_entry = ttk.Combobox(details_window, values=["Food", "Beverages"])
        product_type_entry.pack()

        tk.Label(details_window, text="Variety:").pack()
        variety_entry = ttk.Combobox(details_window)  # Using Combobox for variety selection
        variety_entry.pack()

        # Update varieties based on product type
        def update_varieties(event):
            if product_type_entry.get() == "Food":
                variety_entry['values'] = ["Pasta", "Meal", "Pizzas", "Sandwiches", "Doughnuts"]
            elif product_type_entry.get() == "Beverages":
                variety_entry['values'] = ["Milktea", "Coffee", "Soda", "Cocktails"]
            variety_entry.current(0)  # Select first item by default

        product_type_entry.bind("<<ComboboxSelected>>", update_varieties)

        tk.Label(details_window, text="Description:").pack()
        description_entry = tk.Entry(details_window)
        description_entry.pack()

        tk.Label(details_window, text="Quantity:").pack()
        quantity_entry = tk.Entry(details_window)
        quantity_entry.pack()

        tk.Label(details_window, text="Price:").pack()
        price_entry = tk.Entry(details_window)
        price_entry.pack()

        # Upload image button
        tk.Label(details_window, text="Image:").pack()  # Label for image
        self.image_label = tk.Label(details_window, text="No image selected")
        self.image_label.pack()

        upload_image_button = tk.Button(details_window, text="Upload Image", command=lambda: self.upload_image(details_window))
        upload_image_button.pack()

        def remove_image():
            """Removes the selected image and updates the label."""
            self.image_data = None  # Clear the image data
            self.image_label.config(text="No image selected")  # Update the label

        remove_image_button = tk.Button(details_window, text="Remove Image", command=remove_image)
        remove_image_button.pack()

        def save_item():
            """Saves the new item to the database, including the image."""
            try:
                product_name = product_name_entry.get()
                product_type = product_type_entry.get()
                variety = variety_entry.get()
                description = description_entry.get()
                quantity = int(quantity_entry.get())  # This could raise a ValueError
                price = float(price_entry.get())  # This could raise a ValueError

                # Validate that all fields are filled
                if not all([product_name, product_type, variety, description, quantity, price, self.image_data]):
                    raise ValueError("All fields must be filled!")

                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO items (product_name, product_type, variety, description, quantity, price, image) VALUES (?, ?, ?, ?, ?, ?, ?) ",
                               (product_name, product_type, variety, description, quantity, price, self.image_data))
                self.conn.commit()
                messagebox.showinfo("Success", "Item added successfully!")
                details_window.destroy()
                self.load_items_from_db()  # Refresh the item list

            except ValueError as ve:
                messagebox.showerror("Input Error", str(ve))
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        tk.Button(details_window, text="Save Item", command=save_item).pack()

    def upload_image(self, details_window):
        """Opens a file dialog to select an image file."""
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:  # If an image is selected
            with open(file_path, 'rb') as file:
                self.image_data = file.read()  # Read the image as binary
            self.image_label.config(text="Image uploaded successfully!")  # Update label with status

    def update_item(self):
        """Prompts for updated item details and updates the selected item in the database."""
        selected_item = self.item_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected!")
            return
        
        item_id = self.item_table.item(selected_item)['values'][0]
        details_window = tk.Toplevel(self.parent)
        details_window.title("Update Item")

        # Fetch current item details
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM items WHERE id=?", (item_id,))
        item = cursor.fetchone()

        # Input fields for item details
        tk.Label(details_window, text="Product Name:").pack()
        product_name_entry = tk.Entry(details_window)
        product_name_entry.insert(0, item[1])  # Fill current value
        product_name_entry.pack()

        tk.Label(details_window, text="Product Type:").pack()
        product_type_entry = ttk.Combobox(details_window, values=["Food", "Beverages"])
        product_type_entry.set(item[2])  # Fill current value
        product_type_entry.pack()

        tk.Label(details_window, text="Variety:").pack()
        variety_entry = ttk.Combobox(details_window)
        variety_entry.set(item[3])  # Fill current value
        variety_entry.pack()

        tk.Label(details_window, text="Description:").pack()
        description_entry = tk.Entry(details_window)
        description_entry.insert(0, item[4])  # Fill current value
        description_entry.pack()

        tk.Label(details_window, text="Quantity:").pack()
        quantity_entry = tk.Entry(details_window)
        quantity_entry.insert(0, item[5])  # Fill current value
        quantity_entry.pack()

        tk.Label(details_window, text="Price:").pack()
        price_entry = tk.Entry(details_window)
        price_entry.insert(0, item[6])  # Fill current value
        price_entry.pack()

        # Show current image
        current_image = Image.open(io.BytesIO(item[7])) if item[7] else None
        if current_image:
            current_image.thumbnail((50, 50))
            current_image = ImageTk.PhotoImage(current_image)
            tk.Label(details_window, image=current_image).pack()
            details_window.image = current_image  # Keep a reference to the image

        tk.Label(details_window, text="New Image:").pack()
        self.image_label = tk.Label(details_window, text="No image selected")
        self.image_label.pack()

        upload_image_button = tk.Button(details_window, text="Upload Image", command=lambda: self.upload_image(details_window))
        upload_image_button.pack()

        def save_updated_item():
            """Saves the updated item details to the database."""
            try:
                product_name = product_name_entry.get()
                product_type = product_type_entry.get()
                variety = variety_entry.get()
                description = description_entry.get()
                quantity = int(quantity_entry.get())  # Validate quantity as integer
                price = float(price_entry.get())  # Validate price as float

                if not all([product_name, product_type, variety, description, quantity, price]):
                    raise ValueError("All fields must be filled!")

                # Update the item in the database
                cursor.execute("UPDATE items SET product_name=?, product_type=?, variety=?, description=?, quantity=?, price=?, image=? WHERE id=?",
                               (product_name, product_type, variety, description, quantity, price, self.image_data, item_id))
                self.conn.commit()
                messagebox.showinfo("Success", "Item updated successfully!")
                details_window.destroy()
                self.load_items_from_db()  # Refresh item list

            except ValueError as ve:
                messagebox.showerror("Input Error", str(ve))
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        tk.Button(details_window, text="Update Item", command=save_updated_item).pack()

        


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Item Management System")
    ManageItems(root).pack(fill=tk.BOTH, expand=True)
    root.mainloop()