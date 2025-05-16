from typing import List, Dict
from datetime import datetime, timedelta
from models.loan import Loan
from strategies.base_strategy import PayoffStrategy

class SnowballStrategy(PayoffStrategy):
    """
    Implements the Snowball debt payoff strategy.
    Prioritizes paying off loans with the smallest balances first.
    """

    def prioritize(self, loans):
        # Sort by current_balance ascending (smallest first)
        return sorted(loans, key=lambda loan: loan.current_balance)

    def generate_payment_plan(self, loans: List[Loan]) -> List[Dict]:
        loans = [Loan(**loan.__dict__) for loan in self.prioritize(loans)]
        payment_plan = []
        payment_date = min(
            loan.first_due_date if hasattr(loan, "first_due_date") else datetime.today().date()
            for loan in loans
        )
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
            for loan in loans:
                if loan.current_balance <= 0:
                    period_payments[loan.name] = 0
                    continue

                accrued_interest = 0
                if hasattr(loan, "calculate_accrued_interest"):
                    try:
                        accrued_interest = loan.calculate_accrued_interest(loan.last_payment_date, payment_date)
                    except Exception:
                        accrued_interest = loan.current_balance * (loan.interest_rate / 100 / 12)
                else:
                    accrued_interest = loan.current_balance * (loan.interest_rate / 100 / 12)

                loan.current_balance += accrued_interest

                payment_amount = loan.monthly_min_payment + loan.extra_payment
                interest_payment = min(payment_amount, accrued_interest)
                principal_payment = max(0.0, payment_amount - interest_payment)
                loan.current_balance = max(0.0, loan.current_balance - principal_payment)
                loan.total_paid += payment_amount
                loan.last_payment_date = payment_date

                period_payments[loan.name] = round(payment_amount, 2)

            total_balance = sum(max(loan.current_balance, 0) for loan in loans)

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

            payment_date += timedelta(days=30)
            iteration += 1

        return payment_plan

if __name__ == "__main__":
    # Example usage
    loan1 = Loan(
        id=1,
        name="Medical Bill",
        principal=500.0,
        current_balance=500.0,
        interest_rate=0.0,
        monthly_min_payment=50.0,
        extra_payment=0.0,
        first_due_date="2025-06-01"
    )

    loan2 = Loan(
        id=2,
        name="Credit Card",
        principal=3000.0,
        current_balance=3000.0,
        interest_rate=15.0,
        monthly_min_payment=100.0,
        extra_payment=50.0,
        first_due_date="2025-06-01"
    )

    strategy = SnowballStrategy()
    plan = strategy.generate_payment_plan([loan1, loan2])

    for payment in plan:
        print(payment)