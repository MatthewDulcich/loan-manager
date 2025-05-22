import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askfloat  # Import askfloat from tkinter.simpledialog
from utils.generate_payment_plan import generate_payment_plan


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
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side="right", fill="y")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)

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
        tree_scroll.config(command=self.tree.yview)

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
            
            # Extra Payment
            extra_cash = period.get("extra_cash", 0)
            row.append(f"${extra_cash:,.2f}")  # Display Extra Payment

            # Total Minimum Payment
            minimum_total_payment = period.get("minimum_total_payment", 0)
            row.append(f"${minimum_total_payment:,.2f}")  # Display Total Minimum Payment

            # Total Payment (sum of all loan payments + extra cash)
            total_payment = sum(period["payments"].values()) + extra_cash
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
            new_plan = self.recalc_callback(extra_cash)
        elif self.strategy:
            for loan in self.loans:
                loan.extra_payment = extra_cash
            new_plan = self.strategy.generate_payment_plan(self.loans)
        else:
            messagebox.showinfo("Recalculate", f"Would recalculate with extra cash: ${extra_cash:,.2f}")
            return

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
        current_value = self.plan[row_index].get("extra_cash", 0)

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
            print("Save value triggered")  # Debug statement
            try:
                extra_cash = float(entry.get())
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid number for extra cash.")
                entry.destroy()
                return

            # Update the plan with the extra cash
            self.plan[row_index]["extra_cash"] = extra_cash

            # Recalculate the plan starting from this row
            self.recalculate_plan_from_row(row_index)

            # Destroy the Entry widget
            entry.destroy()

        # Bind Enter key to save the value
        entry.bind("<Return>", save_value)
        entry.focus()

    def recalculate_plan_from_row(self, start_row):
        print(f"Recalculating from row {start_row}")  # Debug statement

        # Preserve the values for rows before the start_row
        for idx, period in enumerate(self.plan[:start_row]):
            print(f"Preserving row {idx}, Total Payment: {period['total_payment']}")  # Debug statement

        # Update the plan starting from the specified row
        for idx, period in enumerate(self.plan[start_row:], start=start_row):
            extra_cash = period.get("extra_cash", 0)
            print(f"Row {idx}, Extra Cash: {extra_cash}")  # Debug statement

            # Determine the starting balances for this row
            if idx == 0:  # If this is the very first row in the plan
                starting_balances = {loan.name: loan.current_balance for loan in self.loans}
            elif idx == start_row:  # If this is the first row being recalculated
                starting_balances = self.plan[idx - 1]["balances"]
            else:  # For all other rows
                starting_balances = self.plan[idx - 1]["balances"]

            # Calculate payments and update balances for this row
            period["payments"] = {}
            ending_balances = {}  # Track ending balances for this row
            total_extra_payments = 0  # Track total extra payments for this period
            freed_min_payments = 0  # Track freed minimum payments from paid-off loans

            # Step 1: Pay minimum payments and track freed-up money
            for loan in self.loans:
                loan_name = loan.name
                starting_balance = starting_balances[loan_name]

                # Skip loans that are already paid off
                if starting_balance <= 0:
                    period["payments"][loan_name] = 0.0
                    ending_balances[loan_name] = 0.0
                    freed_min_payments += loan.monthly_min_payment  # Add freed minimum payment
                    continue

                # Apply the minimum payment
                payment = loan.monthly_min_payment
                if payment > starting_balance:
                    payment = starting_balance  # Cap payment at the remaining balance

                # Apply extra cash if available
                if extra_cash > 0:
                    extra_payment = min(extra_cash, starting_balance - payment)
                    payment += extra_payment
                    extra_cash -= extra_payment
                    total_extra_payments += extra_payment  # Track extra payments

                # Calculate the new balance after the payment
                new_balance = starting_balance - payment
                period["payments"][loan_name] = round(payment, 2)
                ending_balances[loan_name] = max(round(new_balance, 2), 0.0)  # Ensure balance does not go negative

            # Step 2: Redistribute freed-up money (freed minimum payments + leftover extra cash)
            extra_pool = extra_cash + freed_min_payments
            for loan in sorted(self.loans, key=lambda l: ending_balances[l.name]):  # Prioritize smallest balances
                loan_name = loan.name
                if extra_pool <= 0 or ending_balances[loan_name] <= 0:
                    continue  # Skip loans that are already paid off or if no extra money is left
                bonus_payment = min(extra_pool, ending_balances[loan_name])
                ending_balances[loan_name] -= bonus_payment
                period["payments"][loan_name] += round(bonus_payment, 2)
                extra_pool -= bonus_payment
                total_extra_payments += bonus_payment  # Track redistributed payments

            # Step 3: Ensure total payment matches the fixed budget
            fixed_budget = sum(loan.monthly_min_payment for loan in self.loans) + period.get("extra_cash", 0)
            actual_total = sum(period["payments"].values())
            if actual_total < fixed_budget:
                diff = fixed_budget - actual_total
                for loan in sorted(self.loans, key=lambda l: ending_balances[l.name]):  # Prioritize smallest balances
                    loan_name = loan.name
                    if diff <= 0 or ending_balances[loan_name] <= 0:
                        continue
                    bonus_payment = min(diff, ending_balances[loan_name])
                    ending_balances[loan_name] -= bonus_payment
                    period["payments"][loan_name] += round(bonus_payment, 2)
                    diff -= bonus_payment

            # Step 4: Update the balances for the loans in this period
            period["balances"] = ending_balances

            # Step 5: Update the total payment for this period
            period["total_payment"] = sum(period["payments"].values())

            # Step 6: Propagate the ending balances to the next row
            if idx + 1 < len(self.plan):
                self.plan[idx + 1]["balances"] = ending_balances

        # Refresh the display to show updated rows
        self.display_plan(self.plan)
