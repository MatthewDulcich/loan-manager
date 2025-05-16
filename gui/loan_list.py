import tkinter as tk
from tkinter import ttk
from database.db import Database
from gui.loan_entry import LoanEntryForm  # Assuming this is your loan entry form

class LoanListView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Loan List")
        self.geometry("800x400")

        # Create Treeview
        columns = ("id", "name", "principal", "current_balance", "interest_rate", "monthly_min_payment", "extra_payment", "first_due_date")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add buttons
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, pady=5)
        tk.Button(button_frame, text="Add New Loan", command=self.open_add_loan).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Refresh", command=self.load_loans).pack(side=tk.LEFT)

        self.load_loans()

    def load_loans(self):
        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Fetch data from database
        db = Database()
        db.connect()
        loans = db.fetchall("SELECT * FROM loans")
        db.close()

        # Insert data into Treeview
        for loan in loans:
            self.tree.insert("", tk.END, values=(
                loan["id"],
                loan["name"],
                loan["principal"],
                loan["current_balance"],
                loan["interest_rate"],
                loan["monthly_min_payment"],
                loan["extra_payment"],
                loan["first_due_date"]
            ))

    def open_add_loan(self):
        def on_submit():
            self.load_loans()
        LoanEntryForm(master=self, on_submit=on_submit)