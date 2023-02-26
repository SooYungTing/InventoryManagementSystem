import tkinter as tk
import sqlite3
from datetime import datetime


# create a connection to the database
conn = sqlite3.connect('inventory.db')

# create a cursor object to execute SQL commands
c = conn.cursor()

# create a table to store the form data
c.execute('''CREATE TABLE IF NOT EXISTS inventory (
             item_num INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT,
             price REAL,
             quantity INTEGER,
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
        c.execute("INSERT INTO inventory (item_num, name, price, quantity, expiry_date) VALUES (?, ?, ?, ?, ? )",
                  (item_num, name, price, quantity, ed))

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
        self.ed_label = tk.Label(master, text="Expiry Date (YYYY/MM/DD):")
        self.ed_label.grid(row=4, column=0)
        self.ed_entry = tk.Entry(master)
        self.ed_entry.grid(row=4, column=1)

        # set self.clear_fields to a function that clears all entry fields
        self.clear_fields = self._clear_fields

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

        try:
            # create a connection to the database
            conn = sqlite3.connect('inventory.db')

            # create a cursor object to execute SQL commands
            c = conn.cursor()

            # execute SQL query to delete the product from the database
            c.execute("DELETE FROM inventory WHERE item_num=?", (item_num,))

            # commit the changes and close the connection
            conn.commit()
            conn.close()

            for i, product in enumerate(self.inventory):
                if product.item_num == item_num:
                    del self.inventory[i]
                    break

            self.result_textbox.delete("1.0", "end")
            self.result_textbox.insert("end", f"Product with item number {item_num} removed from inventory.")
        except sqlite3.Error as error:
            print("Failed to remove product from sqlite table", error)
            self.result_textbox.delete("1.0", "end")
            self.result_textbox.insert("end", f"Failed to remove product with item number {item_num}.")

    def update_product(self):
        item_num = self.item_num_entry.get()
        name = self.name_entry.get()
        price = float(self.price_entry.get())
        quantity = int(self.quantity_entry.get())
        ed = datetime.strptime(self.ed_entry.get(), '%Y/%m/%d')

        try:
            # create a connection to the database
            conn = sqlite3.connect('inventory.db')

            # create a cursor object to execute SQL commands
            c = conn.cursor()

            # execute SQL query to update the product details in the database
            c.execute("UPDATE inventory SET name=?, price=?, quantity=?, expiry_date=? WHERE item_num=?",
                      (name, price, quantity, ed, item_num))

            # commit the changes and close the connection
            conn.commit()
            conn.close()

            # Update the corresponding product in the inventory list
            for i, product in enumerate(self.inventory):
                if product.item_num == item_num:
                    self.inventory[i] = Product(item_num, name, price, quantity, ed)

            self.result_textbox.delete("1.0", "end")
            self.result_textbox.insert("end", f"{name} updated successfully.")
        except sqlite3.Error as error:
            print("Failed to update data into sqlite table", error)

    def view_products(self):
        # clear the result textbox
        self.result_textbox.delete("1.0", "end")

        try:
            # create a connection to the database
            conn = sqlite3.connect('inventory.db')

            # create a cursor object to execute SQL commands
            c = conn.cursor()

            # execute SQL query to select all products from the database
            c.execute("SELECT * FROM inventory")

            # fetch all the rows from the database
            rows = c.fetchall()

            # print the rows
            for row in rows:
                product = Product(row[0], row[1], row[2], row[3], row[4])
                self.inventory.append(product)
                self.result_textbox.insert("end",
                                               f"{product.item_num}, {product.name}, {product.price}, {product.quantity}, {product.ed}\n")

                # close the connection
            conn.close()
        except sqlite3.Error as error:
            print("Failed to select data from sqlite table", error)

    def search_product(self):
        item_num = self.item_num_entry.get()

        try:
            # create a connection to the database
            conn = sqlite3.connect('inventory.db')

            # create a cursor object to execute SQL commands
            c = conn.cursor()

            # execute SQL query to retrieve the product from the database
            c.execute("SELECT * FROM inventory WHERE item_num=?", (item_num))
            row = c.fetchall()

            # close the connection
            conn.close()

            # check if product exists in inventory
            if row is not None:
                # clear the result textbox
                self.result_textbox.delete("1.0", "end")

                # display the product details in the result textbox
                item_num = row

                self.result_textbox.insert("end", f"Item Number: {item_num}\n")
                
            else:
                self.result_textbox.delete("1.0", "end")
                self.result_textbox.insert("end", "Product not found.")
        except sqlite3.Error as error:
            print("Failed to search product in sqlite table", error)


    def _clear_fields(self):
        self.item_num_entry.delete(0, "end")
        self.name_entry.delete(0, "end")
        self.price_entry.delete(0, "end")
        self.quantity_entry.delete(0, "end")
        self.ed_entry.delete(0, "end")
        self.result_textbox.delete("1.0", "end")

if __name__ == "__main__":
    root = tk.Tk()
    gui = InventoryGUI(root)
    root.mainloop()