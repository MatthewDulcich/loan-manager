import tkinter as tk
from tkinter import ttk, messagebox

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
        columns = ["Date"] + loan_names + ["Total Payment", "Total Balance"]

        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side="right", fill="y")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=tree_scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        tree_scroll.config(command=self.tree.yview)

        # Set column headers and widths
        self.tree.heading("Date", text="Date")
        self.tree.column("Date", width=100, anchor="center")
        for loan_name in loan_names:
            self.tree.heading(loan_name, text=loan_name)
            self.tree.column(loan_name, width=140, anchor="center")
        self.tree.heading("Total Payment", text="Total Payment")
        self.tree.column("Total Payment", width=130, anchor="center")
        self.tree.heading("Total Balance", text="Total Balance")
        self.tree.column("Total Balance", width=140, anchor="center")

        self.loan_names = loan_names
        self.display_plan(plan)

        # Save button
        save_btn = tk.Button(self, text="Save to File", command=lambda: self.save_plan(self.plan, self.loan_names))
        save_btn.pack(pady=5)

    def update_min_payment_label(self):
        min_payment = sum(loan.monthly_min_payment for loan in self.loans)
        self.min_label.config(text=f"Total Minimum Monthly Payment: ${min_payment:,.2f}")

    def display_plan(self, plan):
        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Insert plan data
        for period in plan:
            row = [period["date"]]
            total_payment = 0
            for loan_name in self.loan_names:
                payment = period["payments"].get(loan_name, 0)
                row.append(f"${payment:,.2f}" if payment > 0 else "")
                total_payment += payment
            row.append(f"${total_payment:,.2f}")
            row.append(f"${period.get('total_balance', 0):,.2f}")
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