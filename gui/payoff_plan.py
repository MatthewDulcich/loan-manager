import tkinter as tk
from tkinter import ttk, messagebox

class PayoffPlanPopup(tk.Toplevel):
    def __init__(self, master, plan, loans):
        super().__init__(master)
        self.title("Payoff Plan")
        self.geometry("900x500")

        # Use the loans argument directly
        loan_headers = [f"{loan.name}\n(${loan.current_balance:,.2f} @ {loan.interest_rate:.2f}%)" for loan in loans]
        loan_names = [loan.name for loan in loans]

        columns = ["Date"] + loan_headers + ["Total Payment", "Total Balance"]

        # Treeview for table
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side="right", fill="y")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=tree_scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        tree_scroll.config(command=self.tree.yview)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        # Insert plan data
        for period in plan:  # <-- FIXED
            row = [period["date"]]
            total_payment = 0
            for loan_name in loan_names:
                payment = period["payments"].get(loan_name, 0)
                row.append(f"${payment:,.2f}" if payment > 0 else "")
                total_payment += payment
            row.append(f"${total_payment:,.2f}")
            row.append(f"${period.get('total_balance', 0):,.2f}")
            self.tree.insert("", "end", values=row)

        # Save button
        save_btn = tk.Button(self, text="Save to File", command=lambda: self.save_plan(plan, loan_names))
        save_btn.pack(pady=5)

    def save_plan(self, plan, loan_names):
        try:
            with open("payoff_plan.txt", "w") as f:
                header = "Date," + ",".join(loan_names) + ",Total Payment,Total Balance\n"
                f.write(header)
                for period in plan:  # <-- FIXED
                    row = [period["date"]]
                    total_payment = 0
                    for loan_name in loan_names:
                        payment = period["payments"].get(loan_name, 0)
                        row.append(str(payment))
                        total_payment += payment
                    row.append(str(total_payment))
                    row.append(str(period.get("total_balance", 0)))
                    f.write(",".join(row) + "\n")
            messagebox.showinfo("Export", "Payoff plan exported to payoff_plan.txt")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")