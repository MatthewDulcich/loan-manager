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
    loans.sort(key=lambda l: l.current_balance)
    payment_plan = []
    payment_date = datetime.today().date()

    # Initialize last payment dates and adjusted payments
    for loan in loans:
        loan.last_payment_date = payment_date
        loan.total_paid = 0
        loan.adjusted_min_payment = loan.monthly_min_payment

    max_iterations = 1000
    iteration = 0
    previous_total_balance = None

    user_extra_cash = sum(loan.extra_payment for loan in loans)

    while any(loan.current_balance > 0 for loan in loans):
        loans.sort(key=lambda l: l.current_balance)

        if iteration >= max_iterations:
            print("Reached maximum iterations. Exiting loop to prevent overflow.")
            break

        period_payments = {}
        total_extra_payment = user_extra_cash
        current_cycle_freed = 0.0

        # Pay minimums
        for loan in loans:
            if loan.current_balance <= 0:
                period_payments[loan.name] = 0.0
                continue

            # Interest
            accrued_interest = loan.current_balance * (loan.interest_rate / 100 / 12)
            loan.current_balance += accrued_interest

            # Minimum payment
            interest_payment = min(loan.adjusted_min_payment, accrued_interest)
            principal_payment = max(0.0, loan.adjusted_min_payment - interest_payment)
            loan.current_balance = max(0.0, loan.current_balance - principal_payment)
            loan.total_paid += loan.adjusted_min_payment
            loan.last_payment_date = payment_date

            period_payments[loan.name] = round(loan.adjusted_min_payment, 2)

            # If loan is paid off, defer its min payment for next month and store freed permanently
            if loan.current_balance == 0:
                current_cycle_freed += loan.adjusted_min_payment
                loan.adjusted_min_payment = 0.0

        # Redirect freed payments once to next loan
        if current_cycle_freed > 0:
            # Re-sort to find next nonzero balance loan
            loans.sort(key=lambda l: l.current_balance)
            for loan in loans:
                if loan.current_balance > 0:
                    loan.adjusted_min_payment += current_cycle_freed
                    break

        # Redistribute total extra payment to remaining loans
        for loan in loans:
            if loan.current_balance > 0 and total_extra_payment > 0:
                extra_payment = min(total_extra_payment, loan.current_balance)
                loan.current_balance -= extra_payment
                loan.total_paid += extra_payment
                period_payments[loan.name] += round(extra_payment, 2)
                total_extra_payment -= extra_payment
            if total_extra_payment <= 0:
                break

        total_balance = sum(max(loan.current_balance, 0) for loan in loans)

        # Detect stagnation
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

        if all(p == 0 for p in period_payments.values()):
            break

        payment_date += timedelta(days=30)
        iteration += 1

    return payment_plan