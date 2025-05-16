from typing import List, Dict
from datetime import datetime, timedelta
from models.loan import Loan
from strategies.base_strategy import PayoffStrategy

class SnowballStrategy(PayoffStrategy):
    """
    Implements the Snowball debt payoff strategy.
    Prioritizes paying off loans with the smallest balances first.
    """

    def generate_payment_plan(self, loans: List[Loan]) -> List[Dict]:
        """
        Generate a payment plan using the Snowball strategy.

        Args:
            loans (List[Loan]): A list of Loan objects.

        Returns:
            List[Dict]: A list of payment records detailing the payment schedule.
        """
        # Clone and sort the loans by current balance in ascending order
        loans = sorted(loans, key=lambda loan: loan.current_balance)
        payment_plan = []
        payment_date = datetime.today().date()

        # Continue until all loans are paid off
        while any(loan.current_balance > 0 for loan in loans):
            # Calculate total available payment for this cycle
            total_payment = sum(loan.monthly_min_payment + loan.extra_payment for loan in loans if loan.current_balance > 0)

            # Apply payments to loans
            for loan in loans:
                if loan.current_balance <= 0:
                    continue

                # Calculate accrued interest
                accrued_interest = loan.calculate_accrued_interest(loan.last_payment_date, payment_date)
                loan.current_balance += accrued_interest

                # Determine payment amount
                payment_amount = loan.monthly_min_payment + loan.extra_payment
                interest_payment = min(payment_amount, accrued_interest)
                principal_payment = max(0.0, payment_amount - interest_payment)
                loan.current_balance = max(0.0, loan.current_balance - principal_payment)
                loan.total_paid += payment_amount
                loan.last_payment_date = payment_date

                # Record the payment
                payment_record = {
                    "loan_id": loan.id,
                    "payment_date": payment_date.isoformat(),
                    "payment_amount": round(payment_amount, 2),
                    "principal_paid": round(principal_payment, 2),
                    "interest_paid": round(interest_payment, 2),
                    "remaining_balance": round(loan.current_balance, 2)
                }
                payment_plan.append(payment_record)

            # Advance to next payment date (approximate next month)
            payment_date += timedelta(days=30)

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