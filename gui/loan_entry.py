import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from database.db import Database

class LoanEntryForm(tk.Toplevel):
    def __init__(self, master=None, on_submit=None):
        super().__init__(master)
        self.title("Add New Loan")
        self.geometry("400x400")
        self.on_submit = on_submit  # Optional callback after submission

        vcmd_float = (self.register(self.validate_float), "%P")
        vcmd_int = (self.register(self.validate_int), "%P")

        # Create and place labels and entry fields
        tk.Label(self, text="Loan Name:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self, text="Principal Amount:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.principal_entry = tk.Entry(self, validate="key", validatecommand=vcmd_float)
        self.principal_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self, text="Current Balance:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.balance_entry = tk.Entry(self, validate="key", validatecommand=vcmd_float)
        self.balance_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self, text="Interest Rate (%):").grid(row=3, column=0, padx=10, pady=5, sticky='e')
        self.interest_rate_entry = tk.Entry(self, validate="key", validatecommand=vcmd_float)
        self.interest_rate_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self, text="Monthly Minimum Payment:").grid(row=4, column=0, padx=10, pady=5, sticky='e')
        self.min_payment_entry = tk.Entry(self, validate="key", validatecommand=vcmd_float)
        self.min_payment_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(self, text="Extra Payment (optional):").grid(row=5, column=0, padx=10, pady=5, sticky='e')
        self.extra_payment_entry = tk.Entry(self, validate="key", validatecommand=vcmd_float)
        self.extra_payment_entry.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(self, text="First Due Date:").grid(row=6, column=0, padx=10, pady=5, sticky='e')
        self.first_due_date_entry = DateEntry(self, date_pattern="yyyy-mm-dd")
        self.first_due_date_entry.grid(row=6, column=1, padx=10, pady=5)

        # Submit button
        submit_button = tk.Button(self, text="Submit", command=self.submit_loan)
        submit_button.grid(row=7, column=0, columnspan=2, pady=10)

    def validate_float(self, value):
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False

    def validate_int(self, value):
        if value == "":
            return True
        return value.isdigit()

    def submit_loan(self):
        # Retrieve input values
        name = self.name_entry.get().strip()
        principal = self.principal_entry.get().strip()
        balance = self.balance_entry.get().strip()
        interest_rate = self.interest_rate_entry.get().strip()
        min_payment = self.min_payment_entry.get().strip()
        extra_payment = self.extra_payment_entry.get().strip() or "0"
        first_due_date = self.first_due_date_entry.get_date().strftime("%Y-%m-%d")

        # Validate required fields
        if not name or not principal or not balance or not interest_rate or not min_payment or not first_due_date:
            messagebox.showerror("Input Error", "Please fill in all required fields.")
            return

        # Validate numeric fields
        try:
            principal = float(principal)
            balance = float(balance)
            interest_rate = float(interest_rate)
            min_payment = float(min_payment)
            extra_payment = float(extra_payment)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for all numeric fields.")
            return

        # Insert into database
        db = Database()
        db.connect()
        insert_query = """
        INSERT INTO loans (name, principal, current_balance, interest_rate, monthly_min_payment, extra_payment, first_due_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        db.execute(insert_query, (name, principal, balance, interest_rate, min_payment, extra_payment, first_due_date))
        db.close()
        messagebox.showinfo("Success", "Loan added successfully.")
        if self.on_submit:
            self.on_submit()
        self.destroy()