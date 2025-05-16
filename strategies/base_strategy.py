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
                        Each dictionary should contain:
                        - 'date': Date of the payment period (str)
                        - 'payments': Dict mapping loan names to payment amounts for this period
                        - 'total_balance': Total remaining balance across all loans after this period
        """
        pass

if __name__ == "__main__":
    # Example usage
    class DummyStrategy(PayoffStrategy):
        def generate_payment_plan(self, loans: List[Loan]) -> List[Dict]:
            plan = []
            for i in range(3):
                payments = {loan.name: 100.0 for loan in loans}
                total_balance = sum(loan.current_balance - 100.0 * (i + 1) for loan in loans)
                plan.append({
                    "date": f"2025-0{i+6}-01",
                    "payments": payments,
                    "total_balance": total_balance
                })
            return plan

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