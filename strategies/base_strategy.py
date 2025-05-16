from abc import ABC, abstractmethod
from typing import List, Dict
from models import Loan

class PayoffStrategy(ABC):
    """
    Abstract base class for loan payoff strategies.
    All concrete strategies should inherit from this class and implement the generate_payment_plan method.
    """

    @abstractmethod
    def generate_payment_plan(self, loans: List[Loan]) -> List[Dict]:
        """
        Generate a payment plan based on the provided list of loans.

        Args:
            loans (List[Loan]): A list of Loan objects to include in the payment plan.

        Returns:
            List[Dict]: A list of dictionaries representing the payment plan.
                        Each dictionary should contain details such as:
                        - 'loan_id': Identifier of the loan
                        - 'payment_date': Date of the payment
                        - 'payment_amount': Total payment amount
                        - 'principal_paid': Amount applied to the principal
                        - 'interest_paid': Amount applied to the interest
                        - 'remaining_balance': Remaining balance after the payment
        """
        pass

if __name__ == "__main__":
    # Example usage
    class DummyStrategy(PayoffStrategy):
        def generate_payment_plan(self, loans: List[Loan]) -> List[Dict]:
            return [{"loan_id": loan.id, "payment_date": "2025-06-01", "payment_amount": 100.0,
                     "principal_paid": 80.0, "interest_paid": 20.0, "remaining_balance": loan.current_balance - 80.0}
                    for loan in loans]

    # Create a dummy loan for demonstration
    dummy_loan = Loan(
        id=1,
        name="Demo Loan",
        principal=1000.0,
        current_balance=1000.0,
        interest_rate=5.0,
        monthly_min_payment=50.0,
        extra_payment=0.0,
        first_due_date="2025-06-01"
    )

    strategy = DummyStrategy()
    plan = strategy.generate_payment_plan([dummy_loan])
    for payment in plan:
        print(payment)