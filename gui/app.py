import tkinter as tk
from tkinter import ttk
from database.db import Database
from gui.loan_entry import LoanEntryForm
from models.loan import Loan

class LoanManagerApp(tk.Tk):
    def __init__(self, db=None):
        super().__init__()
        self.title("Loan Manager")
        self.geometry("800x600")

        # Initialize the database
        self.db = db if db else Database()
        self.db.connect()

        # Create the Treeview to display loans
        self.tree = ttk.Treeview(self, columns=("Name", "Principal", "Balance", "Interest Rate", "Min Payment", "Extra Payment", "First Due Date"), show='headings')
        self.tree.heading("Name", text="Loan Name")
        self.tree.heading("Principal", text="Principal")
        self.tree.heading("Balance", text="Current Balance")
        self.tree.heading("Interest Rate", text="Interest Rate (%)")
        self.tree.heading("Min Payment", text="Monthly Min Payment")
        self.tree.heading("Extra Payment", text="Extra Payment")
        self.tree.heading("First Due Date", text="First Due Date")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Add Loan button
        add_loan_button = tk.Button(self, text="Add Loan", command=self.open_add_loan_form)
        add_loan_button.pack(pady=5)

        # Load existing loans
        self.load_loans()

    def load_loans(self):
        # Clear existing entries
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch loans from the database
        loans = self.db.fetchall("SELECT * FROM loans")
        for loan_row in loans:
            loan = Loan.from_row(loan_row)
            self.tree.insert('', 'end', values=(
                loan.name,
                f"${loan.principal:,.2f}",
                f"${loan.current_balance:,.2f}",
                f"{loan.interest_rate:.2f}",
                f"${loan.monthly_min_payment:,.2f}",
                f"${loan.extra_payment:,.2f}",
                loan.first_due_date.strftime("%Y-%m-%d")
            ))

    def open_add_loan_form(self):
        def on_submit():
            self.load_loans()
        LoanEntryForm(master=self, db=self.db, on_submit=on_submit)

if __name__ == "__main__":
    app = LoanManagerApp()
    app.mainloop()