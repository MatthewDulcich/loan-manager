from typing import List, Dict
from datetime import datetime, timedelta
from models.loan import Loan

def generate_payment_plan(prioritized_loans: List[Loan]) -> List[Dict]:
    """
    Generate a payment plan for the given prioritized loans.

    Args:
        prioritized_loans (List[Loan]): A list of Loan objects, already prioritized.

    Returns:
        List[Dict]: Each dict has keys: "date", "payments" (dict), "total_balance"
    """
    loans = [Loan(**loan.__dict__) for loan in prioritized_loans]
    payment_plan = []
    payment_date = datetime.today().date()

    # Initialize last payment dates if not set
    for loan in loans:
        if not hasattr(loan, "last_payment_date") or loan.last_payment_date is None:
            loan.last_payment_date = payment_date
        if not hasattr(loan, "total_paid"):
            loan.total_paid = 0

    max_iterations = 1000
    iteration = 0
    previous_total_balance = None

    while any(loan.current_balance > 0 for loan in loans):
        if iteration >= max_iterations:
            print("Reached maximum iterations. Exiting loop to prevent overflow.")
            break

        period_payments = {}
        total_extra_payment = sum(loan.extra_payment for loan in loans if loan.current_balance > 0)

        for loan in loans:
            if loan.current_balance <= 0:
                period_payments[loan.name] = 0
                continue

            # Calculate accrued interest
            accrued_interest = loan.current_balance * (loan.interest_rate / 100 / 12)
            loan.current_balance += accrued_interest

            # Determine payment amount
            payment_amount = loan.monthly_min_payment + loan.extra_payment
            interest_payment = min(payment_amount, accrued_interest)
            principal_payment = max(0.0, payment_amount - interest_payment)
            loan.current_balance = max(0.0, loan.current_balance - principal_payment)
            loan.total_paid += payment_amount
            loan.last_payment_date = payment_date

            period_payments[loan.name] = round(payment_amount, 2)

            # Redistribute extra payment if loan is paid off
            if loan.current_balance == 0:
                total_extra_payment += loan.monthly_min_payment + loan.extra_payment
                loan.extra_payment = 0

        # Redistribute extra payments to remaining loans
        remaining_loans = [loan for loan in loans if loan.current_balance > 0]
        if remaining_loans and total_extra_payment > 0:
            extra_per_loan = total_extra_payment / len(remaining_loans)
            for loan in remaining_loans:
                loan.extra_payment += extra_per_loan

        total_balance = sum(max(loan.current_balance, 0) for loan in loans)

        # Minimal balance change check
        if previous_total_balance is not None:
            balance_change = abs(total_balance - previous_total_balance)
            if balance_change < 0.01:
                print("Minimal balance change detected. Exiting loop to prevent overflow.")
                break

        previous_total_balance = total_balance

        payment_plan.append({
            "date": payment_date.strftime("%Y-%m-%d"),
            "payments": period_payments,
            "total_balance": round(total_balance, 2)
        })

        # Prevent infinite loop if all payments are zero (shouldn't happen, but just in case)
        if all(p == 0 for p in period_payments.values()):
            break

        payment_date += timedelta(days=30)
        iteration += 1

    return payment_plan