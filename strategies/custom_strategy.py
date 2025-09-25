from typing import List, Dict
from models.loan import Loan
from strategies.base_strategy import PayoffStrategy
from utils import generate_payment_plan  # Import the shared function

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

    def generate_payment_plan(self, loans: List[Loan], extra_cash: float = 0.0) -> List[Dict]:
        """
        Generate a payment plan using the custom strategy.

        Args:
            loans (List[Loan]): A list of Loan objects.
            extra_cash (float): Additional monthly cash available for loan payments.

        Returns:
            List[Dict]: Each dict has keys: "date", "payments" (dict), "total_balance"
        """
        prioritized_loans = self.prioritize(loans)  # Prioritize loans by custom criteria
        return generate_payment_plan(prioritized_loans, user_extra_cash=extra_cash)  # Use the shared function

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