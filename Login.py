import tkinter as tk

def login():
    EmployeeeID = employee_ID_entry.get()
    password = password_entry.get()

    # Code to verify username and password goes here
    if EmployeeeID == "admin" and password == "password":
        # Successful login
        root.destroy()  # Close login window
        # Open inventory management system main window
        # Code goes here
    else:
        # Failed login
        error_label.config(text="Invalid Employee ID or password")

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
employee_ID_label = tk.Label(root, text="Employee ID")
employee_ID_label.pack()
employee_ID_entry = tk.Entry(root)
employee_ID_entry.pack()

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
