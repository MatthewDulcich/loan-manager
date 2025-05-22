from typing import List, Dict
from models.loan import Loan
from strategies.base_strategy import PayoffStrategy
from utils import generate_payment_plan  # Import the shared function

class SnowballStrategy(PayoffStrategy):
    """
    Implements the Snowball debt payoff strategy.
    Prioritizes paying off loans with the smallest balances first.
    """

    def prioritize(self, loans):
        # Sort by current_balance ascending (smallest first)
        return sorted(loans, key=lambda loan: loan.current_balance)

    def generate_payment_plan(self, loans: List[Loan]) -> List[Dict]:
        """
        Generate a payment plan using the Snowball strategy.

        Args:
            loans (List[Loan]): A list of Loan objects.

        Returns:
            List[Dict]: Each dict has keys: "date", "payments" (dict), "total_balance"
        """
        prioritized_loans = self.prioritize(loans)  # Prioritize loans by smallest balance
        return generate_payment_plan(prioritized_loans, user_extra_cash=0)  # Use the shared function

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