from typing import List, Dict
from models.loan import Loan
from strategies.base_strategy import PayoffStrategy
from utils import generate_payment_plan  # Import the shared function

class AvalancheStrategy(PayoffStrategy):
    """
    Implements the Avalanche debt payoff strategy.
    Prioritizes paying off loans with the highest interest rates first.
    """

    def prioritize(self, loans):
        # Sort by interest_rate descending (highest first)
        return sorted(loans, key=lambda loan: loan.interest_rate, reverse=True)

    def generate_payment_plan(self, loans: List[Loan]) -> List[Dict]:
        """
        Generate a payment plan using the Avalanche strategy.

        Args:
            loans (List[Loan]): A list of Loan objects.

        Returns:
            List[Dict]: Each dict has keys: "date", "payments" (dict), "total_balance"
        """
        prioritized_loans = self.prioritize(loans)  # Prioritize loans by interest rate
        return generate_payment_plan(prioritized_loans)  # Use the shared function

if __name__ == "__main__":
    # Example usage
    loan1 = Loan(
        id=1,
        name="Credit Card",
        principal=5000.0,
        current_balance=5000.0,
        interest_rate=19.99,
        monthly_min_payment=150.0,
        extra_payment=50.0,
        first_due_date="2025-06-01"
    )

    loan2 = Loan(
        id=2,
        name="Personal Loan",
        principal=3000.0,
        current_balance=3000.0,
        interest_rate=10.5,
        monthly_min_payment=100.0,
        extra_payment=0.0,
        first_due_date="2025-06-01"
    )

    strategy = AvalancheStrategy()
    plan = strategy.generate_payment_plan([loan1, loan2])

    for payment in plan:
        print(payment)