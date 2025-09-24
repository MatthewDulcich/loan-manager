import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import font
from datetime import datetime

class SalaryCalculatorPopup(tk.Toplevel):
    def __init__(self, master, loans=None):
        super().__init__(master)
        self.title("Salary Calculator")
        self.geometry("600x900")  # Made window larger
        self.resizable(True, True)
        self.loans = loans or []
        
        # Make window modal
        self.transient(master)
        self.grab_set()
        
        # Configure grid weights for responsive design
        self.grid_columnconfigure(1, weight=1)
        
        # Create a canvas and scrollbar for scrolling
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Configure scrollable frame grid
        self.scrollable_frame.grid_columnconfigure(1, weight=1)
        
        self.create_widgets()
        self.center_window()
        
        # Bind mousewheel to canvas
        self.bind_mousewheel()
        
        # Ensure the window starts scrolled to the top
        self.after(100, lambda: self.canvas.yview_moveto(0))
        
    def center_window(self):
        """Center the window on the screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def bind_mousewheel(self):
        """Bind mousewheel events to canvas"""
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            self.canvas.unbind_all("<MouseWheel>")
        
        self.canvas.bind('<Enter>', _bind_to_mousewheel)
        self.canvas.bind('<Leave>', _unbind_from_mousewheel)

    def set_placeholder(self, entry_widget, string_var, placeholder_text):
        """Set placeholder text for an entry widget"""
        def on_focus_in(event):
            if entry_widget.get() == placeholder_text:
                entry_widget.delete(0, tk.END)
                entry_widget.config(fg='white')
        
        def on_focus_out(event):
            if entry_widget.get() == '':
                entry_widget.insert(0, placeholder_text)
                entry_widget.config(fg='gray')
        
        # Set initial placeholder
        entry_widget.insert(0, placeholder_text)
        entry_widget.config(fg='gray')
        
        # Bind events
        entry_widget.bind('<FocusIn>', on_focus_in)
        entry_widget.bind('<FocusOut>', on_focus_out)

    def create_widgets(self):
        # Title
        title_font = font.Font(size=16, weight="bold")
        title_label = tk.Label(self.scrollable_frame, text="Salary Requirements Calculator", font=title_font)
        title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky="ew")
        
        # Validation commands
        vcmd_float = (self.register(self.validate_float), "%P")
        vcmd_percent = (self.register(self.validate_percent), "%P")
        
        current_row = 1
        
        # Monthly Expenses Section
        expenses_label = tk.Label(self.scrollable_frame, text="Monthly Living Expenses", font=font.Font(weight="bold"))
        expenses_label.grid(row=current_row, column=0, columnspan=2, pady=(10, 5), sticky="w")
        current_row += 1
        
        # Rent/Mortgage
        tk.Label(self.scrollable_frame, text="Rent/Mortgage:").grid(row=current_row, column=0, padx=10, pady=5, sticky='e')
        self.rent_var = tk.StringVar()
        self.rent_entry = tk.Entry(self.scrollable_frame, textvariable=self.rent_var, validate="key", validatecommand=vcmd_float)
        self.rent_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
        self.set_placeholder(self.rent_entry, self.rent_var, "1800")
        current_row += 1
        
        # Car Payment
        tk.Label(self.scrollable_frame, text="Car Payment:").grid(row=current_row, column=0, padx=10, pady=5, sticky='e')
        self.car_var = tk.StringVar()
        self.car_entry = tk.Entry(self.scrollable_frame, textvariable=self.car_var, validate="key", validatecommand=vcmd_float)
        self.car_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
        self.set_placeholder(self.car_entry, self.car_var, "450")
        current_row += 1
        
        # Insurance
        tk.Label(self.scrollable_frame, text="Insurance (Health, Car, etc.):").grid(row=current_row, column=0, padx=10, pady=5, sticky='e')
        self.insurance_var = tk.StringVar()
        self.insurance_entry = tk.Entry(self.scrollable_frame, textvariable=self.insurance_var, validate="key", validatecommand=vcmd_float)
        self.insurance_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
        self.set_placeholder(self.insurance_entry, self.insurance_var, "350")
        current_row += 1
        
        # Food
        tk.Label(self.scrollable_frame, text="Food & Groceries:").grid(row=current_row, column=0, padx=10, pady=5, sticky='e')
        self.food_var = tk.StringVar()
        self.food_entry = tk.Entry(self.scrollable_frame, textvariable=self.food_var, validate="key", validatecommand=vcmd_float)
        self.food_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
        self.set_placeholder(self.food_entry, self.food_var, "600")
        current_row += 1
        
        # Utilities
        tk.Label(self.scrollable_frame, text="Utilities (Electric, Gas, Water):").grid(row=current_row, column=0, padx=10, pady=5, sticky='e')
        self.utilities_var = tk.StringVar()
        self.utilities_entry = tk.Entry(self.scrollable_frame, textvariable=self.utilities_var, validate="key", validatecommand=vcmd_float)
        self.utilities_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
        self.set_placeholder(self.utilities_entry, self.utilities_var, "200")
        current_row += 1
        
        # Phone/Internet
        tk.Label(self.scrollable_frame, text="Phone & Internet:").grid(row=current_row, column=0, padx=10, pady=5, sticky='e')
        self.phone_var = tk.StringVar()
        self.phone_entry = tk.Entry(self.scrollable_frame, textvariable=self.phone_var, validate="key", validatecommand=vcmd_float)
        self.phone_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
        self.set_placeholder(self.phone_entry, self.phone_var, "150")
        current_row += 1
        
        # Other Monthly Expenses
        tk.Label(self.scrollable_frame, text="Other Monthly Expenses:").grid(row=current_row, column=0, padx=10, pady=5, sticky='e')
        self.other_expenses_var = tk.StringVar()
        self.other_expenses_entry = tk.Entry(self.scrollable_frame, textvariable=self.other_expenses_var, validate="key", validatecommand=vcmd_float)
        self.other_expenses_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
        self.set_placeholder(self.other_expenses_entry, self.other_expenses_var, "300")
        current_row += 1
        
        # Loan Payments Section
        current_row += 1
        loan_label = tk.Label(self.scrollable_frame, text="Loan Payments", font=font.Font(weight="bold"))
        loan_label.grid(row=current_row, column=0, columnspan=2, pady=(10, 5), sticky="w")
        current_row += 1
        
        # Calculate total loan payments from loaded loans
        total_loan_payment = sum(loan.monthly_min_payment for loan in self.loans)
        
        tk.Label(self.scrollable_frame, text="Total Monthly Loan Payments:").grid(row=current_row, column=0, padx=10, pady=5, sticky='e')
        self.loan_payments_var = tk.StringVar(value=f"{total_loan_payment:.2f}")
        self.loan_payments_entry = tk.Entry(self.scrollable_frame, textvariable=self.loan_payments_var, validate="key", validatecommand=vcmd_float)
        self.loan_payments_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
        current_row += 1
        
        # Extra Loan Payments
        tk.Label(self.scrollable_frame, text="Extra Loan Payments:").grid(row=current_row, column=0, padx=10, pady=5, sticky='e')
        self.extra_loan_var = tk.StringVar()
        self.extra_loan_entry = tk.Entry(self.scrollable_frame, textvariable=self.extra_loan_var, validate="key", validatecommand=vcmd_float)
        self.extra_loan_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
        self.set_placeholder(self.extra_loan_entry, self.extra_loan_var, "200")
        current_row += 1
        
        # Savings & Extras Section
        current_row += 1
        savings_label = tk.Label(self.scrollable_frame, text="Savings & Extra Money", font=font.Font(weight="bold"))
        savings_label.grid(row=current_row, column=0, columnspan=2, pady=(10, 5), sticky="w")
        current_row += 1
        
        # Emergency Fund
        tk.Label(self.scrollable_frame, text="Emergency Fund/Savings:").grid(row=current_row, column=0, padx=10, pady=5, sticky='e')
        self.savings_var = tk.StringVar()
        self.savings_entry = tk.Entry(self.scrollable_frame, textvariable=self.savings_var, validate="key", validatecommand=vcmd_float)
        self.savings_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
        self.set_placeholder(self.savings_entry, self.savings_var, "500")
        current_row += 1
        
        # Entertainment/Personal
        tk.Label(self.scrollable_frame, text="Entertainment/Personal:").grid(row=current_row, column=0, padx=10, pady=5, sticky='e')
        self.entertainment_var = tk.StringVar()
        self.entertainment_entry = tk.Entry(self.scrollable_frame, textvariable=self.entertainment_var, validate="key", validatecommand=vcmd_float)
        self.entertainment_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
        self.set_placeholder(self.entertainment_entry, self.entertainment_var, "400")
        current_row += 1
        
        # Retirement & Investment Section
        current_row += 1
        retirement_label = tk.Label(self.scrollable_frame, text="Retirement & Investment Contributions", font=font.Font(weight="bold"))
        retirement_label.grid(row=current_row, column=0, columnspan=2, pady=(10, 5), sticky="w")
        current_row += 1
        
        # 401k
        tk.Label(self.scrollable_frame, text="401(k) Contribution:").grid(row=current_row, column=0, padx=10, pady=5, sticky='e')
        self.contribution_401k_var = tk.StringVar()
        self.contribution_401k_entry = tk.Entry(self.scrollable_frame, textvariable=self.contribution_401k_var, validate="key", validatecommand=vcmd_float)
        self.contribution_401k_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
        self.set_placeholder(self.contribution_401k_entry, self.contribution_401k_var, "800")
        current_row += 1
        
        # Traditional IRA
        tk.Label(self.scrollable_frame, text="Traditional IRA:").grid(row=current_row, column=0, padx=10, pady=5, sticky='e')
        self.traditional_ira_var = tk.StringVar()
        self.traditional_ira_entry = tk.Entry(self.scrollable_frame, textvariable=self.traditional_ira_var, validate="key", validatecommand=vcmd_float)
        self.traditional_ira_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
        self.set_placeholder(self.traditional_ira_entry, self.traditional_ira_var, "0")
        current_row += 1
        
        # Roth IRA
        tk.Label(self.scrollable_frame, text="Roth IRA:").grid(row=current_row, column=0, padx=10, pady=5, sticky='e')
        self.roth_ira_var = tk.StringVar()
        self.roth_ira_entry = tk.Entry(self.scrollable_frame, textvariable=self.roth_ira_var, validate="key", validatecommand=vcmd_float)
        self.roth_ira_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
        self.set_placeholder(self.roth_ira_entry, self.roth_ira_var, "500")
        current_row += 1
        
        # HSA (Health Savings Account)
        tk.Label(self.scrollable_frame, text="HSA Contribution:").grid(row=current_row, column=0, padx=10, pady=5, sticky='e')
        self.hsa_var = tk.StringVar()
        self.hsa_entry = tk.Entry(self.scrollable_frame, textvariable=self.hsa_var, validate="key", validatecommand=vcmd_float)
        self.hsa_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
        self.set_placeholder(self.hsa_entry, self.hsa_var, "300")
        current_row += 1
        
        # 529 Education Plan
        tk.Label(self.scrollable_frame, text="529 Education Plan:").grid(row=current_row, column=0, padx=10, pady=5, sticky='e')
        self.education_529_var = tk.StringVar()
        self.education_529_entry = tk.Entry(self.scrollable_frame, textvariable=self.education_529_var, validate="key", validatecommand=vcmd_float)
        self.education_529_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
        self.set_placeholder(self.education_529_entry, self.education_529_var, "0")
        current_row += 1
        
        # Other Investments
        tk.Label(self.scrollable_frame, text="Other Investments:").grid(row=current_row, column=0, padx=10, pady=5, sticky='e')
        self.other_investments_var = tk.StringVar()
        self.other_investments_entry = tk.Entry(self.scrollable_frame, textvariable=self.other_investments_var, validate="key", validatecommand=vcmd_float)
        self.other_investments_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
        self.set_placeholder(self.other_investments_entry, self.other_investments_var, "200")
        current_row += 1
        
        # Tax Information Section
        current_row += 1
        tax_label = tk.Label(self.scrollable_frame, text="Tax Information", font=font.Font(weight="bold"))
        tax_label.grid(row=current_row, column=0, columnspan=2, pady=(10, 5), sticky="w")
        current_row += 1
        
        # Tax calculation method
        tk.Label(self.scrollable_frame, text="Tax Calculation Method:").grid(row=current_row, column=0, padx=10, pady=5, sticky='e')
        self.tax_method_var = tk.StringVar(value="Progressive")
        tax_method_combo = ttk.Combobox(self.scrollable_frame, textvariable=self.tax_method_var, 
                                       values=["Progressive", "Flat Rate"], state="readonly")
        tax_method_combo.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
        tax_method_combo.bind("<<ComboboxSelected>>", self.on_tax_method_change)
        current_row += 1
        
        # Progressive tax frame (shown by default)
        self.progressive_frame = tk.Frame(self.scrollable_frame)
        self.progressive_frame.grid(row=current_row, column=0, columnspan=2, sticky="ew", padx=10)
        self.progressive_frame.grid_columnconfigure(1, weight=1)
        
        # Filing Status
        tk.Label(self.progressive_frame, text="Filing Status:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.filing_status_var = tk.StringVar(value="Single")
        filing_combo = ttk.Combobox(self.progressive_frame, textvariable=self.filing_status_var,
                                   values=["Single", "Married Filing Jointly", "Married Filing Separately", "Head of Household"], 
                                   state="readonly")
        filing_combo.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        # State selection
        tk.Label(self.progressive_frame, text="State:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.state_var = tk.StringVar(value="Maryland")
        state_combo = ttk.Combobox(self.progressive_frame, textvariable=self.state_var,
                                  values=["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", 
                                         "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", 
                                         "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", 
                                         "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", 
                                         "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", 
                                         "New Hampshire", "New Jersey", "New Mexico", "New York", 
                                         "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", 
                                         "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", 
                                         "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", 
                                         "West Virginia", "Wisconsin", "Wyoming"], 
                                  state="readonly")
        state_combo.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        current_row += 1
        
        # Flat rate frame (hidden by default)
        self.flat_rate_frame = tk.Frame(self.scrollable_frame)
        self.flat_rate_frame.grid(row=current_row, column=0, columnspan=2, sticky="ew", padx=10)
        self.flat_rate_frame.grid_columnconfigure(1, weight=1)
        self.flat_rate_frame.grid_remove()  # Hide initially
        
        # Federal Tax Rate (flat)
        tk.Label(self.flat_rate_frame, text="Federal Tax Rate (%):").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.federal_tax_var = tk.StringVar(value="22")
        self.federal_tax_entry = tk.Entry(self.flat_rate_frame, textvariable=self.federal_tax_var, validate="key", validatecommand=vcmd_percent)
        self.federal_tax_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        # State Tax Rate (flat)
        tk.Label(self.flat_rate_frame, text="State Tax Rate (%):").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.state_tax_var = tk.StringVar(value="6")
        self.state_tax_entry = tk.Entry(self.flat_rate_frame, textvariable=self.state_tax_var, validate="key", validatecommand=vcmd_percent)
        self.state_tax_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        current_row += 1
        
        # FICA Tax (always shown - same for both methods)
        tk.Label(self.scrollable_frame, text="FICA Tax Rate (%):").grid(row=current_row, column=0, padx=10, pady=5, sticky='e')
        self.fica_tax_var = tk.StringVar(value="7.65")  # Social Security (6.2%) + Medicare (1.45%)
        self.fica_tax_entry = tk.Entry(self.scrollable_frame, textvariable=self.fica_tax_var, validate="key", validatecommand=vcmd_percent)
        self.fica_tax_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
        current_row += 1
        
        # Tithe Section
        current_row += 1
        tithe_label = tk.Label(self.scrollable_frame, text="Tithe Information", font=font.Font(weight="bold"))
        tithe_label.grid(row=current_row, column=0, columnspan=2, pady=(10, 5), sticky="w")
        current_row += 1
        
        # Tithe checkbox
        self.tithe_enabled_var = tk.BooleanVar(value=True)
        tithe_check = tk.Checkbutton(self.scrollable_frame, text="Include Tithe", variable=self.tithe_enabled_var,
                                    command=self.on_tithe_toggle)
        tithe_check.grid(row=current_row, column=0, padx=10, pady=5, sticky='w')
        current_row += 1
        
        # Tithe rate
        tk.Label(self.scrollable_frame, text="Tithe Rate (%):").grid(row=current_row, column=0, padx=10, pady=5, sticky='e')
        self.tithe_var = tk.StringVar(value="10")
        self.tithe_entry = tk.Entry(self.scrollable_frame, textvariable=self.tithe_var, validate="key", validatecommand=vcmd_percent)
        self.tithe_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
        current_row += 1
        
        # Tithe calculation method
        tk.Label(self.scrollable_frame, text="Calculate Tithe On:").grid(row=current_row, column=0, padx=10, pady=5, sticky='e')
        self.tithe_basis_var = tk.StringVar(value="Gross Income")
        tithe_basis_combo = ttk.Combobox(self.scrollable_frame, textvariable=self.tithe_basis_var,
                                        values=["Gross Income", "Net Income"], state="readonly")
        tithe_basis_combo.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
        current_row += 1
        
        # Minimum Leftover Amount Section
        current_row += 1
        leftover_label = tk.Label(self.scrollable_frame, text="Financial Cushion", font=font.Font(weight="bold"))
        leftover_label.grid(row=current_row, column=0, columnspan=2, pady=(10, 5), sticky="w")
        current_row += 1
        
        # Minimum leftover amount
        tk.Label(self.scrollable_frame, text="Minimum Monthly Leftover:").grid(row=current_row, column=0, padx=10, pady=5, sticky='e')
        self.min_leftover_var = tk.StringVar()
        self.min_leftover_entry = tk.Entry(self.scrollable_frame, textvariable=self.min_leftover_var, validate="key", validatecommand=vcmd_float)
        self.min_leftover_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
        self.set_placeholder(self.min_leftover_entry, self.min_leftover_var, "500")
        current_row += 1
        
        # Help text for leftover amount
        help_text = tk.Label(self.scrollable_frame, text="(Extra money for unexpected expenses, discretionary spending, etc.)", 
                            font=font.Font(size=9), fg="gray")
        help_text.grid(row=current_row, column=1, padx=10, pady=(0, 5), sticky="w")
        current_row += 1
        
        # Calculate Button
        current_row += 1
        calculate_button = tk.Button(self.scrollable_frame, text="🧮 Calculate Required Salary", command=self.calculate_salary, 
                                   bg="#E0E0E0", fg="black", font=font.Font(weight="bold", size=14),
                                   relief=tk.RAISED, bd=2, pady=10)
        calculate_button.grid(row=current_row, column=0, columnspan=2, pady=25, padx=20, sticky="ew")
        current_row += 1
        
        # Results Section
        self.results_frame = tk.Frame(self.scrollable_frame, relief=tk.RAISED, bd=2)
        self.results_frame.grid(row=current_row, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.results_frame.grid_columnconfigure(1, weight=1)
        current_row += 1
        
        # Save Results Button (initially hidden)
        self.save_button = tk.Button(self.scrollable_frame, text="💾 Save Calculation Results", command=self.save_results,
                                   bg="#E0E0E0", fg="black", font=font.Font(weight="bold", size=12),
                                   relief=tk.RAISED, bd=2, pady=5)
        self.save_button.grid(row=current_row, column=0, columnspan=2, pady=15, padx=20, sticky="ew")
        self.save_button.grid_remove()  # Hide initially until calculation is done
        
        # Results will be populated by calculate_salary method
        self.results_labels = {}
        self.last_calculation_results = None  # Store results for saving
        
    def validate_float(self, value):
        """Validate float input"""
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            self.bell()
            return False
    
    def validate_percent(self, value):
        """Validate percentage input"""
        if value == "":
            return True
        try:
            val = float(value)
            if 0 <= val <= 100:
                return True
            else:
                self.bell()
                return False
        except ValueError:
            self.bell()
            return False
    
    def on_tax_method_change(self, event=None):
        """Handle tax method change"""
        if self.tax_method_var.get() == "Progressive":
            self.progressive_frame.grid()
            self.flat_rate_frame.grid_remove()
        else:
            self.progressive_frame.grid_remove()
            self.flat_rate_frame.grid()
    
    def on_tithe_toggle(self):
        """Enable/disable tithe entry based on checkbox"""
        if self.tithe_enabled_var.get():
            self.tithe_entry.config(state='normal')
        else:
            self.tithe_entry.config(state='disabled')
    
    def get_federal_tax_brackets_2025(self, filing_status):
        """Get 2025 federal tax brackets based on filing status"""
        brackets = {
            "Single": [
                (11600, 0.10),    # 10% on income up to $11,600
                (47150, 0.12),    # 12% on income $11,601 to $47,150
                (100525, 0.22),   # 22% on income $47,151 to $100,525
                (191950, 0.24),   # 24% on income $100,526 to $191,950
                (243725, 0.32),   # 32% on income $191,951 to $243,725
                (609350, 0.35),   # 35% on income $243,726 to $609,350
                (float('inf'), 0.37)  # 37% on income over $609,350
            ],
            "Married Filing Jointly": [
                (23200, 0.10),    # 10% on income up to $23,200
                (94300, 0.12),    # 12% on income $23,201 to $94,300
                (201050, 0.22),   # 22% on income $94,301 to $201,050
                (383900, 0.24),   # 24% on income $201,051 to $383,900
                (487450, 0.32),   # 32% on income $383,901 to $487,450
                (731200, 0.35),   # 35% on income $487,451 to $731,200
                (float('inf'), 0.37)  # 37% on income over $731,200
            ],
            "Married Filing Separately": [
                (11600, 0.10),    # 10% on income up to $11,600
                (47150, 0.12),    # 12% on income $11,601 to $47,150
                (100525, 0.22),   # 22% on income $47,151 to $100,525
                (191950, 0.24),   # 24% on income $100,526 to $191,950
                (243725, 0.32),   # 32% on income $191,951 to $243,725
                (365600, 0.35),   # 35% on income $243,726 to $365,600
                (float('inf'), 0.37)  # 37% on income over $365,600
            ],
            "Head of Household": [
                (16550, 0.10),    # 10% on income up to $16,550
                (63100, 0.12),    # 12% on income $16,551 to $63,100
                (100500, 0.22),   # 22% on income $63,101 to $100,500
                (191950, 0.24),   # 24% on income $100,501 to $191,950
                (243700, 0.32),   # 32% on income $191,951 to $243,700
                (609350, 0.35),   # 35% on income $243,701 to $609,350
                (float('inf'), 0.37)  # 37% on income over $609,350
            ]
        }
        return brackets.get(filing_status, brackets["Single"])
    
    def get_state_tax_rate(self, state, income):
        """Get state tax rate - simplified version for major states"""
        # This is a simplified version. In reality, many states have progressive brackets too
        state_rates = {
            "Alabama": 0.05, "Alaska": 0.0, "Arizona": 0.045, "Arkansas": 0.063,
            "California": 0.093, "Colorado": 0.0455, "Connecticut": 0.0699, "Delaware": 0.066,
            "Florida": 0.0, "Georgia": 0.057, "Hawaii": 0.11, "Idaho": 0.058,
            "Illinois": 0.0495, "Indiana": 0.032, "Iowa": 0.053, "Kansas": 0.057,
            "Kentucky": 0.06, "Louisiana": 0.0425, "Maine": 0.0715, "Maryland": 0.0575,
            "Massachusetts": 0.05, "Michigan": 0.0425, "Minnesota": 0.0985, "Mississippi": 0.05,
            "Missouri": 0.054, "Montana": 0.0675, "Nebraska": 0.0684, "Nevada": 0.0,
            "New Hampshire": 0.0, "New Jersey": 0.1075, "New Mexico": 0.059, "New York": 0.1090,
            "North Carolina": 0.0475, "North Dakota": 0.0295, "Ohio": 0.0399, "Oklahoma": 0.05,
            "Oregon": 0.099, "Pennsylvania": 0.0307, "Rhode Island": 0.0599, "South Carolina": 0.07,
            "South Dakota": 0.0, "Tennessee": 0.0, "Texas": 0.0, "Utah": 0.0495,
            "Vermont": 0.066, "Virginia": 0.0575, "Washington": 0.0, "West Virginia": 0.065,
            "Wisconsin": 0.0765, "Wyoming": 0.0
        }
        return state_rates.get(state, 0.0)
    
    def calculate_progressive_federal_tax(self, income, filing_status):
        """Calculate federal tax using progressive brackets"""
        brackets = self.get_federal_tax_brackets_2025(filing_status)
        total_tax = 0
        prev_bracket = 0
        
        for bracket_limit, rate in brackets:
            if income <= prev_bracket:
                break
            
            taxable_in_bracket = min(income, bracket_limit) - prev_bracket
            total_tax += taxable_in_bracket * rate
            prev_bracket = bracket_limit
            
            if income <= bracket_limit:
                break
        
        return total_tax
    
    def calculate_fica_tax(self, income):
        """Calculate FICA taxes (Social Security + Medicare)"""
        # Social Security: 6.2% up to $168,600 (2025 limit)
        # Medicare: 1.45% on all income
        # Additional Medicare: 0.9% on income over $200,000 (single) / $250,000 (married)
        
        ss_rate = 0.062
        ss_wage_base = 168600  # 2025 Social Security wage base
        medicare_rate = 0.0145
        additional_medicare_rate = 0.009
        additional_medicare_threshold = 200000  # Single filer threshold
        
        # Social Security tax
        ss_tax = min(income, ss_wage_base) * ss_rate
        
        # Medicare tax
        medicare_tax = income * medicare_rate
        
        # Additional Medicare tax (if applicable)
        additional_medicare_tax = 0
        if income > additional_medicare_threshold:
            additional_medicare_tax = (income - additional_medicare_threshold) * additional_medicare_rate
        
        return ss_tax + medicare_tax + additional_medicare_tax
    
    def get_float_value(self, var, entry_widget=None):
        """Safely get float value from StringVar, using placeholder text as default if present"""
        try:
            value = var.get().strip()
            if not value:
                return 0.0
            # If entry widget is provided and text is gray (placeholder), use the placeholder value
            if entry_widget and entry_widget.cget('fg') == 'gray':
                return float(value)  # Use the placeholder value as actual default
            return float(value)
        except (ValueError, AttributeError):
            return 0.0
    
    def calculate_salary(self):
        """Calculate the required salary"""
        try:
            # Get all expense values
            rent = self.get_float_value(self.rent_var, self.rent_entry)
            car = self.get_float_value(self.car_var, self.car_entry)
            insurance = self.get_float_value(self.insurance_var, self.insurance_entry)
            food = self.get_float_value(self.food_var, self.food_entry)
            utilities = self.get_float_value(self.utilities_var, self.utilities_entry)
            phone = self.get_float_value(self.phone_var, self.phone_entry)
            other_expenses = self.get_float_value(self.other_expenses_var, self.other_expenses_entry)
            
            # Loan payments
            loan_payments = self.get_float_value(self.loan_payments_var)
            extra_loan = self.get_float_value(self.extra_loan_var, self.extra_loan_entry)
            
            # Savings and extras
            savings = self.get_float_value(self.savings_var, self.savings_entry)
            entertainment = self.get_float_value(self.entertainment_var, self.entertainment_entry)
            
            # Retirement and investment contributions
            contribution_401k = self.get_float_value(self.contribution_401k_var, self.contribution_401k_entry)
            traditional_ira = self.get_float_value(self.traditional_ira_var, self.traditional_ira_entry)
            roth_ira = self.get_float_value(self.roth_ira_var, self.roth_ira_entry)
            hsa = self.get_float_value(self.hsa_var, self.hsa_entry)
            education_529 = self.get_float_value(self.education_529_var, self.education_529_entry)
            other_investments = self.get_float_value(self.other_investments_var, self.other_investments_entry)
            
            # Minimum leftover amount
            min_leftover = self.get_float_value(self.min_leftover_var, self.min_leftover_entry)
            
            # Calculate total pre-tax contributions (reduce taxable income)
            pre_tax_contributions = contribution_401k + traditional_ira + hsa
            
            # Calculate total after-tax contributions (paid with net income)
            after_tax_contributions = roth_ira + education_529 + other_investments
            
            # Calculate total monthly expenses (after-tax needs) including desired leftover amount
            total_monthly_expenses = (rent + car + insurance + food + utilities + 
                                    phone + other_expenses + loan_payments + 
                                    extra_loan + savings + entertainment + min_leftover + 
                                    after_tax_contributions)
            
            # Calculate required salary using iterative approach for progressive taxes
            if self.tax_method_var.get() == "Progressive":
                required_gross_annual = self.calculate_required_salary_progressive(total_monthly_expenses * 12, pre_tax_contributions * 12)
            else:
                required_gross_annual = self.calculate_required_salary_flat(total_monthly_expenses * 12, pre_tax_contributions * 12)
            
            required_gross_monthly = required_gross_annual / 12
            required_hourly = required_gross_annual / (52 * 40)  # 52 weeks * 40 hours per week
            
            # Calculate taxable income (gross minus pre-tax contributions)
            taxable_income_annual = required_gross_annual - (pre_tax_contributions * 12)
            
            # Calculate actual taxes and tithe for the required salary
            if self.tax_method_var.get() == "Progressive":
                federal_tax_annual = self.calculate_progressive_federal_tax(taxable_income_annual, self.filing_status_var.get())
                state_rate = self.get_state_tax_rate(self.state_var.get(), taxable_income_annual)
                state_tax_annual = taxable_income_annual * state_rate
                fica_tax_annual = self.calculate_fica_tax(required_gross_annual)  # FICA is on gross, not taxable
            else:
                federal_tax_rate = self.get_float_value(self.federal_tax_var) / 100
                state_tax_rate = self.get_float_value(self.state_tax_var) / 100
                fica_tax_rate = self.get_float_value(self.fica_tax_var) / 100
                
                federal_tax_annual = taxable_income_annual * federal_tax_rate
                state_tax_annual = taxable_income_annual * state_tax_rate
                fica_tax_annual = required_gross_annual * fica_tax_rate  # FICA is on gross
            
            total_taxes_annual = federal_tax_annual + state_tax_annual + fica_tax_annual
            
            # Calculate tithe
            tithe_annual = 0
            if self.tithe_enabled_var.get():
                tithe_rate = self.get_float_value(self.tithe_var) / 100
                if self.tithe_basis_var.get() == "Gross Income":
                    tithe_annual = required_gross_annual * tithe_rate
                else:  # Net Income
                    net_income_annual = required_gross_annual - total_taxes_annual - (pre_tax_contributions * 12)
                    tithe_annual = net_income_annual * tithe_rate
            
            # Calculate final breakdown
            net_income_annual = required_gross_annual - total_taxes_annual - tithe_annual - (pre_tax_contributions * 12)
            # Calculate actual expenses (everything except the min_leftover target)
            actual_expenses_annual = ((rent + car + insurance + food + utilities + 
                                     phone + other_expenses + loan_payments + 
                                     extra_loan + savings + entertainment) * 12) + (after_tax_contributions * 12)
            # The leftover is what remains after all actual expenses
            leftover_annual = net_income_annual - actual_expenses_annual
            
            # Store results for saving
            self.last_calculation_results = {
                'gross_annual': required_gross_annual,
                'gross_monthly': required_gross_monthly,
                'hourly_wage': required_hourly,
                'taxable_income_annual': taxable_income_annual,
                'pre_tax_contributions': pre_tax_contributions,
                'after_tax_contributions': after_tax_contributions,
                'total_taxes': total_taxes_annual / 12,
                'tithe': tithe_annual / 12,
                'net_income': net_income_annual / 12,
                'total_expenses': actual_expenses_annual / 12,  # Show actual expenses (no leftover target)
                'leftover': leftover_annual / 12,
                'min_leftover_requested': min_leftover,
                'tax_breakdown': {
                    'federal': federal_tax_annual / 12,
                    'state': state_tax_annual / 12,
                    'fica': fica_tax_annual / 12
                },
                'tithe_enabled': self.tithe_enabled_var.get(),
                'tax_method': self.tax_method_var.get(),
                'calculation_inputs': {
                    'rent': rent,
                    'car': car,
                    'insurance': insurance,
                    'food': food,
                    'utilities': utilities,
                    'phone': phone,
                    'other_expenses': other_expenses,
                    'loan_payments': loan_payments,
                    'extra_loan': extra_loan,
                    'savings': savings,
                    'entertainment': entertainment,
                    'min_leftover': min_leftover,
                    'contribution_401k': contribution_401k,
                    'traditional_ira': traditional_ira,
                    'roth_ira': roth_ira,
                    'hsa': hsa,
                    'education_529': education_529,
                    'other_investments': other_investments,
                    'filing_status': self.filing_status_var.get() if self.tax_method_var.get() == "Progressive" else None,
                    'state': self.state_var.get() if self.tax_method_var.get() == "Progressive" else None,
                    'federal_tax_rate': self.get_float_value(self.federal_tax_var) if self.tax_method_var.get() == "Flat Rate" else None,
                    'state_tax_rate': self.get_float_value(self.state_tax_var) if self.tax_method_var.get() == "Flat Rate" else None,
                    'fica_rate': self.get_float_value(self.fica_tax_var),
                    'tithe_rate': self.get_float_value(self.tithe_var) if self.tithe_enabled_var.get() else 0,
                    'tithe_basis': self.tithe_basis_var.get() if self.tithe_enabled_var.get() else None
                }
            }
            
            # Display results
            self.display_results(self.last_calculation_results)
            
            # Show save button
            self.save_button.grid()
            
        except Exception as e:
            messagebox.showerror("Calculation Error", f"Error calculating salary: {str(e)}")
    
    def calculate_required_salary_progressive(self, annual_expenses, pre_tax_contributions_annual=0):
        """Calculate required salary using iterative approach for progressive taxes"""
        # Start with an estimate
        estimated_salary = (annual_expenses + pre_tax_contributions_annual) * 1.5  # Initial guess
        
        # Iteratively refine the estimate
        for iteration in range(20):  # Increased to 20 iterations for better convergence
            # Calculate taxable income (gross minus pre-tax contributions)
            taxable_income = estimated_salary - pre_tax_contributions_annual
            
            # Calculate taxes for current estimate
            federal_tax = self.calculate_progressive_federal_tax(taxable_income, self.filing_status_var.get())
            state_rate = self.get_state_tax_rate(self.state_var.get(), taxable_income)
            state_tax = taxable_income * state_rate
            fica_tax = self.calculate_fica_tax(estimated_salary)  # FICA on gross income
            total_taxes = federal_tax + state_tax + fica_tax
            
            # Calculate tithe
            tithe = 0
            if self.tithe_enabled_var.get():
                tithe_rate = self.get_float_value(self.tithe_var) / 100
                if self.tithe_basis_var.get() == "Gross Income":
                    tithe = estimated_salary * tithe_rate
                else:  # Net Income
                    net_income = estimated_salary - total_taxes - pre_tax_contributions_annual
                    tithe = net_income * tithe_rate
            
            # Calculate net income after taxes, tithe, and pre-tax contributions
            net_income = estimated_salary - total_taxes - tithe - pre_tax_contributions_annual
            
            # Check convergence with tighter tolerance and percentage-based check
            difference = abs(net_income - annual_expenses)
            if difference < 50 or (annual_expenses > 0 and difference / annual_expenses < 0.001):  # Within $50 or 0.1%
                break
            
            # More gradual adjustment for better convergence
            adjustment_factor = min(difference / annual_expenses, 0.1) if annual_expenses > 0 else 0.05
            if net_income < annual_expenses:
                estimated_salary *= (1 + adjustment_factor)  # Increase based on difference
            else:
                estimated_salary *= (1 - adjustment_factor * 0.5)  # Decrease more gradually
        
        return estimated_salary
    
    def calculate_required_salary_flat(self, annual_expenses, pre_tax_contributions_annual=0):
        """Calculate required salary using flat tax rates"""
        federal_tax_rate = self.get_float_value(self.federal_tax_var) / 100
        state_tax_rate = self.get_float_value(self.state_tax_var) / 100
        fica_tax_rate = self.get_float_value(self.fica_tax_var) / 100
        
        # Note: Federal and state taxes apply to taxable income (gross - pre-tax contributions)
        # FICA applies to gross income
        taxable_tax_rate = federal_tax_rate + state_tax_rate
        
        tithe_rate = 0
        if self.tithe_enabled_var.get():
            tithe_rate = self.get_float_value(self.tithe_var) / 100
        
        # This is a simplified calculation for flat taxes with pre-tax contributions
        # Formula needs to account for FICA on gross and other taxes on taxable income
        if self.tithe_basis_var.get() == "Gross Income":
            # Iterative approach for flat tax with pre-tax contributions
            estimated_salary = (annual_expenses + pre_tax_contributions_annual) * 1.4
            for _ in range(15):  # Increased iterations
                taxable_income = estimated_salary - pre_tax_contributions_annual
                taxes = taxable_income * taxable_tax_rate + estimated_salary * fica_tax_rate
                tithe = estimated_salary * tithe_rate
                net_income = estimated_salary - taxes - tithe - pre_tax_contributions_annual
                
                # Improved convergence check
                difference = abs(net_income - annual_expenses)
                if difference < 50 or (annual_expenses > 0 and difference / annual_expenses < 0.001):
                    break
                    
                # More gradual adjustment
                adjustment_factor = min(difference / annual_expenses, 0.1) if annual_expenses > 0 else 0.05
                if net_income < annual_expenses:
                    estimated_salary *= (1 + adjustment_factor)
                else:
                    estimated_salary *= (1 - adjustment_factor * 0.5)
                    
            required_gross = estimated_salary
        else:  # Net Income tithe
            # Similar iterative approach for net income tithe
            estimated_salary = (annual_expenses + pre_tax_contributions_annual) * 1.4
            for _ in range(15):  # Increased iterations
                taxable_income = estimated_salary - pre_tax_contributions_annual
                taxes = taxable_income * taxable_tax_rate + estimated_salary * fica_tax_rate
                net_before_tithe = estimated_salary - taxes - pre_tax_contributions_annual
                tithe = net_before_tithe * tithe_rate
                net_income = net_before_tithe - tithe
                
                # Improved convergence check
                difference = abs(net_income - annual_expenses)
                if difference < 50 or (annual_expenses > 0 and difference / annual_expenses < 0.001):
                    break
                    
                # More gradual adjustment
                adjustment_factor = min(difference / annual_expenses, 0.1) if annual_expenses > 0 else 0.05
                if net_income < annual_expenses:
                    estimated_salary *= (1 + adjustment_factor)
                else:
                    estimated_salary *= (1 - adjustment_factor * 0.5)
                    
            required_gross = estimated_salary
        
        return required_gross
    
    def display_results(self, results):
        """Display the calculation results"""
        # Clear existing results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Title
        title = tk.Label(self.results_frame, text="Required Salary Calculation", 
                        font=font.Font(size=14, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, pady=10)
        
        row = 1
        
        # Annual Salary
        tk.Label(self.results_frame, text="Required Annual Salary:", 
                font=font.Font(weight="bold")).grid(row=row, column=0, sticky='w', padx=10, pady=5)
        tk.Label(self.results_frame, text=f"${results['gross_annual']:,.2f}", 
                font=font.Font(weight="bold", size=12), fg="green").grid(row=row, column=1, sticky='w', padx=10, pady=5)
        row += 1
        
        # Hourly Wage
        tk.Label(self.results_frame, text="Required Hourly Wage:", 
                font=font.Font(weight="bold")).grid(row=row, column=0, sticky='w', padx=10, pady=5)
        tk.Label(self.results_frame, text=f"${results['hourly_wage']:,.2f}/hour", 
                font=font.Font(weight="bold", size=12), fg="green").grid(row=row, column=1, sticky='w', padx=10, pady=5)
        row += 1
        
        # Work assumption note
        tk.Label(self.results_frame, text="(Based on 40 hours/week)", 
                font=font.Font(size=9), fg="gray").grid(row=row, column=1, sticky='w', padx=10, pady=(0, 5))
        row += 1
        
        # Monthly Breakdown
        tk.Label(self.results_frame, text="Monthly Breakdown:", 
                font=font.Font(weight="bold")).grid(row=row, column=0, columnspan=2, sticky='w', padx=10, pady=(15, 5))
        row += 1
        
        # Gross Monthly
        tk.Label(self.results_frame, text="  Gross Monthly Income:").grid(row=row, column=0, sticky='w', padx=20, pady=2)
        tk.Label(self.results_frame, text=f"${results['gross_monthly']:,.2f}").grid(row=row, column=1, sticky='w', padx=10, pady=2)
        row += 1
        
        # Tax breakdown
        tk.Label(self.results_frame, text="  Federal Tax:").grid(row=row, column=0, sticky='w', padx=20, pady=2)
        tk.Label(self.results_frame, text=f"-${results['tax_breakdown']['federal']:,.2f}", fg="red").grid(row=row, column=1, sticky='w', padx=10, pady=2)
        row += 1
        
        tk.Label(self.results_frame, text="  State Tax:").grid(row=row, column=0, sticky='w', padx=20, pady=2)
        tk.Label(self.results_frame, text=f"-${results['tax_breakdown']['state']:,.2f}", fg="red").grid(row=row, column=1, sticky='w', padx=10, pady=2)
        row += 1
        
        tk.Label(self.results_frame, text="  FICA Tax:").grid(row=row, column=0, sticky='w', padx=20, pady=2)
        tk.Label(self.results_frame, text=f"-${results['tax_breakdown']['fica']:,.2f}", fg="red").grid(row=row, column=1, sticky='w', padx=10, pady=2)
        row += 1
        
        # Pre-tax contributions (if any)
        if results['pre_tax_contributions'] > 0:
            tk.Label(self.results_frame, text="  Pre-tax Contributions:").grid(row=row, column=0, sticky='w', padx=20, pady=2)
            tk.Label(self.results_frame, text=f"-${results['pre_tax_contributions']:,.2f}", fg="orange").grid(row=row, column=1, sticky='w', padx=10, pady=2)
            row += 1
        
        # Tithe (if enabled)
        if results['tithe_enabled']:
            tk.Label(self.results_frame, text="  Tithe:").grid(row=row, column=0, sticky='w', padx=20, pady=2)
            tk.Label(self.results_frame, text=f"-${results['tithe']:,.2f}", fg="#A400BA").grid(row=row, column=1, sticky='w', padx=10, pady=2)
            row += 1
        
        # Net Income
        tk.Label(self.results_frame, text="  Net Income:").grid(row=row, column=0, sticky='w', padx=20, pady=2)
        tk.Label(self.results_frame, text=f"${results['net_income']:,.2f}", 
                font=font.Font(weight="bold")).grid(row=row, column=1, sticky='w', padx=10, pady=2)
        row += 1
        
        # Total Expenses
        tk.Label(self.results_frame, text="  Total Expenses:").grid(row=row, column=0, sticky='w', padx=20, pady=2)
        tk.Label(self.results_frame, text=f"-${results['total_expenses']:,.2f}", fg="red").grid(row=row, column=1, sticky='w', padx=10, pady=2)
        row += 1
        
        # Leftover
        leftover_color = "green" if results['leftover'] >= 0 else "red"
        tk.Label(self.results_frame, text="  Money Left Over:").grid(row=row, column=0, sticky='w', padx=20, pady=2)
        tk.Label(self.results_frame, text=f"${results['leftover']:,.2f}", 
                fg=leftover_color, font=font.Font(weight="bold")).grid(row=row, column=1, sticky='w', padx=10, pady=2)
        row += 1
        
        # Show requested minimum leftover for reference
        if 'min_leftover_requested' in results and results['min_leftover_requested'] > 0:
            tk.Label(self.results_frame, text="  (Requested minimum:").grid(row=row, column=0, sticky='w', padx=20, pady=2)
            tk.Label(self.results_frame, text=f"${results['min_leftover_requested']:,.2f})", 
                    fg="gray").grid(row=row, column=1, sticky='w', padx=10, pady=2)
            row += 1
        
        # Warning if negative
        if results['leftover'] < 0:
            warning = tk.Label(self.results_frame, text="⚠️ Warning: Expenses exceed available income!", 
                             fg="red", font=font.Font(weight="bold"))
            warning.grid(row=row, column=0, columnspan=2, pady=10)
            row += 1
        
        # Tax method info
        method_info = f"Calculation Method: {results['tax_method']} Tax"
        if results['tax_method'] == "Progressive":
            method_info += f" ({self.filing_status_var.get()}, {self.state_var.get()})"
        
        tk.Label(self.results_frame, text=method_info, 
                font=font.Font(size=9), fg="gray").grid(row=row, column=0, columnspan=2, pady=(10, 5))

    def save_results(self):
        """Save the calculation results to a file"""
        if not self.last_calculation_results:
            messagebox.showwarning("No Results", "Please calculate salary requirements first.")
            return
        
        try:
            # Get save file path
            file_path = filedialog.asksaveasfilename(
                title="Save Salary Calculation Results",
                defaultextension=".txt",
                filetypes=[
                    ("Text files", "*.txt"),
                    ("CSV files", "*.csv"),
                    ("All files", "*.*")
                ],
                initialname=f"salary_calculation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            
            if not file_path:
                return
            
            # Determine file format based on extension
            file_extension = file_path.lower().split('.')[-1]
            
            if file_extension == 'csv':
                self.save_as_csv(file_path)
            else:
                self.save_as_text(file_path)
                
            messagebox.showinfo("Success", f"Results saved to {file_path}")
            
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save results: {str(e)}")
    
    def save_as_text(self, file_path):
        """Save results as formatted text file"""
        results = self.last_calculation_results
        inputs = results['calculation_inputs']
        
        with open(file_path, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("SALARY REQUIREMENTS CALCULATION RESULTS\n")
            f.write("=" * 60 + "\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Summary
            f.write("SUMMARY\n")
            f.write("-" * 30 + "\n")
            f.write(f"Required Annual Salary: ${results['gross_annual']:,.2f}\n")
            f.write(f"Required Monthly Income: ${results['gross_monthly']:,.2f}\n")
            f.write(f"Required Hourly Wage: ${results['hourly_wage']:,.2f}/hour (40 hrs/week)\n")
            f.write(f"Monthly Money Left Over: ${results['leftover']:,.2f}\n\n")
            
            # Monthly Breakdown
            f.write("MONTHLY BREAKDOWN\n")
            f.write("-" * 30 + "\n")
            f.write(f"Gross Monthly Income:     ${results['gross_monthly']:>10,.2f}\n")
            f.write(f"  Federal Tax:           -${results['tax_breakdown']['federal']:>10,.2f}\n")
            f.write(f"  State Tax:             -${results['tax_breakdown']['state']:>10,.2f}\n")
            f.write(f"  FICA Tax:              -${results['tax_breakdown']['fica']:>10,.2f}\n")
            
            if results['pre_tax_contributions'] > 0:
                f.write(f"  Pre-tax Contributions: -${results['pre_tax_contributions']:>10,.2f}\n")
            
            if results['tithe_enabled']:
                f.write(f"  Tithe:                 -${results['tithe']:>10,.2f}\n")
            
            f.write(f"Net Income:               ${results['net_income']:>10,.2f}\n")
            f.write(f"Total Expenses:          -${results['total_expenses']:>10,.2f}\n")
            f.write(f"Money Left Over:          ${results['leftover']:>10,.2f}\n\n")
            
            # Expense Details
            f.write("EXPENSE BREAKDOWN\n")
            f.write("-" * 30 + "\n")
            f.write(f"Rent/Mortgage:            ${inputs['rent']:>10,.2f}\n")
            f.write(f"Car Payment:              ${inputs['car']:>10,.2f}\n")
            f.write(f"Insurance:                ${inputs['insurance']:>10,.2f}\n")
            f.write(f"Food & Groceries:         ${inputs['food']:>10,.2f}\n")
            f.write(f"Utilities:                ${inputs['utilities']:>10,.2f}\n")
            f.write(f"Phone & Internet:         ${inputs['phone']:>10,.2f}\n")
            f.write(f"Other Expenses:           ${inputs['other_expenses']:>10,.2f}\n")
            f.write(f"Loan Payments:            ${inputs['loan_payments']:>10,.2f}\n")
            f.write(f"Extra Loan Payments:      ${inputs['extra_loan']:>10,.2f}\n")
            f.write(f"Savings:                  ${inputs['savings']:>10,.2f}\n")
            f.write(f"Entertainment:            ${inputs['entertainment']:>10,.2f}\n")
            if 'min_leftover' in inputs and inputs['min_leftover'] > 0:
                f.write(f"Minimum Leftover Req.:    ${inputs['min_leftover']:>10,.2f}\n")
            f.write(f"{'':->43}\n")
            f.write(f"Total Monthly Expenses:   ${results['total_expenses']:>10,.2f}\n\n")
            
            # Retirement & Investment Contributions
            if (inputs.get('contribution_401k', 0) + inputs.get('traditional_ira', 0) + 
                inputs.get('roth_ira', 0) + inputs.get('hsa', 0) + 
                inputs.get('education_529', 0) + inputs.get('other_investments', 0)) > 0:
                f.write("RETIREMENT & INVESTMENT CONTRIBUTIONS\n")
                f.write("-" * 30 + "\n")
                if inputs.get('contribution_401k', 0) > 0:
                    f.write(f"401(k) Contribution:      ${inputs['contribution_401k']:>10,.2f}\n")
                if inputs.get('traditional_ira', 0) > 0:
                    f.write(f"Traditional IRA:          ${inputs['traditional_ira']:>10,.2f}\n")
                if inputs.get('roth_ira', 0) > 0:
                    f.write(f"Roth IRA:                 ${inputs['roth_ira']:>10,.2f}\n")
                if inputs.get('hsa', 0) > 0:
                    f.write(f"HSA Contribution:         ${inputs['hsa']:>10,.2f}\n")
                if inputs.get('education_529', 0) > 0:
                    f.write(f"529 Education Plan:       ${inputs['education_529']:>10,.2f}\n")
                if inputs.get('other_investments', 0) > 0:
                    f.write(f"Other Investments:        ${inputs['other_investments']:>10,.2f}\n")
                f.write(f"{'':->43}\n")
                f.write(f"Total Pre-tax:            ${results['pre_tax_contributions']:>10,.2f}\n")
                f.write(f"Total After-tax:          ${results['after_tax_contributions']:>10,.2f}\n\n")
            
            # Tax Information
            f.write("TAX CALCULATION DETAILS\n")
            f.write("-" * 30 + "\n")
            f.write(f"Method: {results['tax_method']} Tax Calculation\n")
            
            if results['tax_method'] == "Progressive":
                f.write(f"Filing Status: {inputs['filing_status']}\n")
                f.write(f"State: {inputs['state']}\n")
            else:
                f.write(f"Federal Tax Rate: {inputs['federal_tax_rate']:.2f}%\n")
                f.write(f"State Tax Rate: {inputs['state_tax_rate']:.2f}%\n")
            
            f.write(f"FICA Tax Rate: {inputs['fica_rate']:.2f}%\n")
            
            if results['tithe_enabled']:
                f.write(f"Tithe Rate: {inputs['tithe_rate']:.2f}%\n")
                f.write(f"Tithe Calculated On: {inputs['tithe_basis']}\n")
            
            f.write("\n" + "=" * 60 + "\n")
            f.write("Note: Results are estimates. Consult a tax professional for precise calculations.\n")
    
    def save_as_csv(self, file_path):
        """Save results as CSV file"""
        results = self.last_calculation_results
        inputs = results['calculation_inputs']
        
        with open(file_path, 'w', newline='') as f:
            f.write("Salary Calculation Results\n")
            f.write(f"Generated on,{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Summary section
            f.write("Summary\n")
            f.write("Item,Amount\n")
            f.write(f"Required Annual Salary,${results['gross_annual']:,.2f}\n")
            f.write(f"Required Monthly Income,${results['gross_monthly']:,.2f}\n")
            f.write(f"Required Hourly Wage,${results['hourly_wage']:,.2f}/hour\n")
            f.write(f"Monthly Money Left Over,${results['leftover']:,.2f}\n\n")
            
            # Monthly breakdown
            f.write("Monthly Breakdown\n")
            f.write("Category,Amount\n")
            f.write(f"Gross Monthly Income,${results['gross_monthly']:,.2f}\n")
            f.write(f"Federal Tax,-${results['tax_breakdown']['federal']:,.2f}\n")
            f.write(f"State Tax,-${results['tax_breakdown']['state']:,.2f}\n")
            f.write(f"FICA Tax,-${results['tax_breakdown']['fica']:,.2f}\n")
            
            if results['pre_tax_contributions'] > 0:
                f.write(f"Pre-tax Contributions,-${results['pre_tax_contributions']:,.2f}\n")
            
            if results['tithe_enabled']:
                f.write(f"Tithe,-${results['tithe']:,.2f}\n")
            
            f.write(f"Net Income,${results['net_income']:,.2f}\n")
            f.write(f"Total Expenses,-${results['total_expenses']:,.2f}\n")
            f.write(f"Money Left Over,${results['leftover']:,.2f}\n\n")
            
            # Expenses
            f.write("Expense Breakdown\n")
            f.write("Category,Amount\n")
            f.write(f"Rent/Mortgage,${inputs['rent']:,.2f}\n")
            f.write(f"Car Payment,${inputs['car']:,.2f}\n")
            f.write(f"Insurance,${inputs['insurance']:,.2f}\n")
            f.write(f"Food & Groceries,${inputs['food']:,.2f}\n")
            f.write(f"Utilities,${inputs['utilities']:,.2f}\n")
            f.write(f"Phone & Internet,${inputs['phone']:,.2f}\n")
            f.write(f"Other Expenses,${inputs['other_expenses']:,.2f}\n")
            f.write(f"Loan Payments,${inputs['loan_payments']:,.2f}\n")
            f.write(f"Extra Loan Payments,${inputs['extra_loan']:,.2f}\n")
            f.write(f"Savings,${inputs['savings']:,.2f}\n")
            f.write(f"Entertainment,${inputs['entertainment']:,.2f}\n")
            if 'min_leftover' in inputs and inputs['min_leftover'] > 0:
                f.write(f"Minimum Leftover Required,${inputs['min_leftover']:,.2f}\n")
            f.write("\n")
            
            # Retirement & Investment Contributions
            if (inputs.get('contribution_401k', 0) + inputs.get('traditional_ira', 0) + 
                inputs.get('roth_ira', 0) + inputs.get('hsa', 0) + 
                inputs.get('education_529', 0) + inputs.get('other_investments', 0)) > 0:
                f.write("Retirement & Investment Contributions\n")
                f.write("Category,Amount\n")
                if inputs.get('contribution_401k', 0) > 0:
                    f.write(f"401(k) Contribution,${inputs['contribution_401k']:,.2f}\n")
                if inputs.get('traditional_ira', 0) > 0:
                    f.write(f"Traditional IRA,${inputs['traditional_ira']:,.2f}\n")
                if inputs.get('roth_ira', 0) > 0:
                    f.write(f"Roth IRA,${inputs['roth_ira']:,.2f}\n")
                if inputs.get('hsa', 0) > 0:
                    f.write(f"HSA Contribution,${inputs['hsa']:,.2f}\n")
                if inputs.get('education_529', 0) > 0:
                    f.write(f"529 Education Plan,${inputs['education_529']:,.2f}\n")
                if inputs.get('other_investments', 0) > 0:
                    f.write(f"Other Investments,${inputs['other_investments']:,.2f}\n")
                f.write(f"Total Pre-tax,${results['pre_tax_contributions']:,.2f}\n")
                f.write(f"Total After-tax,${results['after_tax_contributions']:,.2f}\n\n")
            
            # Settings
            f.write("Calculation Settings\n")
            f.write("Setting,Value\n")
            f.write(f"Tax Method,{results['tax_method']}\n")
            
            if results['tax_method'] == "Progressive":
                f.write(f"Filing Status,{inputs['filing_status']}\n")
                f.write(f"State,{inputs['state']}\n")
            else:
                f.write(f"Federal Tax Rate,{inputs['federal_tax_rate']:.2f}%\n")
                f.write(f"State Tax Rate,{inputs['state_tax_rate']:.2f}%\n")
            
            f.write(f"FICA Tax Rate,{inputs['fica_rate']:.2f}%\n")
            
            if results['tithe_enabled']:
                f.write(f"Tithe Enabled,Yes\n")
                f.write(f"Tithe Rate,{inputs['tithe_rate']:.2f}%\n")
                f.write(f"Tithe Basis,{inputs['tithe_basis']}\n")
            else:
                f.write(f"Tithe Enabled,No\n")