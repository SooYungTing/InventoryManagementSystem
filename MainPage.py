import tkinter as tk
import sqlite3
from datetime import datetime

# create a connection to the database
conn = sqlite3.connect('inventory.db')

# create a cursor object to execute SQL commands
c = conn.cursor()

# create a table to store the form data
c.execute('''CREATE TABLE IF NOT EXISTS registration (
             item_num INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT,
             price TEXT,
             quantity TEXT,
             expiry_date TEXT)''')

# commit the changes and close the connection
conn.commit()
conn.close()

class Product:
    def __init__(self, item_num, name, price, quantity, ed):
        self.item_num = item_num
        self.name = name
        self.price = price
        self.quantity = quantity
        self.ed = ed


def add_product_to_db(item_num, name, price, quantity, ed):
    try:
        # create a connection to the database
        conn = sqlite3.connect('inventory.db')

        # create a cursor object to execute SQL commands
        c = conn.cursor()

        # execute SQL query to insert the product details into the database
        c.execute("INSERT INTO registration (item_num, name, price, quantity, expiry_date) VALUES (?, ?, ?, ?, ? )", (item_num, name, price, quantity, ed))

        # commit the changes and close the connection
        conn.commit()
        conn.close()
        print("Data inserted successfully")
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)

class InventoryGUI:
    def __init__(self, master):
        self.clear_fields = None
        self.master = master
        master.title("Inventory Management System")

        # Create label and entry for item number
        self.item_num_label = tk.Label(master, text="Item Number:")
        self.item_num_label.grid(row=0, column=0)
        self.item_num_entry = tk.Entry(master)
        self.item_num_entry.grid(row=0, column=1)

        # Create label and entry for product name
        self.name_label = tk.Label(master, text="Product Name:")
        self.name_label.grid(row=1, column=0)
        self.name_entry = tk.Entry(master)
        self.name_entry.grid(row=1, column=1)

        # Create label and entry for product price
        self.price_label = tk.Label(master, text="Product Price:")
        self.price_label.grid(row=2, column=0)
        self.price_entry = tk.Entry(master)
        self.price_entry.grid(row=2, column=1)

        # Create label and entry for product quantity
        self.quantity_label = tk.Label(master, text="Product Quantity:")
        self.quantity_label.grid(row=3, column=0)
        self.quantity_entry = tk.Entry(master)
        self.quantity_entry.grid(row=3, column=1)

        # Create label and entry for product expiry date
        self.ed_label = tk.Label(master, text="Expiry Date:")
        self.ed_label.grid(row=4, column=0)
        self.ed_entry = tk.Entry(master)
        self.ed_entry.grid(row=4, column=1)

        # Create buttons for add, remove, update, view, and search
        self.add_button = tk.Button(master, text="Add", command=self.add_product)
        self.add_button.grid(row=5, column=0)

        self.remove_button = tk.Button(master, text="Remove", command=self.remove_product)
        self.remove_button.grid(row=5, column=1)

        self.update_button = tk.Button(master, text="Update", command=self.update_product)
        self.update_button.grid(row=5, column=2)

        self.view_button = tk.Button(master, text="View All", command=self.view_products)
        self.view_button.grid(row=6, column=0)

        self.search_button = tk.Button(master, text="Search", command=self.search_product)
        self.search_button.grid(row=6, column=1)

        self.clear_button = tk.Button(master, text="Clear", command=self.clear_fields)
        self.clear_button.grid(row=6, column=2)

        # Create text box to display results
        self.result_textbox = tk.Text(master, width=50, height=10)
        self.result_textbox.grid(row=7, column=0, columnspan=3)

        # Create empty inventory
        self.inventory = []

    def add_product(self):
        item_num = self.item_num_entry.get()
        name = self.name_entry.get()
        price = float(self.price_entry.get())
        quantity = int(self.quantity_entry.get())
        ed = datetime.strptime(self.ed_entry.get(), '%Y/%m/%d')

        product = Product(item_num, name, price, quantity, ed)
        self.inventory.append(product)

        # insert the product into the database
        add_product_to_db(item_num, name, price, quantity, ed)

        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("end", f"{product.name} added to inventory.")

    def remove_product(self):
        item_num = self.item_num_entry.get()

        removed = False
        for product in self.inventory:
            if product.item_num == item_num:
                self.inventory.remove(product)
                removed = True
                break

        if removed:
            self.result_textbox.delete("1.0", "end")
            self.result_textbox.insert("end", f"{item_num} removed from inventory.")
        else:
            self.result_textbox.delete("1.0", "end")
            self.result_textbox.insert("end", f"{item_num} not found in inventory.")

    def update_product(self):
        item_num = self.item_num_entry.get()

        for product in self.inventory:
            if product.item_num == item_num:
                product.name = str(self.name_entry.get())
                product.price = float(self.price_entry.get())
                product.quantity = int(self.quantity_entry.get())
                ed = datetime.strptime(self.ed_entry.get(), '%Y/%m/%d')

                self.result_textbox.delete("1.0", "end")
                self.result_textbox.insert("end", f"{product.item_num} updated.")
                return

        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("end", f"{item_num} not found in inventory.")


    def view_products(self):
        # create a connection to the database
        conn = sqlite3.connect('inventory.db')

        # create a cursor object to execute SQL commands
        c = conn.cursor()

        # execute SQL query to retrieve all products from the database
        c.execute("SELECT * FROM registration")
        products = c.fetchall()

        self.result_textbox.delete("1.0", "end")

        if len(products) == 0:
            self.result_textbox.insert("end", "No products found in inventory.")
        else:
            for product in products:
                self.result_textbox.insert("end", f"Item Number: {product[0]}\n")
                self.result_textbox.insert("end", f"Product Name: {product[1]}\n")
                self.result_textbox.insert("end", f"Product Price: {product[2]}\n")
                self.result_textbox.insert("end", f"Product Quantity: {product[3]}\n")
                self.result_textbox.insert("end", f"Expiry Date: {product[4]}\n")
                self.result_textbox.insert("end", "\n")

        # close the connection
        conn.close()

    def search_product(self):
        item_num = self.item_num_entry.get()

        # create a connection to the database
        conn = sqlite3.connect('inventory.db')

        # create a cursor object to execute SQL commands
        c = conn.cursor()

        # execute SQL query to retrieve the product with the given item number
        c.execute("SELECT * FROM registration WHERE item_num = ?", (item_num,))
        product = c.fetchone()

        self.result_textbox.delete("1.0", "end")

        if product is not None:
            self.result_textbox.insert("end", f"Item Number: {product[0]}\n")
            self.result_textbox.insert("end", f"Product Name: {product[1]}\n")
            self.result_textbox.insert("end", f"Product Price: {product[2]}\n")
            self.result_textbox.insert("end", f"Product Quantity: {product[3]}\n")
            self.result_textbox.insert("end", f"Expiry Date: {product[4]}\n")
        else:
            self.result_textbox.insert("end", f"Product with item number {item_num} not found in inventory.")

        # close the connection
        conn.close()

        def clear_fields(self):
            self.item_num_entry.delete(0, "end")
            self.name_entry.delete(0, "end")
            self.price_entry.delete(0, "end")
            self.quantity_entry.delete(0, "end")
            self.ed_entry.delete(0, "end")
            
if __name__ == "__main__":
    root = tk.Tk()
    gui = InventoryGUI(root)
    root.mainloop()