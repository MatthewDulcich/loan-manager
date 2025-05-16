from typing import List, Dict
from datetime import datetime, timedelta
from models.loan import Loan
from strategies.base_strategy import PayoffStrategy

class CustomStrategy(PayoffStrategy):
    """
    Implements a customizable debt payoff strategy.
    Allows users to define their own loan repayment order.
    """

    def __init__(self, loan_priority: List[int]):
        """
        Initialize the custom strategy with a specific loan priority order.

        Args:
            loan_priority (List[int]): A list of loan IDs in the desired payoff order.
        """
        self.loan_priority = loan_priority

    def generate_payment_plan(self, loans: List[Loan]) -> List[Dict]:
        """
        Generate a payment plan based on the user-defined loan priority.

        Args:
            loans (List[Loan]): A list of Loan objects.

        Returns:
            List[Dict]: A list of payment records detailing the payment schedule.
        """
        # Create a mapping from loan ID to Loan object
        loan_map = {loan.id: loan for loan in loans}
        payment_plan = []
        payment_date = datetime.today().date()

        # Continue until all loans are paid off
        while any(loan.current_balance > 0 for loan in loans):
            # Apply payments based on user-defined priority
            for loan_id in self.loan_priority:
                loan = loan_map.get(loan_id)
                if loan and loan.current_balance > 0:
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
        name="Car Loan",
        principal=10000.0,
        current_balance=10000.0,
        interest_rate=5.0,
        monthly_min_payment=200.0,
        extra_payment=50.0,
        first_due_date="2025-06-01"
    )

    loan2 = Loan(
        id=2,
        name="Student Loan",
        principal=15000.0,
        current_balance=15000.0,
        interest_rate=4.5,
        monthly_min_payment=150.0,
        extra_payment=0.0,
        first_due_date="2025-06-01"
    )

    # Define custom priority: pay off Car Loan first, then Student Loan
    custom_priority = [1, 2]

    strategy = CustomStrategy(loan_priority=custom_priority)
    plan = strategy.generate_payment_plan([loan1, loan2])

    for payment in plan:
        print(payment)