#!/usr/bin/env python3
"""
Debug script to analyze salary calculation logic
"""

def get_federal_tax_brackets_2025(filing_status="Single"):
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
        ]
    }
    return brackets.get(filing_status, brackets["Single"])

def calculate_progressive_federal_tax(income, filing_status="Single"):
    """Calculate federal tax using progressive brackets"""
    brackets = get_federal_tax_brackets_2025(filing_status)
    total_tax = 0
    prev_bracket = 0
    
    print(f"\nCalculating federal tax on income: ${income:,.2f}")
    
    for bracket_limit, rate in brackets:
        if income <= prev_bracket:
            break
        
        taxable_in_bracket = min(income, bracket_limit) - prev_bracket
        tax_in_bracket = taxable_in_bracket * rate
        total_tax += tax_in_bracket
        
        print(f"  Bracket ${prev_bracket:,.0f} - ${bracket_limit:,.0f} at {rate*100:.1f}%: ${taxable_in_bracket:,.2f} * {rate:.3f} = ${tax_in_bracket:,.2f}")
        
        prev_bracket = bracket_limit
        
        if income <= bracket_limit:
            break
    
    print(f"  Total Federal Tax: ${total_tax:,.2f}")
    return total_tax

def calculate_fica_tax(income):
    """Calculate FICA taxes (Social Security + Medicare)"""
    # Social Security: 6.2% up to $168,600 (2025 limit)
    # Medicare: 1.45% on all income
    # Additional Medicare: 0.9% on income over $200,000 (single)
    
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
    
    print(f"\nFICA Tax Calculation:")
    print(f"  Social Security: ${min(income, ss_wage_base):,.2f} * {ss_rate:.3f} = ${ss_tax:,.2f}")
    print(f"  Medicare: ${income:,.2f} * {medicare_rate:.4f} = ${medicare_tax:,.2f}")
    if additional_medicare_tax > 0:
        print(f"  Additional Medicare: ${income - additional_medicare_threshold:,.2f} * {additional_medicare_rate:.3f} = ${additional_medicare_tax:,.2f}")
    
    total_fica = ss_tax + medicare_tax + additional_medicare_tax
    print(f"  Total FICA: ${total_fica:,.2f}")
    return total_fica

def get_state_tax_rate(state):
    """Get state tax rate - simplified version for Maryland"""
    state_rates = {
        "Maryland": 0.0575,
        "California": 0.093,
        "Texas": 0.0,
        "Florida": 0.0
    }
    return state_rates.get(state, 0.0)

def test_calculation():
    """Test the salary calculation with sample values"""
    print("=" * 80)
    print("SALARY CALCULATION DEBUG TEST")
    print("=" * 80)
    
    # Sample input values (using placeholder defaults)
    expenses = {
        "rent": 1800,
        "car": 450,
        "insurance": 350,
        "food": 600,
        "utilities": 200,
        "phone": 150,
        "other_expenses": 300,
        "loan_payments": 0,  # Assume no loans for simplicity
        "extra_loan": 200,
        "savings": 500,
        "entertainment": 400,
        "min_leftover": 500  # This is what we want left over
    }
    
    # Retirement contributions
    retirement = {
        "contribution_401k": 800,  # Pre-tax
        "traditional_ira": 0,      # Pre-tax
        "roth_ira": 500,           # After-tax
        "hsa": 300,                # Pre-tax
        "education_529": 0,        # After-tax
        "other_investments": 200   # After-tax
    }
    
    # Tax settings
    tax_settings = {
        "filing_status": "Single",
        "state": "Maryland",
        "tithe_enabled": True,
        "tithe_rate": 0.10,
        "tithe_basis": "Gross Income"
    }
    
    print(f"MONTHLY EXPENSES:")
    total_basic_expenses = 0
    for key, value in expenses.items():
        if key != "min_leftover":
            print(f"  {key.replace('_', ' ').title()}: ${value:,.2f}")
            total_basic_expenses += value
    
    print(f"  Minimum Leftover Desired: ${expenses['min_leftover']:,.2f}")
    print(f"  Total Basic Monthly Expenses: ${total_basic_expenses:,.2f}")
    print(f"  Total Desired Monthly Amount: ${total_basic_expenses + expenses['min_leftover']:,.2f}")
    
    print(f"\nRETIREMENT CONTRIBUTIONS:")
    pre_tax_monthly = retirement["contribution_401k"] + retirement["traditional_ira"] + retirement["hsa"]
    after_tax_monthly = retirement["roth_ira"] + retirement["education_529"] + retirement["other_investments"]
    
    print(f"  Pre-tax monthly: ${pre_tax_monthly:,.2f}")
    print(f"  After-tax monthly: ${after_tax_monthly:,.2f}")
    
    # Calculate required annual amounts
    annual_basic_expenses = total_basic_expenses * 12
    annual_min_leftover = expenses['min_leftover'] * 12
    annual_after_tax_retirement = after_tax_monthly * 12
    annual_pre_tax_retirement = pre_tax_monthly * 12
    
    # Total after-tax needs (includes basic expenses + desired leftover + after-tax retirement)
    total_after_tax_needs = annual_basic_expenses + annual_min_leftover + annual_after_tax_retirement
    
    print(f"\nANNUAL REQUIREMENTS:")
    print(f"  Basic expenses (annual): ${annual_basic_expenses:,.2f}")
    print(f"  Minimum leftover (annual): ${annual_min_leftover:,.2f}")
    print(f"  After-tax retirement (annual): ${annual_after_tax_retirement:,.2f}")
    print(f"  Pre-tax retirement (annual): ${annual_pre_tax_retirement:,.2f}")
    print(f"  Total after-tax needs: ${total_after_tax_needs:,.2f}")
    
    # Now iterate to find required gross salary
    print(f"\nITERATIVE SALARY CALCULATION:")
    estimated_salary = total_after_tax_needs * 1.6  # Start with higher estimate
    
    for iteration in range(15):
        print(f"\n--- Iteration {iteration + 1} ---")
        print(f"Testing gross salary: ${estimated_salary:,.2f}")
        
        # Calculate taxable income (gross minus pre-tax contributions)
        taxable_income = estimated_salary - annual_pre_tax_retirement
        print(f"Taxable income: ${estimated_salary:,.2f} - ${annual_pre_tax_retirement:,.2f} = ${taxable_income:,.2f}")
        
        # Calculate taxes
        federal_tax = calculate_progressive_federal_tax(taxable_income, tax_settings["filing_status"])
        state_rate = get_state_tax_rate(tax_settings["state"])
        state_tax = taxable_income * state_rate
        print(f"State tax ({tax_settings['state']}): ${taxable_income:,.2f} * {state_rate:.4f} = ${state_tax:,.2f}")
        
        fica_tax = calculate_fica_tax(estimated_salary)  # FICA on gross income
        
        total_taxes = federal_tax + state_tax + fica_tax
        print(f"Total taxes: ${total_taxes:,.2f}")
        
        # Calculate tithe
        tithe = 0
        if tax_settings["tithe_enabled"]:
            if tax_settings["tithe_basis"] == "Gross Income":
                tithe = estimated_salary * tax_settings["tithe_rate"]
                print(f"Tithe on gross: ${estimated_salary:,.2f} * {tax_settings['tithe_rate']:.2f} = ${tithe:,.2f}")
            else:  # Net Income
                net_before_tithe = estimated_salary - total_taxes - annual_pre_tax_retirement
                tithe = net_before_tithe * tax_settings["tithe_rate"]
                print(f"Tithe on net: ${net_before_tithe:,.2f} * {tax_settings['tithe_rate']:.2f} = ${tithe:,.2f}")
        
        # Calculate final net income after all deductions
        net_income = estimated_salary - total_taxes - tithe - annual_pre_tax_retirement
        print(f"Net income: ${estimated_salary:,.2f} - ${total_taxes:,.2f} - ${tithe:,.2f} - ${annual_pre_tax_retirement:,.2f} = ${net_income:,.2f}")
        
        # Compare to needs
        print(f"After-tax needs: ${total_after_tax_needs:,.2f}")
        print(f"Net income available: ${net_income:,.2f}")
        print(f"Difference: ${net_income - total_after_tax_needs:,.2f}")
        
        # Check convergence
        if abs(net_income - total_after_tax_needs) < 100:
            print(f"\n✅ CONVERGED! Required gross salary: ${estimated_salary:,.2f}")
            break
        
        # Adjust estimate
        if net_income < total_after_tax_needs:
            print("Net income too low, increasing estimate...")
            estimated_salary *= 1.05
        else:
            print("Net income too high, decreasing estimate...")
            estimated_salary *= 0.98
    
    # Final breakdown
    print(f"\n" + "="*80)
    print("FINAL RESULTS:")
    print("="*80)
    print(f"Required Annual Gross Salary: ${estimated_salary:,.2f}")
    print(f"Required Monthly Gross Salary: ${estimated_salary/12:,.2f}")
    print(f"Required Hourly Wage: ${estimated_salary/(52*40):,.2f}")
    
    # Verify the calculation
    print(f"\nVERIFICATION:")
    taxable_income_final = estimated_salary - annual_pre_tax_retirement
    federal_tax_final = calculate_progressive_federal_tax(taxable_income_final, "Single")
    state_tax_final = taxable_income_final * get_state_tax_rate("Maryland")
    fica_tax_final = calculate_fica_tax(estimated_salary)
    total_taxes_final = federal_tax_final + state_tax_final + fica_tax_final
    tithe_final = estimated_salary * 0.10 if tax_settings["tithe_enabled"] else 0
    net_income_final = estimated_salary - total_taxes_final - tithe_final - annual_pre_tax_retirement
    
    # Now calculate what we actually have left after ACTUAL expenses (not including min_leftover target)
    actual_annual_expenses = annual_basic_expenses + annual_after_tax_retirement
    actual_leftover = net_income_final - actual_annual_expenses
    
    print(f"Final net income: ${net_income_final:,.2f}")
    print(f"Actual annual expenses: ${actual_annual_expenses:,.2f}")
    print(f"Money actually left over: ${actual_leftover:,.2f}")
    print(f"Monthly leftover: ${actual_leftover/12:,.2f}")
    print(f"Target minimum leftover: ${expenses['min_leftover']:,.2f}")
    
    if abs(actual_leftover/12 - expenses['min_leftover']) < 10:
        print("✅ Calculation is CORRECT!")
    else:
        print("❌ Calculation has an ERROR!")
        print(f"Expected leftover: ${expenses['min_leftover']:,.2f}")
        print(f"Actual leftover: ${actual_leftover/12:,.2f}")
        print(f"Difference: ${actual_leftover/12 - expenses['min_leftover']:,.2f}")

if __name__ == "__main__":
    test_calculation()