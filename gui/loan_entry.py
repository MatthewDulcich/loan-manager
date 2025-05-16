import tkinter as tk
from tkinter import messagebox
from database.db import Database

class LoanEntryForm(tk.Toplevel):
    def __init__(self, master=None, on_submit=None):
        super().__init__(master)
        self.title("Add New Loan")
        self.geometry("400x400")
        self.on_submit = on_submit  # Optional callback after submission

        # Create and place labels and entry fields
        tk.Label(self, text="Loan Name:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self, text="Principal Amount:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.principal_entry = tk.Entry(self)
        self.principal_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self, text="Current Balance:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.balance_entry = tk.Entry(self)
        self.balance_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self, text="Interest Rate (%):").grid(row=3, column=0, padx=10, pady=5, sticky='e')
        self.interest_rate_entry = tk.Entry(self)
        self.interest_rate_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self, text="Monthly Minimum Payment:").grid(row=4, column=0, padx=10, pady=5, sticky='e')
        self.min_payment_entry = tk.Entry(self)
        self.min_payment_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(self, text="Extra Payment (optional):").grid(row=5, column=0, padx=10, pady=5, sticky='e')
        self.extra_payment_entry = tk.Entry(self)
        self.extra_payment_entry.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(self, text="First Due Date (YYYY-MM-DD):").grid(row=6, column=0, padx=10, pady=5, sticky='e')
        self.first_due_date_entry = tk.Entry(self)
        self.first_due_date_entry.grid(row=6, column=1, padx=10, pady=5)

        # Submit button
        submit_button = tk.Button(self, text="Submit", command=self.submit_loan)
        submit_button.grid(row=7, column=0, columnspan=2, pady=10)

    def submit_loan(self):
        # Retrieve input values
        name = self.name_entry.get()
        principal = self.principal_entry.get()
        balance = self.balance_entry.get()
        interest_rate = self.interest_rate_entry.get()
        min_payment = self.min_payment_entry.get()
        extra_payment = self.extra_payment_entry.get()
        first_due_date = self.first_due_date_entry.get()

        # Validate inputs (basic example)
        if not name or not principal or not balance or not interest_rate or not min_payment or not first_due_date:
            messagebox.showerror("Input Error", "Please fill in all required fields.")
            return

        # Insert into database
        db = Database()
        db.connect()
        insert_query = """
        INSERT INTO loans (name, principal, current_balance, interest_rate, monthly_min_payment, extra_payment, first_due_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        db.execute(insert_query, (name, float(principal), float(balance), float(interest_rate), float(min_payment), float(extra_payment or 0), first_due_date))
        db.close()
        messagebox.showinfo("Success", "Loan added successfully.")
        if self.on_submit:
            self.on_submit()
        self.destroy()