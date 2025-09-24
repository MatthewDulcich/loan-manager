#!/usr/bin/env python3
"""
Test the save functionality directly to identify the issue
"""

import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import traceback

# Mock the calculation results for testing
def test_save_functionality():
    """Test save functionality with mock data"""
    print("Testing save functionality...")
    
    # Mock calculation results - same structure as the actual results
    mock_results = {
        'gross_annual': 144590.43,
        'gross_monthly': 12049.20,
        'hourly_wage': 69.57,
        'taxable_income_annual': 131390.43,
        'pre_tax_contributions': 1100.0,
        'after_tax_contributions': 700.0,
        'total_taxes': 3602.83,
        'tithe': 1204.92,
        'net_income': 6144.92,
        'total_expenses': 5650.0,
        'leftover': 494.92,
        'min_leftover_requested': 500.0,
        'tax_breakdown': {
            'federal': 2051.11,
            'state': 755.49,
            'fica': 796.23
        },
        'tithe_enabled': True,
        'tax_method': "Progressive",
        'calculation_inputs': {
            'rent': 1800.0,
            'car': 450.0,
            'insurance': 350.0,
            'food': 600.0,
            'utilities': 200.0,
            'phone': 150.0,
            'other_expenses': 300.0,
            'loan_payments': 0.0,
            'extra_loan': 200.0,
            'savings': 500.0,
            'entertainment': 400.0,
            'min_leftover': 500.0,
            'contribution_401k': 800.0,
            'traditional_ira': 0.0,
            'roth_ira': 500.0,
            'hsa': 300.0,
            'education_529': 0.0,
            'other_investments': 200.0,
            'filing_status': "Single",
            'state': "Maryland",
            'federal_tax_rate': None,
            'state_tax_rate': None,
            'fica_rate': 7.65,
            'tithe_rate': 10.0,
            'tithe_basis': "Gross Income"
        }
    }
    
    print("Mock results created successfully")
    
    # Test save_as_text function
    try:
        print("Testing save_as_text function...")
        test_file_path = "/tmp/test_salary_calculation.txt"
        save_as_text_test(mock_results, test_file_path)
        print(f"✅ Text save successful! File created at {test_file_path}")
        
        # Check if file exists and has content
        with open(test_file_path, 'r') as f:
            content = f.read()
            print(f"File size: {len(content)} characters")
            if len(content) > 100:
                print("✅ File has substantial content")
            else:
                print("❌ File seems too small")
                print("Content preview:", content[:200])
        
    except Exception as e:
        print(f"❌ Text save failed: {str(e)}")
        print("Full traceback:")
        traceback.print_exc()
    
    # Test save_as_csv function
    try:
        print("\nTesting save_as_csv function...")
        test_csv_path = "/tmp/test_salary_calculation.csv"
        save_as_csv_test(mock_results, test_csv_path)
        print(f"✅ CSV save successful! File created at {test_csv_path}")
        
        # Check if file exists and has content
        with open(test_csv_path, 'r') as f:
            content = f.read()
            print(f"File size: {len(content)} characters")
            if len(content) > 100:
                print("✅ File has substantial content")
            else:
                print("❌ File seems too small")
                print("Content preview:", content[:200])
        
    except Exception as e:
        print(f"❌ CSV save failed: {str(e)}")
        print("Full traceback:")
        traceback.print_exc()

def save_as_text_test(results, file_path):
    """Test version of save_as_text"""
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
        
        # Tax Information
        f.write("TAX CALCULATION DETAILS\n")
        f.write("-" * 30 + "\n")
        f.write(f"Method: {results['tax_method']} Tax Calculation\n")
        
        if results['tax_method'] == "Progressive":
            f.write(f"Filing Status: {inputs['filing_status']}\n")
            f.write(f"State: {inputs['state']}\n")
        else:
            if inputs['federal_tax_rate'] is not None:
                f.write(f"Federal Tax Rate: {inputs['federal_tax_rate']:.2f}%\n")
            if inputs['state_tax_rate'] is not None:
                f.write(f"State Tax Rate: {inputs['state_tax_rate']:.2f}%\n")
        
        f.write(f"FICA Tax Rate: {inputs['fica_rate']:.2f}%\n")
        
        if results['tithe_enabled']:
            f.write(f"Tithe Rate: {inputs['tithe_rate']:.2f}%\n")
            f.write(f"Tithe Calculated On: {inputs['tithe_basis']}\n")
        
        f.write("\n" + "=" * 60 + "\n")
        f.write("Note: Results are estimates. Consult a tax professional for precise calculations.\n")

def save_as_csv_test(results, file_path):
    """Test version of save_as_csv"""
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
        
        # Settings
        f.write("Calculation Settings\n")
        f.write("Setting,Value\n")
        f.write(f"Tax Method,{results['tax_method']}\n")
        
        if results['tax_method'] == "Progressive":
            f.write(f"Filing Status,{inputs['filing_status']}\n")
            f.write(f"State,{inputs['state']}\n")
        else:
            if inputs['federal_tax_rate'] is not None:
                f.write(f"Federal Tax Rate,{inputs['federal_tax_rate']:.2f}%\n")
            if inputs['state_tax_rate'] is not None:
                f.write(f"State Tax Rate,{inputs['state_tax_rate']:.2f}%\n")
        
        f.write(f"FICA Tax Rate,{inputs['fica_rate']:.2f}%\n")
        
        if results['tithe_enabled']:
            f.write(f"Tithe Enabled,Yes\n")
            f.write(f"Tithe Rate,{inputs['tithe_rate']:.2f}%\n")
            f.write(f"Tithe Basis,{inputs['tithe_basis']}\n")
        else:
            f.write(f"Tithe Enabled,No\n")

if __name__ == "__main__":
    test_save_functionality()