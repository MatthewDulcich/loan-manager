import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askfloat  # Import askfloat from tkinter.simpledialog
from utils.generate_payment_plan import generate_payment_plan
from models.loan import Loan


class PayoffPlanPopup(tk.Toplevel):
    def __init__(self, master, plan, loans, strategy=None, recalc_callback=None):
        super().__init__(master)
        self.title("Payoff Plan")
        self.geometry("1100x650")

        self.loans = loans
        self.plan = plan
        self.strategy = strategy
        self.recalc_callback = recalc_callback

        # --- Top area for summary and controls ---
        top_frame = tk.Frame(self)
        top_frame.pack(fill="x", padx=10, pady=(20, 0))

        self.min_label = tk.Label(top_frame, font=("Arial", 12, "bold"))
        self.min_label.grid(row=0, column=0, sticky="w", padx=(0, 20), pady=(0, 10))
        self.update_min_payment_label()

        tk.Label(top_frame, text="Extra Cash Per Month:").grid(row=0, column=1, sticky="e", padx=(0, 5), pady=(0, 10))
        self.extra_var = tk.StringVar(value="0")
        extra_entry = tk.Entry(top_frame, textvariable=self.extra_var, width=10)
        extra_entry.grid(row=0, column=2, sticky="w", padx=(0, 10), pady=(0, 10))

        recalc_btn = tk.Button(top_frame, text="Recalculate", command=self.recalculate_plan)
        recalc_btn.grid(row=0, column=3, sticky="w", pady=(0, 10))

        # --- Loan summary area ---
        summary_frame = tk.Frame(self)
        summary_frame.pack(fill="x", padx=10, pady=(10, 10))
        for idx, loan in enumerate(loans):
            summary = f"{loan.name}: ${loan.current_balance:,.2f} @ {loan.interest_rate:.2f}%"
            tk.Label(summary_frame, text=summary, font=("Arial", 10)).grid(row=0, column=idx, padx=10, sticky="w")

        # Spacer
        spacer = tk.Frame(self, height=10)
        spacer.pack(fill="x")

        # --- Table area ---
        loan_names = [loan.name for loan in loans]
        columns = ["Date"] + loan_names + ["Extra Payment", "Total Minimum Payment", "Total Payment", "Total Balance"]

        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Vertical scrollbar
        v_scrollbar = tk.Scrollbar(tree_frame, orient="vertical")
        v_scrollbar.pack(side="right", fill="y")
        
        # Horizontal scrollbar
        h_scrollbar = tk.Scrollbar(tree_frame, orient="horizontal")
        h_scrollbar.pack(side="bottom", fill="x")
        
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20,
                                yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Configure column headings
        self.tree.heading("Date", text="Date")
        for loan_name in loan_names:
            self.tree.heading(loan_name, text=loan_name)
        self.tree.heading("Extra Payment", text="Extra Payment")
        self.tree.heading("Total Minimum Payment", text="Total Minimum Payment")
        self.tree.heading("Total Payment", text="Total Payment")
        self.tree.heading("Total Balance", text="Total Balance")

        # Configure column widths
        self.tree.column("Date", width=115, anchor="center")
        for loan_name in loan_names:
            self.tree.column(loan_name, width=200, anchor="e")
        self.tree.column("Extra Payment", width=120, anchor="e")
        self.tree.column("Total Minimum Payment", width=150, anchor="e")
        self.tree.column("Total Payment", width=120, anchor="e")
        self.tree.column("Total Balance", width=120, anchor="e")

        self.tree.pack(side="left", fill="both", expand=True)
        
        # Connect scrollbars to tree view
        v_scrollbar.config(command=self.tree.yview)
        h_scrollbar.config(command=self.tree.xview)

        self.loan_names = loan_names
        self.display_plan(plan)

        # Save button
        save_btn = tk.Button(self, text="Save to File", command=lambda: self.save_plan(self.plan, self.loan_names))
        save_btn.pack(pady=5)

        # Bind treeview for extra cash editing
        self.tree.bind("<Double-1>", self.on_extra_cash_edit)

    def update_min_payment_label(self):
        min_payment = sum(loan.monthly_min_payment for loan in self.loans)
        self.min_label.config(text=f"Total Minimum Monthly Payment: ${min_payment:,.2f}")

    def display_plan(self, plan):
        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Display each period in the plan
        for idx, period in enumerate(plan):
            row = [period["date"]]
            balances = period.get("balances", {})
            for name in self.loan_names:
                payment = period["payments"].get(name, 0)
                new_bal = balances.get(name, 0)
                prev_bal = new_bal + payment
                if payment > 0 or new_bal > 0:
                    cell_text = f"{prev_bal:,.2f} - {payment:,.2f} = {new_bal:,.2f}"
                else:
                    cell_text = ""
                row.append(cell_text)
            
            # Extra Payment - either stored row-specific value or calculated difference
            if "row_extra_payment" in period:
                extra_payment = period["row_extra_payment"]
            else:
                minimum_total_payment = period.get("minimum_total_payment", 0)
                total_payment = sum(period["payments"].values())
                extra_payment = total_payment - minimum_total_payment
            row.append(f"${extra_payment:,.2f}")  # Display Extra Payment

            # Total Minimum Payment
            minimum_total_payment = period.get("minimum_total_payment", 0)
            row.append(f"${minimum_total_payment:,.2f}")  # Display Total Minimum Payment

            # Total Payment (sum of all loan payments)
            total_payment = sum(period["payments"].values())  # Corrected calculation
            row.append(f"${total_payment:,.2f}")  # Display Total Payment

            # Total Balance
            total_balance = period.get("total_balance", 0)
            row.append(f"${total_balance:,.2f}")  # Display Total Balance

            self.tree.insert("", "end", values=row)

    def recalculate_plan(self):
        try:
            extra_cash = float(self.extra_var.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for extra cash.")
            return

        if self.recalc_callback:
            # Use the callback if provided
            new_plan = self.recalc_callback(extra_cash)
        elif self.strategy:
            # Generate a completely fresh payment plan from scratch using the strategy
            # This will start with the original loan balances and create a new plan
            new_plan = self.strategy.generate_payment_plan(self.loans, extra_cash=extra_cash)
        else:
            # Fallback if no strategy is available
            messagebox.showinfo("Recalculate", f"Would recalculate with extra cash: ${extra_cash:,.2f}")
            return

        # Replace the entire plan with the new one (complete recalculation from scratch)
        self.plan = new_plan
        self.display_plan(new_plan)
        self.update_min_payment_label()

    def save_plan(self, plan, loan_names):
        try:
            with open("payoff_plan.txt", "w") as f:
                header = "Date," + ",".join(loan_names) + ",Total Payment,Total Balance\n"
                f.write(header)
                for period in plan:
                    row = [period["date"]]
                    total_payment = 0
                    for loan_name in loan_names:
                        payment = period["payments"].get(loan_name, 0)
                        row.append(str(payment))
                        total_payment += payment
                    row.append(str(total_payment))
                    row.append(str(period.get('total_balance', 0)))
                    f.write(",".join(row) + "\n")
            messagebox.showinfo("Export", "Payoff plan exported to payoff_plan.txt")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")

    def on_extra_cash_edit(self, event):
        # Get the selected row and column
        selected_item = self.tree.focus()
        if not selected_item:
            return

        # Get the column index and ensure it's the "Extra Payment" column
        col = self.tree.identify_column(event.x)
        extra_payment_col_index = len(self.loan_names) + 2  # Adjust index for "Extra Payment" column
        if col != f"#{extra_payment_col_index}":
            return

        # Get the row index and current value
        row_index = self.tree.index(selected_item)
        period = self.plan[row_index]
        
        # Check if this row has a stored individual extra payment, otherwise calculate from current state
        if "row_extra_payment" in period:
            current_value = period["row_extra_payment"]
        else:
            # Calculate current extra payment (total - minimum for this row)
            minimum_total_payment = period.get("minimum_total_payment", 0)
            total_payment = sum(period["payments"].values())
            current_value = total_payment - minimum_total_payment

        # Get the cell's bounding box
        bbox = self.tree.bbox(selected_item, col)
        if not bbox:
            return

        # Create an Entry widget for editing
        entry = tk.Entry(self.tree, justify="center")
        entry.insert(0, str(current_value))
        entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])

        # Handle Enter key to save the value and recalculate
        def save_value(event):
            try:
                extra_payment = float(entry.get())
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid number for extra payment.")
                entry.destroy()
                return

            # Store the extra payment for this specific row
            self.plan[row_index]["row_extra_payment"] = extra_payment
            
            # Recalculate from this row forward with individual extra payments
            self.recalculate_from_row_with_individual_extras(row_index)

            # Destroy the Entry widget
            entry.destroy()

        # Bind Enter key to save the value
        entry.bind("<Return>", save_value)
        entry.focus()

    def recalculate_from_row_with_individual_extras(self, start_row):
        """Recalculate payment plan from a specific row forward, preserving individual extra payments"""
        # Get starting loan states from the previous row (or original if start_row is 0)
        if start_row == 0:
            # Start with original loan states
            working_loans = [Loan(**loan.__dict__) for loan in self.loans]
            for loan in working_loans:
                loan.adjusted_min_payment = loan.monthly_min_payment
                loan.total_paid = 0.0
        else:
            # Reconstruct loan states from previous period
            prev_period = self.plan[start_row - 1]
            working_loans = []
            for loan in self.loans:
                loan_copy = Loan(**loan.__dict__)
                loan_copy.current_balance = prev_period["balances"].get(loan.name, 0)
                # Keep adjusted_min_payment as original monthly payment if balance > 0, otherwise 0
                loan_copy.adjusted_min_payment = loan.monthly_min_payment if loan_copy.current_balance > 0 else 0
                loan_copy.total_paid = 0.0  # We don't track this in period recalc
                working_loans.append(loan_copy)
        
        # Get the global extra cash amount
        try:
            global_extra_cash = float(self.extra_var.get())
        except (ValueError, AttributeError):
            global_extra_cash = 0.0
        
        # Compute fixed budgets (this should remain constant)
        minimum_total_payment = sum(loan.monthly_min_payment for loan in self.loans)
        
        # Recalculate each period from start_row forward
        from datetime import datetime, timedelta
        base_date = datetime.today().date()
        
        for row_idx in range(start_row, len(self.plan)):
            period = self.plan[row_idx]
            
            # Get the extra payment for this specific period
            # Use stored row-specific value if it exists, otherwise use global
            if "row_extra_payment" in period:
                period_extra_cash = period["row_extra_payment"]
            else:
                period_extra_cash = global_extra_cash
            
            # Calculate fixed budget for this period
            adjusted_total_payment = minimum_total_payment + period_extra_cash
            fixed_budget = adjusted_total_payment
            
            # Sort loans by balance (snowball method)
            working_loans.sort(key=lambda l: l.current_balance)
            
            period_payments = {}
            freed = 0.0
            
            # 1) Pay minimums and collect freed amounts (exact logic from generate_payment_plan)
            for loan in working_loans:
                if loan.current_balance <= 0:
                    period_payments[loan.name] = 0.0
                    continue

                # Accrue interest
                interest = loan.current_balance * (loan.interest_rate / 100 / 12)
                loan.current_balance += interest

                # Determine payment (cap at balance)
                min_pay = loan.adjusted_min_payment
                payment_amt = min(min_pay, loan.current_balance)
                principal = max(0.0, payment_amt - min(payment_amt, interest))

                # Apply payment
                loan.current_balance -= principal
                period_payments[loan.name] = round(payment_amt, 2)

                # Freed from min_pay
                freed += (min_pay - payment_amt)
                if loan.current_balance <= 0:
                    loan.adjusted_min_payment = 0.0

            # 2) Build extra pool and redistribute immediately (exact logic from generate_payment_plan)
            extra_pool = period_extra_cash + freed
            for loan in working_loans:
                if loan.current_balance <= 0 or extra_pool <= 0:
                    continue
                bonus = min(extra_pool, loan.current_balance)
                loan.current_balance -= bonus
                period_payments[loan.name] = period_payments.get(loan.name, 0.0) + round(bonus, 2)
                extra_pool -= bonus

            # 2a) Ensure total_payment equals fixed_budget (exact logic from generate_payment_plan)
            actual_total = sum(period_payments.values())
            if actual_total < fixed_budget:
                diff = fixed_budget - actual_total
                for loan in working_loans:
                    if loan.current_balance <= 0 or diff <= 0:
                        continue
                    bonus = min(diff, loan.current_balance)
                    loan.current_balance -= bonus
                    period_payments[loan.name] = period_payments.get(loan.name, 0.0) + round(bonus, 2)
                    diff -= bonus

            # 3) Update the period with new calculations
            period["payments"] = period_payments
            period["balances"] = {loan.name: round(max(loan.current_balance, 0), 2) for loan in working_loans}
            period["total_payment"] = round(fixed_budget, 2)
            period["total_balance"] = round(sum(max(loan.current_balance, 0) for loan in working_loans), 2)
            period["minimum_total_payment"] = round(minimum_total_payment, 2)
            period["adjusted_total_payment"] = round(adjusted_total_payment, 2)
        
        # Update the display
        self.display_plan(self.plan)
