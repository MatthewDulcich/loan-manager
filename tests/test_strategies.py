import unittest
from strategies.snowball import SnowballStrategy
from strategies.avalanche import AvalancheStrategy
from strategies.custom_strategy import CustomStrategy
from models.loan import Loan

class TestStrategies(unittest.TestCase):
    def setUp(self):
        # Create sample loans
        self.loans = [
            Loan(id=1, name="Loan A", principal=5000, current_balance=3000, interest_rate=5.0,
                 monthly_min_payment=100, extra_payment=0, first_due_date="2025-06-01"),
            Loan(id=2, name="Loan B", principal=8000, current_balance=8000, interest_rate=3.0,
                 monthly_min_payment=150, extra_payment=0, first_due_date="2025-06-01"),
            Loan(id=3, name="Loan C", principal=10000, current_balance=5000, interest_rate=7.0,
                 monthly_min_payment=200, extra_payment=0, first_due_date="2025-06-01"),
        ]

    def test_snowball_strategy(self):
        strategy = SnowballStrategy()
        prioritized_loans = strategy.prioritize(self.loans)
        balances = [loan.current_balance for loan in prioritized_loans]
        self.assertEqual(balances, sorted(balances),
                         "SnowballStrategy should prioritize loans with smallest balance first.")

        # Test payment plan structure
        plan = strategy.generate_payment_plan(self.loans)
        self.assertTrue(isinstance(plan, list))
        for period in plan:
            self.assertIn("date", period)
            self.assertIn("payments", period)
            self.assertIn("total_balance", period)
            self.assertTrue(isinstance(period["payments"], dict))
            for loan in self.loans:
                self.assertIn(loan.name, period["payments"])

    def test_avalanche_strategy(self):
        strategy = AvalancheStrategy()
        prioritized_loans = strategy.prioritize(self.loans)
        rates = [loan.interest_rate for loan in prioritized_loans]
        self.assertEqual(rates, sorted(rates, reverse=True),
                         "AvalancheStrategy should prioritize loans with highest interest rate first.")

        # Test payment plan structure
        plan = strategy.generate_payment_plan(self.loans)
        self.assertTrue(isinstance(plan, list))
        for period in plan:
            self.assertIn("date", period)
            self.assertIn("payments", period)
            self.assertIn("total_balance", period)
            self.assertTrue(isinstance(period["payments"], dict))
            for loan in self.loans:
                self.assertIn(loan.name, period["payments"])

    def test_custom_strategy(self):
        strategy = CustomStrategy()
        prioritized_loans = strategy.prioritize(self.loans)
        # Assuming CustomStrategy prioritizes by loan name alphabetically
        names = [loan.name for loan in prioritized_loans]
        self.assertEqual(names, sorted(names),
                         "CustomStrategy should prioritize loans by name alphabetically.")

        # Test payment plan structure
        plan = strategy.generate_payment_plan(self.loans)
        self.assertTrue(isinstance(plan, list))
        for period in plan:
            self.assertIn("date", period)
            self.assertIn("payments", period)
            self.assertIn("total_balance", period)
            self.assertTrue(isinstance(period["payments"], dict))
            for loan in self.loans:
                self.assertIn(loan.name, period["payments"])

if __name__ == '__main__':
    unittest.main()