import unittest
import sqlite3
from database import Database
from models import Loan

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Initialize an in-memory SQLite database
        self.db = Database(":memory:")
        self.db.connect()
        # Create necessary tables for testing
        self.db.execute("""
            CREATE TABLE loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                principal REAL NOT NULL,
                current_balance REAL NOT NULL,
                interest_rate REAL NOT NULL,
                monthly_min_payment REAL NOT NULL,
                extra_payment REAL DEFAULT 0,
                first_due_date TEXT NOT NULL,
                interest_change_rate REAL DEFAULT 0,
                loan_term_months INTEGER,
                lender TEXT,
                notes TEXT,
                forbearance_start_date TEXT,
                forbearance_end_date TEXT,
                total_paid REAL DEFAULT 0,
                last_payment_date TEXT,
                created_at TEXT
            );
        """)
        self.db.execute("""
            CREATE TABLE loan_priority (
                strategy_id INTEGER NOT NULL,
                loan_id INTEGER NOT NULL,
                priority INTEGER NOT NULL,
                PRIMARY KEY (strategy_id, loan_id)
            );
        """)

    def tearDown(self):
        self.db.close()

    def test_insert_and_fetch_loan(self):
        # Insert a loan record
        self.db.execute("""
            INSERT INTO loans (name, principal, current_balance, interest_rate, monthly_min_payment, extra_payment, first_due_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ("Test Loan", 10000.0, 10000.0, 5.0, 150.0, 0.0, "2025-06-01"))

        # Fetch the loan record
        result = self.db.fetchall("SELECT * FROM loans")
        self.assertEqual(len(result), 1)
        loan = result[0]
        self.assertEqual(loan["name"], "Test Loan")
        self.assertEqual(loan["principal"], 10000.0)

    def test_add_and_get_loan_priority(self):
        # Insert a loan record
        self.db.execute("""
            INSERT INTO loans (name, principal, current_balance, interest_rate, monthly_min_payment, extra_payment, first_due_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ("Priority Loan", 5000.0, 5000.0, 4.5, 100.0, 0.0, "2025-07-01"))
        loan_id = self.db.execute("SELECT id FROM loans WHERE name = ?", ("Priority Loan",)).fetchone()["id"]

        # Add loan priority
        self.db.add_loan_priority(strategy_id=1, loan_id=loan_id, priority=1)

        # Retrieve loans by strategy
        loans = self.db.get_loans_by_strategy(strategy_id=1)
        self.assertEqual(len(loans), 1)
        self.assertEqual(loans[0].name, "Priority Loan")

if __name__ == "__main__":
    unittest.main()