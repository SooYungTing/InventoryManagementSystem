import tkinter as tk
import sqlite3


def login():
    employee_id = employee_id_entry.get()
    password = password_entry.get()

    # Connect to the database
    conn = sqlite3.connect("registration.db")
    cursor = conn.cursor()

    # Check if the employee ID and password match a record in the database
    cursor.execute("SELECT * FROM registration WHERE id=? AND password=?", (employee_id, password))
    record = cursor.fetchone()

    if record:
        # Successful login
        root.destroy()  # Close login window
        # Open inventory management system main window
        # Code goes here
    else:
        # Failed login
        error_label.config(text="Invalid Employee ID or password")

    # Close the database connection
    conn.close()



def open_registration_form():
    # Create registration form window
    import RegistrationForm
    registration_window = tk.Toplevel(root)
    registration_form = RegistrationForm.RegistrationForm(registration_window)


# Create login window
root = tk.Tk()
root.title("Inventory Management System")
root.geometry("300x200")

# Employee ID label and entry
employee_id_label = tk.Label(root, text="Employee ID")
employee_id_label.pack()
employee_id_entry = tk.Entry(root)
employee_id_entry.pack()

# Password label and entry
password_label = tk.Label(root, text="Password")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

# Login button
login_button = tk.Button(root, text="Login", command=login)
login_button.pack()

# New Employee Button
new_button = tk.Button(root, text="New Employee", command=open_registration_form)
new_button.pack()

# Error label (hidden by default)
error_label = tk.Label(root, text="", fg="red")
error_label.pack()
error_label.config(text="", font=("Times", 12, "bold"))

root.mainloop()
