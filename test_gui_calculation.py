#!/usr/bin/env python3
"""
Test the exact GUI calculation logic to find the issue
"""
import sys
import os

# Add the current directory to the path so we can import the GUI module
sys.path.insert(0, '/Users/matthewdulcich/Documents/DevProjects/loan-manager')

# Mock tkinter classes to avoid GUI dependency
class MockStringVar:
    def __init__(self, value=""):
        self._value = str(value)
    
    def get(self):
        return self._value
    
    def set(self, value):
        self._value = str(value)

class MockEntry:
    def __init__(self, value="", fg='white'):
        self._value = str(value)
        self._fg = fg
    
    def get(self):
        return self._value
    
    def cget(self, prop):
        if prop == 'fg':
            return self._fg
        return None

class MockBooleanVar:
    def __init__(self, value=False):
        self._value = value
    
    def get(self):
        return self._value

# Create a test version of the salary calculator logic
class TestSalaryCalculator:
    def __init__(self):
        # Initialize all the variables with default values
        self.rent_var = MockStringVar("1800")
        self.rent_entry = MockEntry("1800", "gray")
        
        self.car_var = MockStringVar("450")
        self.car_entry = MockEntry("450", "gray")
        
        self.insurance_var = MockStringVar("350")
        self.insurance_entry = MockEntry("350", "gray")
        
        self.food_var = MockStringVar("600")
        self.food_entry = MockEntry("600", "gray")
        
        self.utilities_var = MockStringVar("200")
        self.utilities_entry = MockEntry("200", "gray")
        
        self.phone_var = MockStringVar("150")
        self.phone_entry = MockEntry("150", "gray")
        
        self.other_expenses_var = MockStringVar("300")
        self.other_expenses_entry = MockEntry("300", "gray")
        
        self.loan_payments_var = MockStringVar("0")
        self.extra_loan_var = MockStringVar("200")
        self.extra_loan_entry = MockEntry("200", "gray")
        
        self.savings_var = MockStringVar("500")
        self.savings_entry = MockEntry("500", "gray")
        
        self.entertainment_var = MockStringVar("400")
        self.entertainment_entry = MockEntry("400", "gray")
        
        # Retirement accounts
        self.contribution_401k_var = MockStringVar("800")
        self.contribution_401k_entry = MockEntry("800", "gray")
        
        self.traditional_ira_var = MockStringVar("0")
        self.traditional_ira_entry = MockEntry("0", "gray")
        
        self.roth_ira_var = MockStringVar("500")
        self.roth_ira_entry = MockEntry("500", "gray")
        
        self.hsa_var = MockStringVar("300")
        self.hsa_entry = MockEntry("300", "gray")
        
        self.education_529_var = MockStringVar("0")
        self.education_529_entry = MockEntry("0", "gray")
        
        self.other_investments_var = MockStringVar("200")
        self.other_investments_entry = MockEntry("200", "gray")
        
        # Tax settings
        self.tax_method_var = MockStringVar("Progressive")
        self.filing_status_var = MockStringVar("Single")
        self.state_var = MockStringVar("Maryland")
        self.federal_tax_var = MockStringVar("22")
        self.state_tax_var = MockStringVar("6")
        self.fica_tax_var = MockStringVar("7.65")
        
        # Tithe settings
        self.tithe_enabled_var = MockBooleanVar(True)
        self.tithe_var = MockStringVar("10")
        self.tithe_basis_var = MockStringVar("Gross Income")
        
        # Min leftover - this is what we want to test with different values
        self.min_leftover_var = MockStringVar("0")  # Start with 0 to test the issue
        self.min_leftover_entry = MockEntry("0", "white")  # White means user entered it
    
    def get_float_value(self, var, entry_widget=None):
        """Copy of the exact method from GUI"""
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
    
    def get_federal_tax_brackets_2025(self, filing_status):
        """Copy from GUI"""
        brackets = {
            "Single": [
                (11600, 0.10),    # 10% on income up to $11,600
                (47150, 0.12),    # 12% on income $11,601 to $47,150
                (100525, 0.22),   # 22% on income $47,151 to $100,525
                (191950, 0.24),   # 24% on income $100,526 to $191,950
                (243725, 0.32),   # 32% on income $191,951 to $243,725
                (609350, 0.35),   # 35% on income $243,726 to $609,350
                (float('inf'), 0.37)  # 37% on income over $609,350
            ]
        }
        return brackets.get(filing_status, brackets["Single"])
    
    def calculate_progressive_federal_tax(self, income, filing_status):
        """Copy from GUI"""
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
        """Copy from GUI"""
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
    
    def get_state_tax_rate(self, state, income):
        """Copy from GUI"""
        state_rates = {
            "Maryland": 0.0575,
        }
        return state_rates.get(state, 0.0)
    
    def calculate_required_salary_progressive(self, annual_expenses, pre_tax_contributions_annual=0):
        """Copy from GUI"""
        # Start with an estimate
        estimated_salary = (annual_expenses + pre_tax_contributions_annual) * 1.5  # Initial guess
        
        # Iteratively refine the estimate
        for iteration in range(15):  # Maximum 15 iterations for better convergence
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
            
            # Check if net income covers expenses
            if abs(net_income - annual_expenses) < 100:  # Within $100
                print(f"Converged on iteration {iteration + 1}: salary=${estimated_salary:.2f}, net=${net_income:.2f}, target=${annual_expenses:.2f}")
                break
            
            # Adjust estimate
            if net_income < annual_expenses:
                estimated_salary *= 1.05  # Increase by 5%
            else:
                estimated_salary *= 0.98  # Decrease by 2%
        
        return estimated_salary
    
    def test_calculate_salary(self):
        """Copy the exact calculate_salary logic from GUI"""
        print("Testing salary calculation with min_leftover = 0")
        print("="*60)
        
        # Get all expense values using the exact same logic
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
        
        print(f"Min leftover value: ${min_leftover}")
        print(f"Min leftover color: {self.min_leftover_entry.cget('fg')}")
        
        # Calculate total pre-tax contributions (reduce taxable income)
        pre_tax_contributions = contribution_401k + traditional_ira + hsa
        
        # Calculate total after-tax contributions (paid with net income)
        after_tax_contributions = roth_ira + education_529 + other_investments
        
        # Calculate total monthly expenses (after-tax needs) including desired leftover amount
        total_monthly_expenses = (rent + car + insurance + food + utilities + 
                                phone + other_expenses + loan_payments + 
                                extra_loan + savings + entertainment + min_leftover + 
                                after_tax_contributions)
        
        print(f"Basic expenses: ${rent + car + insurance + food + utilities + phone + other_expenses + loan_payments + extra_loan + savings + entertainment}")
        print(f"After-tax retirement: ${after_tax_contributions}")
        print(f"Min leftover target: ${min_leftover}")
        print(f"Total monthly target: ${total_monthly_expenses}")
        
        # Calculate required salary using iterative approach for progressive taxes
        required_gross_annual = self.calculate_required_salary_progressive(total_monthly_expenses * 12, pre_tax_contributions * 12)
        
        # Now calculate the final breakdown exactly as the GUI does
        required_gross_monthly = required_gross_annual / 12
        
        # Calculate taxable income (gross minus pre-tax contributions)
        taxable_income_annual = required_gross_annual - (pre_tax_contributions * 12)
        
        # Calculate actual taxes and tithe for the required salary
        federal_tax_annual = self.calculate_progressive_federal_tax(taxable_income_annual, self.filing_status_var.get())
        state_rate = self.get_state_tax_rate(self.state_var.get(), taxable_income_annual)
        state_tax_annual = taxable_income_annual * state_rate
        fica_tax_annual = self.calculate_fica_tax(required_gross_annual)  # FICA is on gross, not taxable
        
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
        
        print(f"\nFINAL CALCULATION:")
        print(f"Required gross annual: ${required_gross_annual:.2f}")
        print(f"Required gross monthly: ${required_gross_monthly:.2f}")
        print(f"Net income annual: ${net_income_annual:.2f}")
        print(f"Net income monthly: ${net_income_annual/12:.2f}")
        print(f"Actual expenses annual: ${actual_expenses_annual:.2f}")
        print(f"Actual expenses monthly: ${actual_expenses_annual/12:.2f}")
        print(f"Leftover annual: ${leftover_annual:.2f}")
        print(f"Leftover monthly: ${leftover_annual/12:.2f}")
        
        print(f"\nANALYSIS:")
        if min_leftover == 0:
            print(f"Expected leftover: $0.00")
            print(f"Actual leftover: ${leftover_annual/12:.2f}")
            if abs(leftover_annual/12) < 1:
                print("✅ Calculation is correct!")
            else:
                print("❌ Calculation has an error!")
        else:
            print(f"Target minimum: ${min_leftover:.2f}")
            print(f"Actual leftover: ${leftover_annual/12:.2f}")
            print(f"Difference: ${leftover_annual/12 - min_leftover:.2f}")

def test_different_scenarios():
    """Test with different min_leftover values"""
    print("Testing different min_leftover scenarios")
    print("="*60)
    
    # Test with min_leftover = 0 (user entered)
    print("\n1. Testing with min_leftover = 0 (user entered)")
    calc = TestSalaryCalculator()
    calc.min_leftover_var.set("0")
    calc.min_leftover_entry = MockEntry("0", "white")  # White means user typed it
    calc.test_calculate_salary()
    
    # Test with empty min_leftover (should use placeholder)
    print("\n2. Testing with empty min_leftover (should use placeholder)")
    calc2 = TestSalaryCalculator()
    calc2.min_leftover_var.set("500")  # Placeholder value
    calc2.min_leftover_entry = MockEntry("500", "gray")  # Gray means it's placeholder
    calc2.test_calculate_salary()

if __name__ == "__main__":
    test_different_scenarios()