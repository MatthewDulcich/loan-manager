from typing import List, Dict
from datetime import datetime, timedelta
from models.loan import Loan
from strategies.base_strategy import PayoffStrategy

class CustomStrategy(PayoffStrategy):
    """
    Implements a customizable debt payoff strategy.
    Allows users to define their own loan repayment order.
    """

    def __init__(self, loan_priority=None):
        """
        Initialize the custom strategy with a specific loan priority order.

        Args:
            loan_priority (List[int]): A list of loan IDs in the desired payoff order.
        """
        self.loan_priority = loan_priority

    def prioritize(self, loans):
        """
        Prioritize loans based on a custom sorting logic.

        Args:
            loans (List[Loan]): A list of Loan objects.

        Returns:
            List[Loan]: A sorted list of Loan objects.
        """
        # Example: sort by name alphabetically if no priority is set
        if not self.loan_priority:
            return sorted(loans, key=lambda loan: loan.name)
        # Otherwise, sort by user-defined priority
        loan_map = {loan.id: loan for loan in loans}
        return [loan_map[loan_id] for loan_id in self.loan_priority if loan_id in loan_map]

    def generate_payment_plan(self, loans: List[Loan]) -> List[Dict]:
        """
        Generate a payment plan based on the user-defined loan priority.

        Args:
            loans (List[Loan]): A list of Loan objects.

        Returns:
            List[Dict]: Each dict has keys: "date", "payments" (dict), "total_balance"
        """
        # Clone the loans to avoid mutating the original list
        loans = [Loan(**loan.__dict__) for loan in self.prioritize(loans)]
        loan_map = {loan.id: loan for loan in loans}
        payment_plan = []
        payment_date = datetime.today().date()

        # Initialize last payment dates if not set
        for loan in loans:
            if not hasattr(loan, "last_payment_date") or loan.last_payment_date is None:
                loan.last_payment_date = payment_date
            if not hasattr(loan, "total_paid"):
                loan.total_paid = 0

        while any(loan.current_balance > 0 for loan in loans):
            period_payments = {}
            for loan_id in self.loan_priority or [loan.id for loan in loans]:
                loan = loan_map.get(loan_id)
                if loan and loan.current_balance > 0:
                    # Calculate accrued interest
                    accrued_interest = 0
                    if hasattr(loan, "calculate_accrued_interest"):
                        try:
                            accrued_interest = loan.calculate_accrued_interest(loan.last_payment_date, payment_date)
                        except Exception:
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
                elif loan:
                    period_payments[loan.name] = 0

            total_balance = sum(max(loan.current_balance, 0) for loan in loans)
            payment_plan.append({
                "date": payment_date.strftime("%Y-%m-%d"),
                "payments": period_payments,
                "total_balance": round(total_balance, 2)
            })

            # Advance to next payment date (approximate next month)
            payment_date += timedelta(days=30)

            # Prevent infinite loop if all payments are zero (shouldn't happen, but just in case)
            if all(p == 0 for p in period_payments.values()):
                break

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