import tkinter as tk
import sqlite3
import pandas as pd


class InventoryManagementSystem(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Inventory Management System")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Welcome to the Inventory Management System!", font = ("Times", 20, "bold"))
        self.label.pack()

        self.product_button = tk.Button(self, text="Product", command=self.product_item)
        self.product_button.pack()

        self.analysis_button = tk.Button(self, text="Analysis", command=self.analysis_item)
        self.analysis_button.pack()

        self.download_button = tk.Button(self, text="Download Inventory", command=self.download_inventory)
        self.download_button.pack()

        self.quit_button = tk.Button(self, text="Quit", command=self.master.destroy)
        self.quit_button.pack()

    def product_item(self):
        import MainPage
        Main_window = tk.Toplevel(root)
        MainPage = MainPage.InventoryGUI(Main_window)

    def analysis_item(self):
        import Analysis

    def download_inventory(self):
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()

        # Create 'items' table if it does not exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                Item_Number INTEGER NOT NULL,
                Name TEXT NOT NULL,
                Quantity INTEGER NOT NULL,
                Price REAL NOT NULL,
                Expiry_Date TEXT
            )
        ''')

        cursor.execute("SELECT * FROM inventory")
        results = cursor.fetchall()

        if len(results) == 0:
            print("No data found in the 'inventory' table.")
            return

        df = pd.DataFrame(results, columns=['Item_Number', 'Name', 'Quantity', 'Price', 'Expiry_Date'])

        if df.empty:
            print("The dataframe is empty.")
            return

        writer = pd.ExcelWriter('inventory.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Inventory', index=False)
        writer.save()
        writer.close()
        conn.close()

        print(f"{len(results)} rows saved to 'inventory.xlsx'.")
        print("Download complete.")


root = tk.Tk()
app = InventoryManagementSystem(master=root)
app.mainloop()
