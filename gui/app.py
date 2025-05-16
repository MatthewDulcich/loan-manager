import tkinter as tk
from tkinter import ttk, messagebox
from database.db import Database
from gui.loan_entry import LoanEntryForm
from models.loan import Loan
from strategies.snowball import SnowballStrategy
from strategies.avalanche import AvalancheStrategy
from strategies.custom_strategy import CustomStrategy
from gui.payoff_plan import PayoffPlanPopup

class LoanManagerApp(tk.Tk):
    def __init__(self, db=None):
        super().__init__()
        self.title("Loan Manager")
        self.geometry("800x600")

        self.db = db if db else Database()
        self.db.connect()

        # Strategy selection
        self.strategy_var = tk.StringVar(value="Snowball")
        strategy_options = ["Snowball", "Avalanche", "Custom"]
        self.strategy_combo = ttk.Combobox(self, textvariable=self.strategy_var, values=strategy_options, state="readonly")
        self.strategy_combo.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.strategy_combo.bind("<<ComboboxSelected>>", lambda e: self.load_loans())

        # Export button
        export_button = tk.Button(self, text="Export Payoff Plan", command=self.export_payoff_plan)
        export_button.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Treeview for loans
        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Principal", "Balance", "Interest Rate", "Min Payment", "Extra Payment", "First Due Date"), show='headings')
        self.tree.column("ID", width=0, stretch=False)  # Hide the ID column
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Add Loan button
        add_loan_button = tk.Button(self, text="Add Loan", command=self.open_add_loan_form)
        add_loan_button.grid(row=2, column=0, pady=5, sticky="w")

        # Delete Loan button
        delete_loan_button = tk.Button(self, text="Delete Loan", command=self.delete_selected_loan)
        delete_loan_button.grid(row=2, column=1, pady=5, sticky="e")

        self.load_loans()

    def get_strategy(self):
        strategy = self.strategy_var.get()
        if strategy == "Snowball":
            return SnowballStrategy()
        elif strategy == "Avalanche":
            return AvalancheStrategy()
        elif strategy == "Custom":
            # For demo, sort by name
            return CustomStrategy(loan_priority=[loan.id for loan in sorted(self.get_loans(), key=lambda l: l.name)])
        else:
            return SnowballStrategy()

    def get_loans(self):
        loans = self.db.fetchall("SELECT * FROM loans")
        return [Loan.from_row(row) for row in loans]

    def load_loans(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        loans = self.get_loans()
        strategy = self.get_strategy()
        if hasattr(strategy, "prioritize"):
            loans = strategy.prioritize(loans)
        for loan in loans:
            self.tree.insert('', 'end', values=(
                loan.id,  # Add ID as first value
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

    def delete_selected_loan(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Delete Loan", "Please select a loan to delete.")
            return
        loan_values = self.tree.item(selected[0])["values"]
        loan_id = loan_values[0]
        if messagebox.askyesno("Delete Loan", f"Are you sure you want to delete '{loan_values[1]}'?"):
            self.db.delete_loan(loan_id)
            self.load_loans()

    def export_payoff_plan(self):
        loans = self.get_loans()
        strategy = self.get_strategy()
        if hasattr(strategy, "generate_payment_plan"):
            plan = strategy.generate_payment_plan(loans)
            PayoffPlanPopup(self, plan, loans)
        else:
            tk.messagebox.showerror("Error", "Selected strategy does not support payoff plan export.")

if __name__ == "__main__":
    app = LoanManagerApp()
    app.mainloop()