#!/usr/bin/env python3
"""
Quick test to reproduce the user's issue with min leftover = 0
"""

# Simulate the problematic calculation logic from the GUI
def test_min_leftover_zero_issue():
    """Test what happens when min_leftover = 0"""
    
    # Sample values
    basic_monthly_expenses = 4950  # rent + car + insurance + food + utilities + phone + other + loans + savings + entertainment
    after_tax_retirement = 700    # roth IRA + 529 + other investments
    min_leftover = 0  # User sets this to 0
    
    # This is what the GUI currently does (WRONG):
    # It includes min_leftover in the target expense calculation
    total_monthly_expenses_with_target = basic_monthly_expenses + min_leftover + after_tax_retirement
    print(f"Basic monthly expenses: ${basic_monthly_expenses:,.2f}")
    print(f"After-tax retirement: ${after_tax_retirement:,.2f}")
    print(f"Min leftover target: ${min_leftover:,.2f}")
    print(f"Total expenses used in salary calculation: ${total_monthly_expenses_with_target:,.2f}")
    
    # The algorithm finds a salary to provide this much net income
    required_net_monthly = total_monthly_expenses_with_target  # This will be $5,650
    print(f"Required net income: ${required_net_monthly:,.2f}")
    
    # But then for display, it calculates leftover as:
    # leftover = net_income - (basic_expenses + after_tax_retirement)
    actual_expenses_for_leftover = basic_monthly_expenses + after_tax_retirement  # This is $5,650
    calculated_leftover = required_net_monthly - actual_expenses_for_leftover
    
    print(f"\nFinal calculation:")
    print(f"Net income provided: ${required_net_monthly:,.2f}")
    print(f"Actual expenses (for leftover calc): ${actual_expenses_for_leftover:,.2f}")
    print(f"Calculated leftover: ${calculated_leftover:,.2f}")
    
    if min_leftover == 0:
        print(f"\n🔍 Analysis:")
        print(f"Expected leftover when min_leftover=0: $0.00")
        print(f"Actual calculated leftover: ${calculated_leftover:,.2f}")
        if calculated_leftover == 0:
            print("✅ Correct!")
        else:
            print("❌ This should be 0 but isn't!")

    # Test with non-zero min_leftover to see if logic works
    print("\n" + "="*50)
    print("Testing with min_leftover = $500:")
    min_leftover = 500
    total_monthly_expenses_with_target = basic_monthly_expenses + min_leftover + after_tax_retirement
    required_net_monthly = total_monthly_expenses_with_target
    actual_expenses_for_leftover = basic_monthly_expenses + after_tax_retirement
    calculated_leftover = required_net_monthly - actual_expenses_for_leftover
    
    print(f"Target min leftover: ${min_leftover:,.2f}")
    print(f"Calculated leftover: ${calculated_leftover:,.2f}")
    print(f"Difference: ${calculated_leftover - min_leftover:,.2f}")

if __name__ == "__main__":
    test_min_leftover_zero_issue()