import tkinter as tk
from tkcalendar import DateEntry
import sqlite3

# create a connection to the database
conn = sqlite3.connect('registration.db')

# create a cursor object to execute SQL commands
c = conn.cursor()

# create a table to store the form data
c.execute('''CREATE TABLE IF NOT EXISTS registration (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT,
             employee_id TEXT,
             email TEXT,
             phone TEXT,
             gender TEXT,
             date_of_entry TEXT,
             password TEXT,
             date_of_birth TEXT)''')

# commit the changes and close the connection
conn.commit()
conn.close()

class RegistrationForm:
    def __init__(self, master):
        self.master = master
        master.title("Registration Form")

        # create form labels
        self.name_label = tk.Label(master, text="Name:")
        self.employee_ID_label = tk.Label(master, text="Employee ID:")
        self.email_label = tk.Label(master, text="Email:")
        self.phone_label = tk.Label(master, text="Phone:")
        self.gender_label = tk.Label(master, text="Gender:")
        self.doe_label = tk.Label(master, text="Date of Entry:")
        self.password_label = tk.Label(master, text="Password:")
        self.dob_label = tk.Label(master, text="Date of Birth:")
        # create form inputs
        self.name_entry = tk.Entry(master)
        self.employee_ID_entry = tk.Entry(master)
        self.email_entry = tk.Entry(master)
        self.phone_entry = tk.Entry(master)
        self.gender_var = tk.StringVar(master)
        self.gender_var.set("Gender")  # set the default value of the option
        self.gender_option = tk.OptionMenu(master, self.gender_var, "Male", "Female")
        self.doe_picker = DateEntry(master, width=12, background='skyblue', foreground='black',
                                    date_pattern='dd/mm/yyyy')
        self.password_entry = tk.Entry(master, show="*")
        self.dob_picker = DateEntry(master, width=12, background='skyblue', foreground='black',
                                    date_pattern='dd/mm/yyyy')

        # create submit button
        self.submit_button = tk.Button(master, text="Submit", command=self.submit_form)

        # arrange form elements using grid layout
        self.name_label.grid(row=0, column=0)
        self.name_entry.grid(row=0, column=1)
        self.employee_ID_label.grid(row=1, column=0)
        self.employee_ID_entry.grid(row=1, column=1)
        self.email_label.grid(row=2, column=0)
        self.email_entry.grid(row=2, column=1)
        self.phone_label.grid(row=3, column=0)
        self.phone_entry.grid(row=3, column=1)
        self.password_label.grid(row=0, column=2)
        self.password_entry.grid(row=0, column=3)
        self.dob_label.grid(row=1, column=2)
        self.dob_picker.grid(row=1, column=3)
        self.doe_label.grid(row=2, column=2)
        self.doe_picker.grid(row=2, column=3)
        self.gender_label.grid(row=3, column=2)
        self.gender_option.grid(row=3, column=3)
        self.submit_button.grid(row=4, column=0, columnspan=4, sticky="nsew")

    def submit_form(self):
        # handle form submission here
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        employee_id = self.employee_ID_entry.get()
        gender = self.gender_var.get()
        dob = self.dob_picker.get_date().strftime('%d/%m/%Y')
        doe = self.doe_picker.get_date().strftime('%d/%m/%Y')
        password = self.password_entry.get()

        # insert the form data into the registration table
        conn = sqlite3.connect('registration.db')
        c = conn.cursor()

        c.execute(
            "INSERT INTO registration (name, employee_id, email, phone, gender, date_of_entry, password, date_of_birth) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (name, employee_id, email, phone, gender, doe, password, dob)
        )

        conn.commit()
        conn.close()

        # print a success message
        print("Form submitted successfully!")


# create main window
root = tk.Tk()

# create registration form
registration_form = RegistrationForm(root)

# run main loop
root.mainloop()

