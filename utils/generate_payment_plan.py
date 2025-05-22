from typing import List, Dict
from datetime import datetime, timedelta
from models.loan import Loan

def generate_payment_plan(prioritized_loans: List[Loan], user_extra_cash: float) -> List[Dict]:
    """
    Generate a payment plan for the given prioritized loans using the Snowball method.

    Args:
        prioritized_loans (List[Loan]): Loans sorted by balance ascending.
        user_extra_cash (float): Extra cash available each month.

    Returns:
        List[Dict]: Each entry includes payment details, balances, and fixed totals.
    """
    # Clone loans and initialize state
    loans = [Loan(**loan.__dict__) for loan in prioritized_loans]
    for loan in loans:
        loan.adjusted_min_payment = loan.monthly_min_payment
        loan.total_paid = 0.0
        loan.last_payment_date = datetime.today().date()

    # Compute fixed budgets
    minimum_total_payment = sum(loan.monthly_min_payment for loan in loans)
    adjusted_total_payment = minimum_total_payment + user_extra_cash
    fixed_budget = adjusted_total_payment

    payment_plan = []
    payment_date = datetime.today().date()
    prev_total_balance = None
    max_iterations = 1000
    iteration = 0

    # Main loop
    while any(loan.current_balance > 0 for loan in loans):
        loans.sort(key=lambda l: l.current_balance)
        if iteration >= max_iterations:
            break

        period_payments: Dict[str, float] = {}
        freed = 0.0

        # 1) Pay minimums and collect freed amounts
        for loan in loans:
            if loan.current_balance <= 0:
                period_payments[loan.name] = 0.0
                continue

            # Accrue interest
            interest = loan.current_balance * (loan.interest_rate / 100 / 12)
            loan.current_balance += interest

            # Determine payment (cap at balance)
            min_pay = loan.adjusted_min_payment
            payment_amt = min(min_pay, loan.current_balance)
            principal = max(0.0, payment_amt - min(payment_amt, interest))

            # Apply payment
            loan.current_balance -= principal
            loan.total_paid += payment_amt
            loan.last_payment_date = payment_date
            period_payments[loan.name] = round(payment_amt, 2)

            # Freed from min_pay
            freed += (min_pay - payment_amt)
            if loan.current_balance <= 0:
                loan.adjusted_min_payment = 0.0

        # 2) Build extra pool and redistribute immediately
        extra_pool = user_extra_cash + freed
        for loan in loans:
            if loan.current_balance <= 0 or extra_pool <= 0:
                continue
            bonus = min(extra_pool, loan.current_balance)
            loan.current_balance -= bonus
            loan.total_paid += bonus
            period_payments[loan.name] = period_payments.get(loan.name, 0.0) + round(bonus, 2)
            extra_pool -= bonus

        # 2a) Ensure total_payment equals fixed_budget
        actual_total = sum(period_payments.values())
        if actual_total < fixed_budget:
            diff = fixed_budget - actual_total
            for loan in loans:
                if loan.current_balance <= 0 or diff <= 0:
                    continue
                bonus = min(diff, loan.current_balance)
                loan.current_balance -= bonus
                loan.total_paid += bonus
                period_payments[loan.name] = period_payments.get(loan.name, 0.0) + round(bonus, 2)
                diff -= bonus

        # 3) Summarize
        total_balance = sum(max(l.current_balance, 0) for l in loans)
        balances = {l.name: round(l.current_balance, 2) for l in loans}

        # Detect stagnation
        if prev_total_balance is not None and abs(total_balance - prev_total_balance) < 0.01:
            break
        prev_total_balance = total_balance

        # 4) Append period data
        payment_plan.append({
            "date": payment_date.strftime("%Y-%m-%d"),
            "payments": period_payments,
            "balances": balances,
            "total_payment": round(fixed_budget, 2),
            "total_balance": round(total_balance, 2),
            "minimum_total_payment": round(minimum_total_payment, 2),
            "adjusted_total_payment": round(adjusted_total_payment, 2),
        })

        # Advance to next month
        payment_date += timedelta(days=30)
        iteration += 1

    return payment_plan
