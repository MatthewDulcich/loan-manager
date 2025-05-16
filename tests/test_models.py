import unittest
from datetime import date
from models.loan import Loan

class TestLoanModel(unittest.TestCase):
    def setUp(self):
        self.loan = Loan(
            id=1,
            name="Test Loan",
            principal=10000.0,
            current_balance=10000.0,
            interest_rate=5.0,
            monthly_min_payment=200.0,
            extra_payment=0.0,
            first_due_date="2025-06-01"
        )

    def test_initialization(self):
        self.assertEqual(self.loan.name, "Test Loan")
        self.assertEqual(self.loan.principal, 10000.0)
        self.assertEqual(self.loan.current_balance, 10000.0)
        self.assertEqual(self.loan.interest_rate, 5.0)
        self.assertEqual(self.loan.monthly_min_payment, 200.0)
        self.assertEqual(self.loan.extra_payment, 0.0)
        self.assertEqual(self.loan.first_due_date, date(2025, 6, 1))

    def test_accrued_interest(self):
        self.loan.last_payment_date = date(2025, 6, 1)
        accrued = self.loan.calculate_accrued_interest(
            from_date=date(2025, 6, 1),
            to_date=date(2025, 7, 1)
        )
        expected_interest = round(10000.0 * (0.05 / 365) * 30, 2)
        self.assertAlmostEqual(accrued, expected_interest, places=2)

    def test_apply_payment(self):
        self.loan.last_payment_date = date(2025, 6, 1)
        result = self.loan.apply_payment(300.0, payment_date="2025-07-01")
        self.assertIn("interest_paid", result)
        self.assertIn("principal_paid", result)
        self.assertIn("remaining_balance", result)
        self.assertEqual(self.loan.total_paid, 300.0)

    def test_amortization_schedule(self):
        schedule = self.loan.generate_amortization_schedule()
        self.assertIsInstance(schedule, list)
        self.assertGreater(len(schedule), 0)
        for entry in schedule[:5]:
            self.assertIn("date", entry)
            self.assertIn("payment", entry)
            self.assertIn("principal", entry)
            self.assertIn("interest", entry)
            self.assertIn("balance", entry)

if __name__ == "__main__":
    unittest.main()