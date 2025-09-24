import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os
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

        # Import CSV button
        import_csv_button = tk.Button(self, text="Import CSV", command=self.import_from_csv)
        import_csv_button.grid(row=2, column=1, pady=5)

        # CSV Help button
        csv_help_button = tk.Button(self, text="CSV Format Help", command=self.show_csv_format_help)
        csv_help_button.grid(row=3, column=0, pady=2, sticky="w")

        # Delete Loan button
        delete_loan_button = tk.Button(self, text="Delete Loan", command=self.delete_selected_loan)
        delete_loan_button.grid(row=3, column=1, pady=2, sticky="e")

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

    def import_from_csv(self):
        """Import loans from a CSV file."""
        file_path = filedialog.askopenfilename(
            title="Select CSV file to import",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            imported_count = 0
            errors = []
            
            with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                # Validate required columns
                required_columns = ['name', 'principal', 'current_balance', 'interest_rate', 
                                  'monthly_min_payment', 'first_due_date']
                missing_columns = [col for col in required_columns if col not in reader.fieldnames]
                
                if missing_columns:
                    messagebox.showerror("CSV Import Error", 
                                       f"Missing required columns: {', '.join(missing_columns)}")
                    return
                
                for row_num, row in enumerate(reader, start=2):  # Start at 2 because row 1 is headers
                    try:
                        # Validate and convert data
                        name = row['name'].strip()
                        if not name:
                            errors.append(f"Row {row_num}: Loan name is required")
                            continue
                        
                        # Required numeric fields
                        principal = float(row['principal'])
                        current_balance = float(row['current_balance'])
                        interest_rate = float(row['interest_rate'])
                        monthly_min_payment = float(row['monthly_min_payment'])
                        
                        # Optional fields with defaults
                        extra_payment = float(row.get('extra_payment', 0) or 0)
                        loan_term_months = int(row['loan_term_months']) if row.get('loan_term_months') and row['loan_term_months'].strip() else None
                        lender = row.get('lender', '').strip() or None
                        notes = row.get('notes', '').strip() or None
                        
                        # Date field
                        first_due_date = row['first_due_date'].strip()
                        if not first_due_date:
                            errors.append(f"Row {row_num}: First due date is required")
                            continue
                        
                        # Validate date format (basic check)
                        try:
                            from datetime import datetime
                            datetime.strptime(first_due_date, '%Y-%m-%d')
                        except ValueError:
                            errors.append(f"Row {row_num}: Invalid date format. Use YYYY-MM-DD")
                            continue
                        
                        # Insert into database
                        insert_query = """
                        INSERT INTO loans (name, principal, current_balance, interest_rate, 
                                         monthly_min_payment, extra_payment, first_due_date, 
                                         lender, loan_term_months, notes)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """
                        self.db.execute(insert_query, (
                            name, principal, current_balance, interest_rate,
                            monthly_min_payment, extra_payment, first_due_date,
                            lender, loan_term_months, notes
                        ))
                        imported_count += 1
                        
                    except ValueError as e:
                        errors.append(f"Row {row_num}: Invalid numeric value - {str(e)}")
                    except Exception as e:
                        errors.append(f"Row {row_num}: {str(e)}")
            
            # Show results
            message = f"Successfully imported {imported_count} loans."
            if errors:
                error_message = "\n".join(errors[:10])  # Show first 10 errors
                if len(errors) > 10:
                    error_message += f"\n... and {len(errors) - 10} more errors"
                message += f"\n\nErrors encountered:\n{error_message}"
            
            messagebox.showinfo("CSV Import Results", message)
            
            if imported_count > 0:
                self.load_loans()
                
        except Exception as e:
            messagebox.showerror("CSV Import Error", f"Failed to read CSV file: {str(e)}")

    def show_csv_format_help(self):
        """Show information about the required CSV format."""
        help_text = """CSV Format Requirements:

Required Columns (must be present):
- name: Loan name/description
- principal: Original loan amount
- current_balance: Current outstanding balance
- interest_rate: Annual interest rate (as percentage, e.g., 4.25)
- monthly_min_payment: Minimum monthly payment amount
- first_due_date: First payment due date (YYYY-MM-DD format)

Optional Columns:
- extra_payment: Additional payment amount (default: 0)
- lender: Name of the lending institution
- loan_term_months: Total loan term in months
- notes: Additional notes about the loan

Example:
name,principal,current_balance,interest_rate,monthly_min_payment,extra_payment,first_due_date,lender
Student Loan,25000.00,22500.50,4.25,350.00,0.00,2025-01-15,Federal Direct
Car Loan,18000.00,15200.75,6.50,425.00,50.00,2025-02-01,Chase Bank

A template file 'loan_template.csv' has been created in your project directory."""
        
        messagebox.showinfo("CSV Format Help", help_text)

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